"""
Provide interface for
1) connecting to a running OpenOCD process via telnet and
2) reading or writing registers.
"""
# Standard library imports
import ctypes
import logging
from telnetlib import Telnet
import time
# https://docs.python.org/3/library/telnetlib.html
# Deprecated since version 3.11, will be removed in version 3.13
# telnetlib3 is the recommended replacement:
# https://telnetlib3.readthedocs.io/en/latest/intro.html
# Third party imports
import psutil
# Local application/library imports


class Backend:
    """
    An instance of this class will do the job.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int | None = None,
        target_name: str | None = None,
        logger_suffix: str | None = None,
        start_if_reset: bool = False
    ):
        """
        :param host: Optional OpenOCD host name, e.g. localhost.
        :param port: Optional OpenOCD port number, e.g. 4444. Use None if the port number
        is unknown and should be detected.
        :param target_name: Optional OpenOCD target name.
        :param logger_suffix: Optional suffix for the logger name.
        """
        self.logger = logging.getLogger(
            self.__class__.__name__ + ("" if logger_suffix is None else logger_suffix))
        self.host = host
        self.port = port if port is not None else self._find_port()
        self.target_name = target_name
        self.tlnt: Telnet | None = None
        self.start_if_reset = start_if_reset

    @staticmethod
    def _find_port() -> int:
        for proc in psutil.process_iter(["cmdline"]):
            cmd_line = proc.info["cmdline"]
            if len(cmd_line) > 1 and cmd_line[0] == "openocd":
                for param in cmd_line[1:]:
                    if param.startswith("telnet_port"):
                        return int(param[12:])
        raise ValueError("openocd process is not running")

    def __enter__(self):
        self.logger.info("Opening telnet on %s:%s.", self.host, self.port)

        self.tlnt = Telnet()
        self.tlnt.open(self.host, self.port)

        # Read "Open On-Chip Debugger" or any other invitation
        _ = self.tlnt.read_until(b">", timeout=2.0)
        self.logger.debug("Telnet ok.")

        target_names = self.request(cmd="target names")[0].split()
        target_states = [self.request(cmd=f"{name} curstate")[0]for name in target_names]
        self.logger.info("Targets: %s.",
                         ", ".join([f"{name}({state})" for name, state
                                    in zip(target_names, target_states)]))
        if self.target_name is not None:
            if self.target_name not in target_names:
                self.logger.warning("Target name looks wrong.")
            resp = self.request(cmd=f"targets {self.target_name}")
            if resp:
                self.logger.warning(resp)
        target_current, target_state = self.get_current_target_state()
        (self.logger.warning if target_state == "reset" else self.logger.info)(
            "Current target: %s(%s).", target_current, target_state)
        if self.start_if_reset and target_state == "reset":
            _ = self.request(cmd="reset run")
            self.logger.warning("Restarted.")

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.tlnt.close()
        self.logger.debug("Telnet closed.")
        if exc_type is not None:
            self.logger.error("%s: %s", exc_type.__name__, exc_value)

    def request(self, cmd: str, timeout: float = 2.0) -> list[str]:
        """
        Send a command and wait for an answer; return the list of lines except the first,
        which is the request echo, and the last, which is a prompt.

        A successful response consists of the following lines:
        * The echo of the request.
        * (optional) The response if it is supposed to be, e.g. when reading some memory.
        * "\r>", which is the prompt for the following request.
        If there are issues, the response can consist of several lines.
        """
        t_write = time.monotonic()
        self.tlnt.write((cmd + "\n").encode("ascii"))
        self.logger.debug("tx=%s", cmd)
        response_lines = self.tlnt.read_until(b">", timeout=timeout).decode("ascii").split("\r\n")
        self.logger.debug("rx=%s, Δt=%fs", response_lines, time.monotonic() - t_write)
        assert response_lines[0].strip() == cmd, f"Expected to receive the echo (`{cmd}`) but got `{response_lines[0].strip()}`"
        assert response_lines[-1] == "\r>", f"Expected to receive `\\r` but got `{response_lines[-1]}`"
        return response_lines[1:-1]

    def get_current_target_state(self) -> tuple[str, str]:
        """
        As of OpenOCD 0.11, target state can be debug-running, halted, reset, running, or unknown.
        """
        target_current = self.request(cmd="target current")[0]
        target_state = self.request(cmd=f"{target_current} curstate")[0]
        assert target_state in {"debug-running", "halted", "reset", "running", "unknown"}
        return target_current, target_state

    def read_register(self, addr: int | str) -> int | None:
        """
        Read 32-bit registers
        """
        # TODO: check 32-bit alignment

        if isinstance(addr, int):
            # Read a memory-mapped register. Example:
            #   > mdw 0xe000ed04 1
            #   0xe000ed04: 0010000a
            tncmd = (f"mdw 0x{addr:x} 1\n").encode("ascii")
        elif isinstance(addr, str):
            # Read a special core register. Example:
            #   > reg lr
            #   lr (/32): 0x080000d9
            tncmd = (f"reg {addr}\n").encode("ascii")

        self.tlnt.write(tncmd)
        rdb: bytes = self.tlnt.read_until(b">", timeout=2.0)

        self.logger.debug(rdb)
        tnresp = rdb.decode("ascii").split("\r\n")[1]
        # self.logger.debug(tnresp)
        resp_parts = tnresp.split(":")
        assert len(resp_parts) == 2, f"Could not parse the response: `{resp_parts}`"
        val_s = resp_parts[1].strip()
        val = int(val_s, 16)

        # Remove useless lines from the response:
        # err_lines = [line.strip() for line in rdb.decode("ascii").split("\r\n")
        #              if line.strip() not in ("", "\r", ">")]
        # The string "SWD DPIDR 0x6ba02477" doesn"t help because 0x6ba02477 is just
        # the default value of DP_DPIDR (Debug port identification register) for
        # STM32H743/753. This may mean that the target is held at reset.
        # Removing "connect_assert_srst" from "reset_config" in the OpenOCD configuration
        # file may help.
        # raise ValueError(f"Failed reading register 0x{addr:08X}: {err_lines}")

        return val

    def read_memory(self, addr: int, ctype=ctypes.c_uint32) -> int:
        """
        Read a memory cell.
        """
        if ctype in {ctypes.c_int8, ctypes.c_uint8}:
            tncmd = (f"mdb 0x{addr:x} 1\n").encode("ascii")
            response_size = 8  # Size (bits) of individual parts of a response string
        elif ctype in {ctypes.c_int16, ctypes.c_uint16}:
            tncmd = (f"mdh 0x{addr:x} 1\n").encode("ascii")
            response_size = 16
        elif ctype in {ctypes.c_int32, ctypes.c_uint32}:
            tncmd = (f"mdw 0x{addr:x} 1\n").encode("ascii")
            response_size = 32
        elif ctype in {ctypes.c_int64, ctypes.c_uint64}:
            # tncmd = (f"mdd 0x{addr:x} 1\n").encode("ascii")
            tncmd = (f"mdw 0x{addr:x} 2\n").encode("ascii")
            response_size = 32
            # Example of a response: "0x24000740: 008c39df 00000000"
        else:
            raise NotImplementedError(f"{ctype}")
        self.tlnt.write(tncmd)
        rdb: bytes = self.tlnt.read_until(b">", timeout=2.0)

        self.logger.debug(rdb)
        tnresp = rdb.decode("ascii").split("\r\n")[1]
        self.logger.debug(tnresp)
        resp_parts = tnresp.split(":")
        assert len(resp_parts) == 2, f"Could not parse the response: `{resp_parts}`"
        val_s = resp_parts[1].strip().split(" ")
        val = 0
        for i in range(len(val_s)):
            val += int(val_s[i], 16) * 2**(i * response_size)

        if ctype == ctypes.c_int8 and val >= 0x80:
            val = val - 2**8
        elif ctype == ctypes.c_int16 and val >= 0x8000:
            val = val - 2**16
        elif ctype == ctypes.c_int32 and val >= 0x80000000:
            val = val - 2**32
        elif ctype == ctypes.c_int64 and val >= 0x8000000000000000:
            val = val - 2**64

        return val

    def read_registers(self, addrs: list[int]) -> dict[int, int]:
        """
        Read multiple 32-bit registers.
        """
        # TODO: check 32-bit alignment
        addrs = list(addrs)
        reg_vals = {addr: None for addr in addrs}
        for addr in addrs:
            reg_vals[addr] = self.read_register(addr)
        return reg_vals

    def write_register(self, addr: int, val: int) -> None:
        """ Write a value to a register.
        """
        tncmd = (f"mww {addr} {val}\n").encode("ascii")

        self.tlnt.write(tncmd)
        _ = self.tlnt.read_until(b">", timeout=2.0).decode("ascii")

    def write_memory(self, addr: int, val: int, ctype=ctypes.c_uint32) -> None:
        """
        Write a memory cell.
        """
        if ctype in {ctypes.c_int8, ctypes.c_uint8}:
            tncmd = (f"mwb {addr} {val}\n").encode("ascii")
        elif ctype in {ctypes.c_int16, ctypes.c_uint16}:
            tncmd = (f"mwh {addr} {val}\n").encode("ascii")
        elif ctype in {ctypes.c_int32, ctypes.c_uint32}:
            tncmd = (f"mww {addr} {val}\n").encode("ascii")
        elif ctype in {ctypes.c_int64, ctypes.c_uint64}:
            tncmd = (f"mwd {addr} {val}\n").encode("ascii")
        else:
            raise NotImplementedError(f"{ctype}")
        self.tlnt.write(tncmd)
        _ = self.tlnt.read_until(b">", timeout=2.0).decode("ascii")


if __name__ == "__main__":
    # Usage example:
    logging.basicConfig(level=logging.DEBUG)
    HOST = "localhost"
    PORT = 4444
    TARGET = None
    # with Backend(host=HOST, port=PORT, target="master.cpu0") as backend:
    with Backend(host=HOST, port=PORT, target_name=TARGET) as backend:
        # raise ValueError("Testing.")
        pass

    print()
    TARGET0 = None
    TARGET1 = "master.cpu0"
    with Backend(host=HOST, port=PORT, target_name=TARGET0, logger_suffix="0") as backend0, \
            Backend(host=HOST, port=PORT, target_name=TARGET1, logger_suffix="1") as backend1:
        pass
