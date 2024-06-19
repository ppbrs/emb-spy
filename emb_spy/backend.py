"""Backend class."""
import ctypes
import logging
import socket
import time
# https://docs.python.org/3/library/telnetlib.html
# Deprecated since version 3.11, will be removed in version 3.13
# telnetlib3 is the recommended replacement:
# https://telnetlib3.readthedocs.io/en/latest/intro.html
from telnetlib import Telnet

import psutil


class Backend:
    """
    An instance of Backend provides interface for the following:

    1) connecting to a running OpenOCD process via telnet and
    2) reading or writing registers,
    3) executing any supported OpenOCD command.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int | None = None,
        target_name: str | None = None,
        logger_suffix: str | None = None,
        restart_if_not_running: bool = False,
        halt_if_running: bool = False,
    ):
        """
        Construct a Backend object.

        :param host: OpenOCD host name, e.g. "localhost", "10.0.0.3".

        :param port: Optional OpenOCD port number, e.g. 4444. Use None if the port number
        is unknown and should be detected.

        :param target_name: Optional OpenOCD target name. If not provided, the default
        target will be used.

        :param logger_suffix: Optional suffix for the logger name.
        :param restart_if_not_running:
        :param halt_if_running:
        """
        self.logger = logging.getLogger(
            self.__class__.__name__ + ("" if logger_suffix is None else logger_suffix))
        self.host = host
        self.port = port if port is not None else self.find_openocd_telnet_port()
        self.target_name = target_name
        self.tlnt: Telnet | None = None
        self.restart_if_not_running = restart_if_not_running
        self.halt_if_running = halt_if_running

    @staticmethod
    def find_openocd_telnet_port() -> int:
        """
        Scan local running processes and return the telnet port of the first OpenOCD process.

        Example of commnd line for an OpenOCD process:
            openocd -c \
                "gdb_port 50000" \
                -c "tcl_port 50001" \
                -c "telnet_port 50002" \
                -s ~/projects/fw7.wt1 \
                -f ~/.vscode/extensions/marus25.cortex-debug-1.12.1/support/openocd-helpers.tcl \
                -f serpens/openocd.cfg

        When telnet_port is not provided, OpenOCD will use the default value: 4444.
        However, this may not be true.
        """
        for proc in psutil.process_iter(["cmdline"]):
            cmd_line = proc.info["cmdline"]
            if cmd_line is not None and len(cmd_line) > 1 and "openocd" in cmd_line[0]:
                logging.debug("Found OpenOCD process, pid=%d, cmd_line=\"%s\".",
                              proc.pid, " ".join(cmd_line))
                for param in cmd_line[1:]:
                    if param.startswith("telnet_port"):
                        return int(param[12:])
                port = 4444
                logging.warning("Telnet port was not provided explicitly, assuming the default "
                                "value %d is used.", port)
                logging.debug("Checking this by trying to open TCP port %d", port)
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(("localhost", port))
                    sock.close()
                    logging.debug("TCP port %d looks like the one you are looking for.", port)
                    return port
                except ConnectionRefusedError:
                    logging.debug("Could not open TCP port %d. It is either used by another"
                                  "application or not open at all.", port)
        raise ValueError("OpenOCD process is not running.")

    def __enter__(self):
        """Connect to OpenOCD via telnet, list targets, set current target."""
        self.logger.debug("Opening telnet on %s:%s.", self.host, self.port)

        self.tlnt = Telnet()
        self.tlnt.open(self.host, self.port)

        # Read "Open On-Chip Debugger" or any other invitation
        _ = self.tlnt.read_until(b">", timeout=2.0)

        raddr, rport = self.tlnt.get_socket().getpeername()
        laddr, lport = self.tlnt.get_socket().getsockname()
        self.logger.info("Opened telnet on %s:%s (from %s:%s).", raddr, rport, laddr, lport)

        target_names = self.request(cmd="target names")[0].split()
        target_name_current = self.request(cmd="target current")[0]
        target_states = [self.request(cmd=f"{name} curstate")[0] for name in target_names]
        target_reports = []
        for name, state in zip(target_names, target_states):
            report = f"{name}={state}"
            if name == target_name_current:
                report = "CURRENT:" + report
            target_reports.append(report)
        self.logger.info("Targets: %s.", ", ".join(target_reports))

        if self.target_name is not None:
            if self.target_name not in target_names:
                raise ValueError(f"Target name `{self.target_name}` is not in the list of targets: {target_names}.")
            resp = self.request(cmd=f"targets {self.target_name}")
            if resp:
                self.logger.warning(resp)
        target_current, target_state = self.get_current_target_state()
        (self.logger.warning if target_state == "reset" else self.logger.info)(
            "Current target: %s(%s).", target_current, target_state)
        if self.restart_if_not_running and "running" not in target_state:
            _ = self.request(cmd="reset run")
            self.logger.warning("Restarted.")
            time.sleep(3.0)
        if self.halt_if_running:
            _ = self.request(cmd="halt")
            # _ = self.request(cmd="reset halt")
            self.logger.warning("Halted.")

        self.logger.debug("End of __enter__().")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """Disconnect from OpenOCD."""
        self.logger.debug("Start of __exit__().")
        self.tlnt.close()
        self.logger.info("Telnet closed.")
        if exc_type is not None:
            self.logger.error("%s: %s", exc_type.__name__, exc_value)

    def request(
        self,
        cmd: str,
        timeout: float = 2.0
    ) -> list[str]:
        """
        Send a command and wait for an answer; return the list of lines except the first,
        which is the request echo, and the last, which is a prompt.

        A successful response consists of the following lines:
        * The echo of the request.
        * (optional) The response if it is supposed to be, e.g. when reading some memory.
        * ">", which is the prompt for the following request.
        If there are issues, the response can consist of several lines.
        """
        #
        # Read and discard any available data.
        #
        _ = self.tlnt.read_very_eager()

        #
        # Send request.
        #
        t_write = time.monotonic()
        self.tlnt.write((cmd + "\n").encode("ascii"))
        self.logger.debug("tx=\"%s\"", cmd)

        #
        # Collect and show replies.
        #
        r_chars = ""
        # The very first received line is echo, so we don't bother showing it.
        r_last_reported_line = 0
        while True:
            r_bytes = self.tlnt.read_eager()
            r_chars += r_bytes.decode("ascii")

            # Some requests may be quite long; for example, "program" that may take up to a minute.
            # It is more comfortable for human users to see response lines in real time,
            # not after the final ">" is received.
            r_lines = [r_line for r_line in r_chars.replace("\r", "\n").split("\n") if r_line != ""]
            if r_last_reported_line < len(r_lines) - 1:
                for i in range(r_last_reported_line + 1, len(r_lines)):
                    if ">" not in (r_line := r_lines[i]):
                        self.logger.debug(
                            "Δt=%2.03fs: rx=\"%s\", ", time.monotonic() - t_write, r_line)
                r_last_reported_line = len(r_lines) - 1

            if b">" in r_bytes:
                break
            if time.monotonic() > (t_write + timeout):
                self.logger.warning("Δt=%2.03fs: rx timeout", time.monotonic() - t_write)
                break

        r_chars = r_chars.rstrip()
        r_lines = [r_line for r_line in r_chars.replace("\r", "\n").split("\n") if r_line != ""]

        # r_bytes = self.tlnt.read_until(b">", timeout=timeout)
        # r_chars = r_bytes.decode("ascii")
        # r_lines = [r_line for r_line in r_chars.replace("\r", "\n").split("\n") if r_line != ""]
        # for r_line in r_lines:
        #     self.logger.debug("Δt=%2.03fs: rx=\"%s\", ", time.monotonic() - t_write, r_line)

        # Analyze replies.
        assert r_lines[0].strip() == cmd, \
            f"{cmd}: Expected to receive the echo (`{cmd}`) but got `{r_lines[0].strip()}`"
        if r_lines[-1] != ">":
            self.logger.warning("%s: Expected to receive `>` in the last line, but got `%s`",
                                cmd, {r_lines[-1]})
            r_lines = r_lines[1:0]
        else:
            r_lines = r_lines[1:-1]
        return r_lines

    def get_current_target_state(self) -> tuple[str, str]:
        """
        As of OpenOCD 0.11, target state can be debug-running, halted, reset, running, or unknown.
        """
        target_current = self.request(cmd="target current")[0]
        target_state = self.request(cmd=f"{target_current} curstate")[0]
        assert target_state in {"debug-running", "halted", "reset", "running", "unknown"}
        return target_current, target_state

    # def read_register(self, addr: int | str) -> int | None:
    #     """
    #     Read 32-bit registers
    #     """
    #     # TODO: check 32-bit alignment

    #     if isinstance(addr, int):
    #         # Read a memory-mapped register. Example:
    #         #   > mdw 0xe000ed04 1
    #         #   0xe000ed04: 0010000a
    #         cmd = (f"mdw 0x{addr:x} 1\n").encode("ascii")
    #     # elif isinstance(addr, str):
    #     #     # Read a special core register. Example:
    #     #     #   > reg lr
    #     #     #   lr (/32): 0x080000d9
    #     #     cmd = (f"reg {addr}\n").encode("ascii")
    #     else:
    #         assert False, "FIXME"
    #     self.logger.debug("tx=%s", cmd)

    #     self.tlnt.write(cmd)
    #     rdb: bytes = self.tlnt.read_until(b">", timeout=2.0)

    #     self.logger.debug("rx=%s", rdb)
    #     tnresp = rdb.decode("ascii").split("\r\n")[1]
    #     # self.logger.debug(tnresp)
    #     resp_parts = tnresp.split(":")
    #     assert len(resp_parts) == 2, f"Could not parse the response: `{resp_parts}`"
    #     val_s = resp_parts[1].strip()
    #     val = int(val_s, 16)

    #     # Remove useless lines from the response:
    #     # err_lines = [line.strip() for line in rdb.decode("ascii").split("\r\n")
    #     #              if line.strip() not in ("", "\r", ">")]
    #     # The string "SWD DPIDR 0x6ba02477" doesn"t help because 0x6ba02477 is just
    #     # the default value of DP_DPIDR (Debug port identification register) for
    #     # STM32H743/753. This may mean that the target is held at reset.
    #     # Removing "connect_assert_srst" from "reset_config" in the OpenOCD configuration
    #     # file may help.
    #     # raise ValueError(f"Failed reading register 0x{addr:08X}: {err_lines}")

    #     return val

    def read_core_register(
        self,
        name: str
    ) -> bytes | None:
        """
        Read a special core register.

        Target must be halted for core register accesses.

        If OpenOCD refuses to give out the value, return None.

        Examples:
        1. When everything goes fine:

        > reg lr
        <  reg lr (i.e. echo)
        < lr (/32): 0x080000d9

        2. When trying to read a register on a running core:

        > reg r0 force
        <  reg r0 force
        < Could not read register 'r0'
        < embedded:startup.tcl:1241: Error:
        < nat file "embedded:startup.tcl", line 1241\r\n\r>'
        """
        tx_line: str = f"reg {name} force"
        tx_bytes = (tx_line + "\n").encode("ascii")
        self.logger.debug("tx=%s.", tx_bytes)
        self.tlnt.write(tx_bytes)
        rx_bytes: bytes = self.tlnt.read_until(b">", timeout=2.0)
        self.logger.debug("rx=%s.", rx_bytes)

        lines = [line.decode("ascii").strip() for line in rx_bytes.replace(b"\r", b"\n").split(b"\n") if line and line != b">"]
        assert lines[0] == tx_line  # echo
        assert len(lines) > 1
        if "Could not read register" in lines[1]:
            return None

        line = lines[1]
        assert len(line_parts := line.split(":")) == 2, f"Line '{line}' doesn't have exactly one colon."
        val_str = line_parts[1].strip()
        assert len(val_str.split(" ")) == 1, f"More than 1 value in the response line: {val_str}"
        return int(val_str, 16).to_bytes(length=4, byteorder="little", signed=False)

    def read_raw_memory(
        self,
        addr: int,
        size: int
    ) -> bytes:
        """

        Exchange example:
            > b'mdw 0x20000600 1\n'.
            < b' mdw 0x20000600 1\r\n0x20000600: 00078b76 \r\n\r\n\r>'.

        OpenOCD seems to respond with maximum 8 words, 16 half-words, and 32 bytes per line.

        """
        addr_start = addr
        addr_end = addr + size
        if (addr_start % 4) == 0 and (addr_end % 4) == 0:
            num_vals = size // 4
            tx_line: str = (f"mdw 0x{addr:x} {num_vals}")
            num_rx_lines_exp = ((size // 4) + 7) // 8
            val_len = 4
        elif (addr_start % 2) == 0 and (addr_end % 2) == 0:
            num_vals = size // 2
            tx_line: str = (f"mdh 0x{addr:x} {num_vals}")
            num_rx_lines_exp = ((size // 2) + 15) // 16
            val_len = 2
        else:
            num_vals = size
            tx_line: str = (f"mdb 0x{addr:x} {num_vals}")
            num_rx_lines_exp = (size + 31) // 32
            val_len = 1

        tx_bytes = (tx_line + "\n").encode("ascii")
        self.logger.debug("tx=%s.", tx_bytes)
        self.tlnt.write(tx_bytes)
        rx_bytes: bytes = self.tlnt.read_until(b">", timeout=2.0)
        self.logger.debug("rx=%s.", rx_bytes)

        lines = [line.decode("ascii").strip() for line in rx_bytes.replace(b"\r", b"\n").split(b"\n") if line and line != b">"]
        assert lines[0] == tx_line  # echo
        lines = lines[1:]
        assert len(lines) == num_rx_lines_exp

        vals: list[str] = []
        for line in lines:
            assert len(line_parts := line.split(":")) == 2, f"Line '{line}' doesn't have exactly one colon."
            vals += line_parts[1].strip().split(" ")
        assert len(vals) == num_vals

        data = b""
        for val_hex in vals:
            data += int(val_hex, 16).to_bytes(length=val_len, byteorder="little", signed=False)
        self.logger.debug("%s; %s; %s.", lines, vals, data)

        return data

    # def read_memory(self, addr: int, ctype=ctypes.c_uint32) -> int:
    #     """
    #     Read a memory cell.
    #     """
    #     if ctype in {ctypes.c_int8, ctypes.c_uint8}:
    #         tncmd = (f"mdb 0x{addr:x} 1\n").encode("ascii")
    #         response_size = 8  # Size (bits) of individual parts of a response string
    #     elif ctype in {ctypes.c_int16, ctypes.c_uint16}:
    #         tncmd = (f"mdh 0x{addr:x} 1\n").encode("ascii")
    #         response_size = 16
    #     elif ctype in {ctypes.c_int32, ctypes.c_uint32}:
    #         tncmd = (f"mdw 0x{addr:x} 1\n").encode("ascii")
    #         response_size = 32
    #     elif ctype in {ctypes.c_int64, ctypes.c_uint64}:
    #         # tncmd = (f"mdd 0x{addr:x} 1\n").encode("ascii")
    #         tncmd = (f"mdw 0x{addr:x} 2\n").encode("ascii")
    #         response_size = 32
    #         # Example of a response: "0x24000740: 008c39df 00000000"
    #     else:
    #         raise NotImplementedError(f"{ctype}")
    #     self.tlnt.write(tncmd)
    #     rdb: bytes = self.tlnt.read_until(b">", timeout=2.0)

    #     self.logger.debug(rdb)
    #     tnresp = rdb.decode("ascii").split("\r\n")[1]
    #     self.logger.debug(tnresp)
    #     resp_parts = tnresp.split(":")
    #     assert len(resp_parts) == 2, f"Could not parse the response: `{resp_parts}`"
    #     val_s = resp_parts[1].strip().split(" ")
    #     val = 0
    #     for i in range(len(val_s)):
    #         val += int(val_s[i], 16) * 2**(i * response_size)

    #     if ctype == ctypes.c_int8 and val >= 0x80:
    #         val = val - 2**8
    #     elif ctype == ctypes.c_int16 and val >= 0x8000:
    #         val = val - 2**16
    #     elif ctype == ctypes.c_int32 and val >= 0x80000000:
    #         val = val - 2**32
    #     elif ctype == ctypes.c_int64 and val >= 0x8000000000000000:
    #         val = val - 2**64

    #     return val

    # def read_registers(self, addrs: list[int]) -> dict[int, int]:
    #     """
    #     Read multiple 32-bit registers.
    #     """
    #     # TODO: check 32-bit alignment
    #     addrs = list(addrs)
    #     reg_vals = {addr: None for addr in addrs}
    #     for addr in addrs:
    #         reg_vals[addr] = self.read_register(addr)
    #     return reg_vals

    # def write_register(self, addr: int, val: int) -> None:
    #     """ Write a value to a register.
    #     """
    #     tncmd = (f"mww {addr} {val}\n").encode("ascii")

    #     self.tlnt.write(tncmd)
    #     _ = self.tlnt.read_until(b">", timeout=2.0).decode("ascii")

    # def write_memory(self, addr: int, val: int, ctype=ctypes.c_uint32) -> None:
    #     """
    #     Write a memory cell.
    #     """
    #     if ctype in {ctypes.c_int8, ctypes.c_uint8}:
    #         tncmd = (f"mwb {addr} {val}\n").encode("ascii")
    #     elif ctype in {ctypes.c_int16, ctypes.c_uint16}:
    #         tncmd = (f"mwh {addr} {val}\n").encode("ascii")
    #     elif ctype in {ctypes.c_int32, ctypes.c_uint32}:
    #         tncmd = (f"mww {addr} {val}\n").encode("ascii")
    #     elif ctype in {ctypes.c_int64, ctypes.c_uint64}:
    #         tncmd = (f"mwd {addr} {val}\n").encode("ascii")
    #     else:
    #         raise NotImplementedError(f"{ctype}")
    #     self.tlnt.write(tncmd)
    #     _ = self.tlnt.read_until(b">", timeout=2.0).decode("ascii")
