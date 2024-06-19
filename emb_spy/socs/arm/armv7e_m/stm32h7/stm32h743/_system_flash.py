"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def _init_system_flash(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"

    self.append(MmapReg(
        name="SYS_FLASH_SIZE", addr=0x1FF1E880, descr="Flash memory size",
        bits=[
            Bits(bits=range(16), name="F_SIZE", descr="Flash memory size in KBytes."),
        ]))
