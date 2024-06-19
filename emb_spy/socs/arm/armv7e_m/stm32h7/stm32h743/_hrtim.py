"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_hrtim(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"

    base = 0x40017400

    self.append(MmapReg(
        name="HRTIM_MCR", addr=(base + 0x000),
        descr="HRTIM Master Timer Control Register.",
        bits=[
            Bits(bits=21, name="TECEN", descr="Timer E counter enable"),
            Bits(bits=20, name="TDCEN", descr="Timer D counter enable"),
            Bits(bits=19, name="TCCEN", descr="Timer C counter enable"),
            Bits(bits=18, name="TBCEN", descr="Timer B counter enable"),
            Bits(bits=17, name="TACEN", descr="Timer A counter enable"),
            Bits(bits=16, name="MCEN", descr="Master timer counter enable"),
            Bits(bits=range(0, 3), name="CKPSC", descr="Clock prescaler",),
            # 101: fCOUNTER = fHRTIM
            # 110: fCOUNTER = fHRTIM / 2
            # 111: fCOUNTER = fHRTIM / 4
        ]))
