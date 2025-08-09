"""Part of STM32H743 SoC."""

from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_hrtim(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"

    base = 0x40017400
    base_master = base
    base_timer_a = base + 0x080
    base_timer_b = base + 0x100
    base_timer_c = base + 0x180
    base_timer_d = base + 0x200
    base_timer_e = base + 0x280
    base_common = base + 0x380

    self.append(
        MmapReg(
            name="HRTIM_MCR",
            addr=(base + 0x000),
            descr="HRTIM Master Timer Control Register.",
            bits=[
                Bits(bits=21, name="TECEN", descr="Timer E counter enable"),
                Bits(bits=20, name="TDCEN", descr="Timer D counter enable"),
                Bits(bits=19, name="TCCEN", descr="Timer C counter enable"),
                Bits(bits=18, name="TBCEN", descr="Timer B counter enable"),
                Bits(bits=17, name="TACEN", descr="Timer A counter enable"),
                Bits(bits=16, name="MCEN", descr="Master timer counter enable"),
                Bits(
                    bits=range(0, 3),
                    name="CKPSC",
                    descr="Clock prescaler",
                ),
                # 101: fCOUNTER = fHRTIM
                # 110: fCOUNTER = fHRTIM / 2
                # 111: fCOUNTER = fHRTIM / 4
            ],
        )
    )

    for x, base_timer in zip(
        [
            "A",
            "B",
            "C",
            "D",
            "E",
        ],
        [
            base_timer_a,
            base_timer_b,
            base_timer_c,
            base_timer_d,
            base_timer_e,
        ],
    ):
        self.append(
            MmapReg(
                name=f"HRTIM_TIM{x}CR",
                addr=(base_timer + 0x000),
                descr=f"HRTIM Timer{x} Control Register.",
                bits=[
                    Bits(bits=range(0, 3), name="CKPSC", descr=f"Timer{x} Clock prescaler"),
                ],
            )
        )
        self.append(
            MmapReg(
                name=f"HRTIM_CNT{x}R",
                addr=(base_timer + 0x010),
                descr=f"HRTIM Timer{x} Counter Register.",
                bits=[
                    Bits(
                        bits=range(0, 16),
                        name="CNT",
                        descr=f"Timer{x} Counter value",
                    ),
                ],
            )
        )
        self.append(
            MmapReg(
                name=f"HRTIM_PER{x}R",
                addr=(base_timer + 0x014),
                descr=f"HRTIM Timer{x} Period Register.",
                bits=[
                    Bits(
                        bits=range(0, 16),
                        name="PER",
                        descr=f"Timer{x} Period value",
                    ),
                ],
            )
        )
