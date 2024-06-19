"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def _init_syscfg(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"
    base = 0x58000400
    # ==============================================================================================
    self.append(MmapReg(
        name="SYSCFG_PMCR", addr=(base + 0x04),
        descr="SYSCFG peripheral mode configuration register.",
        bits=[
            Bits(bits=27, name="PC3SO", descr="PC3 to PC3_C Switch Open",),
            # 0: Analog switch closed (pads are connected through the analog switch)
            # 1: Analog switch open (2 separated pads)
            Bits(bits=26, name="PC2SO", descr="PC2 to PC2_C Switch Open",),
            Bits(bits=25, name="PA1SO", descr="PA1 to PA1_C Switch Open",),
            Bits(bits=24, name="PA0SO", descr="PA0 to PA0_C Switch Open",),
        ]))

    self.append(MmapReg(
        name="SYSCFG_PKGR", addr=(base + 0x124),
        descr="SYSCFG package register.",
        bits=[
            Bits(bits=range(0, 4), name="PKG", descr="Package",),
            # 0000: LQFP100
            # 0010: TQFP144
            # 0101: TQFP176/UFBGA176
            # 1000: LQFP208/TFBGA240
        ]))
