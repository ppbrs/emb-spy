"""USB part of STM32H743 SoC."""

from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_usb(self: SoC) -> None:
    """Update SoC with memory-mapped registers accessing USB."""
    assert self.__class__.__name__ == "STM32H743"

    # 0x40080000 - 0x400BFFFF USB2
    # 0x40040000 - 0x4007FFFF USB1
