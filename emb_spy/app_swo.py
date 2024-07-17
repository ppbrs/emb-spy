"""
An application that captures and presents data from SWO.
"""
from __future__ import annotations

import enum
import errno
import logging
import pathlib
import select
import socket
import time

from .backend import Backend


class _AppSwoParser:

    @property
    def data(self) -> dict[int, bytearray]:
        """Return the dictionary holding binary data from streams."""
        return self._data

    def __init__(
            self,
            tsformat: AppSwo.TimestampFormat,
            out_path_base: pathlib.Path = pathlib.Path.cwd() / "app_swo_output_default"
    ) -> None:
        self._data = {}
        self.data_left = 0  # How many bytes of data left to get
        self.data_actual = None
        self.channel = None  # Actual channel
        self.out_path_base = out_path_base
        self.tstart = time.time()
        self.tsformat = tsformat

    def _save_data(self) -> None:
        fpath_bin = self.out_path_base.with_suffix(f".ch{self.channel:02d}.bin.log")
        fpath_txt = self.out_path_base.with_suffix(f".ch{self.channel:02d}.log")
        with open(fpath_bin, "ab") as file_bin:
            file_bin.write(self.data_actual)
        with open(fpath_txt, "a", encoding="utf-8") as file_txt:
            trecv = time.time()
            if self.tsformat == AppSwo.TimestampFormat.RELATIVE:
                trecv_ms = int(1000 * (trecv - self.tstart))
                tstamp = f"{trecv_ms:6d}"
            else:
                trecv_ms = int(1000 * (trecv - int(trecv)))
                stl = time.localtime(trecv)
                tstamp = time.strftime("%Y%m%dT%H%M%S", stl) + f".{trecv_ms:03d}"
            unsigned = int.from_bytes(self.data_actual, byteorder="little", signed=False)
            signed = int.from_bytes(self.data_actual, byteorder="little", signed=True)
            match len(self.data_actual):
                case 1:
                    unsigned = int.from_bytes(self.data_actual, byteorder="little", signed=False)
                    file_txt.write(f"{tstamp}: u8={unsigned}, i8={signed}, c={chr(unsigned)},\n")
                case 2:
                    file_txt.write(f"{tstamp}: u16={unsigned}, i16={signed},\n")
                case 4:
                    file_txt.write(f"{tstamp}: u32={unsigned}, i32={signed},\n")
                case _:
                    raise ValueError

    def process_bytes(self, new_bytes: bytes) -> None:
        """
        Continue parsing the SWO stream.
        """
        for new_byte in new_bytes:
            if self.data_left:
                self.data_actual += bytearray([new_byte])
                self.data_left -= 1
                if self.data_left == 0:
                    self._data[self.channel] += self.data_actual
                    self._save_data()
            else:
                # The third bit of a header must be zero, and the last two bits can"t be zero.
                if (new_byte & 0b00000100 == 0) and (new_byte & 0b00000011 != 0):
                    self.channel = new_byte >> 3
                    match new_byte & 0b00000011:
                        case 1:
                            self.data_left = 1
                        case 2:
                            self.data_left = 2
                        case 3:
                            self.data_left = 4
                        case _:
                            raise ValueError
                    if self._data.get(self.channel) is None:
                        self._data[self.channel] = bytearray()
                    self.data_actual = bytearray()
                else:
                    logging.warning("New byte %s, loss of sync.", bin(new_byte))


class AppSwo:
    """
    An application that captures and presents data from SWO.
    """

    @enum.unique
    class TimestampFormat(enum.Enum):
        """
        The format of timestamps in output files.
        """

        RELATIVE = enum.auto()
        """In milliseconds elapsed since the start of capturing."""
        ABSOLUTE = enum.auto()
        """Local date and time."""

    # pylint: disable-next=too-many-arguments
    def __init__(self,
                 traceclkin_freq: int,
                 trace_freq: int,
                 logger_suffix: str = "",
                 out_path_base: pathlib.Path = pathlib.Path.cwd() / "app_swo_output_default",
                 tsformat: AppSwo.TimestampFormat = TimestampFormat.RELATIVE,
                 host: str = "localhost",
                 port: int | None = None
                 ) -> None:
        self.logger_suffix = logger_suffix if logger_suffix is not None else ""
        self.logger = logging.getLogger(self.__class__.__name__ + self.logger_suffix)
        self.port = Backend.find_openocd_telnet_port() if port is None else port
        self.host = host
        self.parser = _AppSwoParser(out_path_base=out_path_base, tsformat=tsformat)
        self.traceclkin_freq = traceclkin_freq
        self.trace_freq = trace_freq

    def enable(self, restart: bool) -> None:
        """Enable receiving bytes from SWO."""
        with Backend(host=self.host, port=self.port, target_name=None,
                     logger_suffix=self.logger_suffix) as backend:
            backend.request(cmd=(f"tpiu config internal :{self.port + 10} uart off "
                                 f"{self.traceclkin_freq} {self.trace_freq}"))
            backend.request(cmd="itm ports on")

            if restart:
                backend.request(cmd="reset run")

    def disable(self) -> None:
        """Disable receiving bytes from SWO."""
        with Backend(host=self.host, port=self.port, target_name=None,
                     logger_suffix=self.logger_suffix) as backend:
            backend.request(cmd="tpiu config disable")

    def collect(self, timeout) -> None:
        """Capture and parse bytes from SWO, save raw and human-readable result to files."""
        self.logger.debug("Connecting to TCP server: %s:%d", self.host, self.port + 10)
        cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cli_sock.connect((self.host, self.port + 10))
        self.logger.debug("Connected.")

        cli_sock.setblocking(False)
        t_return = time.monotonic() + timeout
        while time.monotonic() < t_return:
            try:
                rx_data = cli_sock.recv(1024)  # try to send as much as possible
                logging.debug("Received %d bytes.", len(rx_data))
                self.parser.process_bytes(rx_data)
            except socket.error as exc:  # buffer is full
                if exc.errno != errno.EAGAIN:
                    raise exc
                _ = select.select([], [cli_sock], [], None)  # This blocks until

        cli_sock.close()

        return self.parser.data
