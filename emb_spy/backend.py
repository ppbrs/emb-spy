"""
Provide interface for
1) connecting to a running OpenOCD process via telnet and
2) reading or writing registers.
"""
# Standard library imports
import ctypes
import re
import logging
from telnetlib import Telnet
# https://docs.python.org/3/library/telnetlib.html
# Deprecated since version 3.11, will be removed in version 3.13
# telnetlib3 is the recommended replacement:
# https://telnetlib3.readthedocs.io/en/latest/intro.html

# Third party imports

# Local application/library imports


class Backend:
    """ An instance of this class will do the job.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.tlnt: Telnet | None = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def __enter__(self):
        self.logger.debug("telnet: opening on %s %s", self.host, self.port)

        self.tlnt = Telnet()
        self.tlnt.open(self.host, self.port)

        # Read "Open On-Chip Debugger" or any other invitation
        self.tlnt.read_until(b">", timeout=2.0)

        self.logger.debug("telnet: ok")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.tlnt.close()
        if exc_type is not None:
            print(f"{exc_type=}")
            print(f"{exc_value=}")
            print(f"{exc_tb=}")

    def read_register(self, addr: int | str) -> int | None:
        """
        Read 32-bit registers
        """
        # TODO: check 32-bit alignment

        if isinstance(addr, int):
            # Read a memory-mapped register. Example:
            #   > mdw 0xe000ed04 1
            #   0xe000ed04: 0010000a 
            tncmd = (f"mdw {addr} 1\n").encode("ascii")
        elif isinstance(addr, str):
            # Read a special core register. Example:
            #   > reg lr
            #   lr (/32): 0x080000d9
            tncmd = (f"reg {addr}\n").encode("ascii")

        self.tlnt.write(tncmd)
        rdb: bytes = self.tlnt.read_until(b">", timeout=2.0)

        tnresp = rdb.decode("ascii").split("\r\n")[1]
        # print(tnresp)
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

        if ctype in {ctypes.c_int8, ctypes.c_uint8}:
            tncmd = (f"mdb {addr} 1\n").encode("ascii")
        elif ctype in {ctypes.c_int16, ctypes.c_uint16}:
            tncmd = (f"mdh {addr} 1\n").encode("ascii")
        elif ctype in {ctypes.c_int32, ctypes.c_uint32}:
            tncmd = (f"mdw {addr} 1\n").encode("ascii")
        elif ctype in {ctypes.c_int64, ctypes.c_uint64}:
            tncmd = (f"mdd {addr} 1\n").encode("ascii")
        else:
            raise NotImplementedError(f"{ctype}")
        self.tlnt.write(tncmd)
        rdb: bytes = self.tlnt.read_until(b">", timeout=2.0)

        tnresp = rdb.decode("ascii").split("\r\n")[1]
        # print(tnresp)
        resp_parts = tnresp.split(":")
        assert len(resp_parts) == 2, f"Could not parse the response: `{resp_parts}`"
        val_s = resp_parts[1].strip()
        val = int(val_s, 16)

        if ctype == ctypes.c_int8:
            val = val - 2**8
        elif ctype == ctypes.c_int16:
            val = val - 2**16
        elif ctype == ctypes.c_int32:
            val = val - 2**32

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
        print(_)

    def write_memory(self, addr: int, val: int, ctype=ctypes.c_uint32) -> None:

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
        print(_)


if __name__ == "__main__":
    # Usage example:
    HOST = "localhost"
    PORT = 4444
    with Backend(host=HOST, port=PORT) as backend:
        pass
        # raise Exception
