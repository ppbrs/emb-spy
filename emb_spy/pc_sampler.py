"""Contains PCSampler class."""
import ctypes
import logging
import threading
import time

from emb_spy import Backend
from emb_spy.socs.reg import Reg
from emb_spy.socs.soc import SoC


class PCSampler:
    """Collect processors PC values during a given time."""

    def __init__(
        self,
        host: str,
        port: int,
        soc: SoC,
        jtag_target_name: str,
    ) -> None:
        """Prepare for sampling."""
        self.logger = logging.getLogger("PCSampler")
        self.polling = False
        self.polling_stop_request = False
        self.polling_pc_vals = []
        self.polling_thread = None

        self.host = host
        self.port = port

        reg_pcsr = soc.map_name()["DWT_PCSR"]
        assert isinstance(reg_pcsr, Reg)
        self.reg_pcsr_addr = reg_pcsr.addr

        self.jtag_target_name = jtag_target_name

    def collect(
        self,
        duration: float,
    ) -> list[int]:
        """Sample PC values in a blocking way."""
        self.start_collecting()
        time.sleep(duration)
        return self.stop_collecting()

    def start_collecting(
        self,
    ) -> None:
        """Start sampling PC values in a non-blocking way."""
        assert not self.polling

        self.polling = True
        self.polling_thread = threading.Thread(target=self._collect_func, daemon=True)
        self.polling_thread.start()

    def _collect_func(self) -> None:
        self.logger.info("Started polling PCSR.")
        self.polling_pc_vals = []
        with Backend(
            host=self.host,
            port=self.port,
            target_name=self.jtag_target_name,
            restart_if_not_running=True,
            halt_if_running=False,
        ) as backend:
            while True:
                if self.polling_stop_request:
                    self.polling = False
                    self.polling_stop_request = False
                    break
                raw_mem = backend.read_raw_memory(addr=self.reg_pcsr_addr, size=4)
                pc_val = ctypes.c_uint32.from_buffer_copy(raw_mem).value
                self.polling_pc_vals.append(pc_val)
        self.logger.info("Done polling PCSR, %d samples collected.", len(self.polling_pc_vals))

    def stop_collecting(
        self,
    ) -> list[int]:
        """Stop sampling PC values and return them."""
        assert self.polling

        self.polling_stop_request = True

        self.polling_thread.join()

        return self.polling_pc_vals
