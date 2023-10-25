"""
Get data from SWO port and split it into separate channels.
"""
import logging
# import time

from .backend import Backend


class AppSwoParser:

    def __init__(self):
        self._data = {}
        self.data_left = 0  # How many bytes of data left to get
        self.channel = None  # Actual channel

    def process_bytes(self, new_bytes: bytes):
        for new_byte in new_bytes:
            if self.data_left:
                # logging.debug("New byte %s, data left %d", hex(new_byte), self.data_left)
                self._data[self.channel] += bytearray([new_byte])
                self.data_left -= 1
            else:
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
                    # logging.debug("New byte %s, channel %d, data left %d", bin(new_byte), self.channel, self.data_left)
                else:
                    logging.warning("New byte %s, loss of sync.", bin(new_byte))


# The third bit of a header must be zero, and the last two bits
            # can't be zero.

    @property
    def data(self):
        return self._data


class AppSwo:

    def __init__(self, host: str, port: int,
                 logger_suffix: str | None = None) -> None:
        self.logger_suffix = logger_suffix if logger_suffix is not None else ""
        self.logger = logging.getLogger(self.__class__.__name__ + self.logger_suffix)
        self.host = host
        self.port = port

    def enable(self) -> None:
        with Backend(host=self.host, port=self.port, target_name=None,
                     logger_suffix=self.logger_suffix) as backend:
            backend.request(cmd="tpiu config internal swo.log uart false 64000000 2000000")
            backend.request(cmd="itm ports on")

    def disable(self) -> None:
        with Backend(host=self.host, port=self.port, target_name=None,
                     logger_suffix=self.logger_suffix) as backend:
            backend.request(cmd="tpiu config disable")

    def get_status(self) -> None:
        with Backend(host=self.host, port=self.port, target_name=None,
                     logger_suffix=self.logger_suffix) as backend:
            backend.request(cmd="tpiu names")
