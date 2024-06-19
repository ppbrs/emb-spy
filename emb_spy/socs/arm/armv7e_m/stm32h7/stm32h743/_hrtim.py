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
        # ------------------------------------------------------------------------------------------
        output_set_reset_bits = [
            Bits(bits=31, name="UPDATE", descr="Registers update (transfer preload to active)"),
            Bits(bits=30, name="EXTEVNT10", descr="External Event 10"),
            Bits(bits=29, name="EXTEVNT9", descr="External Event 9"),
            Bits(bits=28, name="EXTEVNT8", descr="External Event 8"),
            Bits(bits=27, name="EXTEVNT7", descr="External Event 7"),
            Bits(bits=26, name="EXTEVNT6", descr="External Event 6"),
            Bits(bits=25, name="EXTEVNT5", descr="External Event 5"),
            Bits(bits=24, name="EXTEVNT4", descr="External Event 4"),
            Bits(bits=23, name="EXTEVNT3", descr="External Event 3"),
            Bits(bits=22, name="EXTEVNT2", descr="External Event 2"),
            Bits(bits=21, name="EXTEVNT1", descr="External Event 1"),
            Bits(bits=20, name="TIMEVNT9", descr="Timer Event 9"),
            Bits(bits=19, name="TIMEVNT8", descr="Timer Event 8"),
            Bits(bits=18, name="TIMEVNT7", descr="Timer Event 7"),
            Bits(bits=17, name="TIMEVNT6", descr="Timer Event 6"),
            Bits(bits=16, name="TIMEVNT5", descr="Timer Event 5"),
            Bits(bits=15, name="TIMEVNT4", descr="Timer Event 4"),
            Bits(bits=14, name="TIMEVNT3", descr="Timer Event 3"),
            Bits(bits=13, name="TIMEVNT2", descr="Timer Event 2"),
            Bits(bits=12, name="TIMEVNT1", descr="imer Event 1"),
            Bits(bits=11, name="MSTCMP4", descr="Master Compare 4"),
            Bits(bits=10, name="MSTCMP3", descr="Master Compare 3"),
            Bits(bits=9, name="MSTCMP2", descr="Master Compare 2"),
            Bits(bits=8, name="MSTCMP1", descr="Master Compare 1"),
            Bits(bits=7, name="MSTPER", descr="Master Period"),
            Bits(bits=6, name="CMP4", descr="Timer x Compare 4"),
            Bits(bits=5, name="CMP3", descr="Timer x Compare 3"),
            Bits(bits=4, name="CMP2", descr="Timer x Compare 2"),
            Bits(bits=3, name="CMP1", descr="Timer x Compare 1"),
            Bits(bits=2, name="PER", descr="Timer x Period"),
            Bits(bits=1, name="RESYNC", descr="Timer A resynchronization"),
            Bits(bits=0, name="SST", descr="Software Set trigger"),
        ]
        self.append(
            MmapReg(
                name=f"HRTIM_SET{x}1R",
                addr=(base_timer + 0x3C),
                descr=f"HRTIM Timer{x} Output1 Set Register",
                bits=output_set_reset_bits,
            )
        )
        self.append(
            MmapReg(
                name=f"HRTIM_RST{x}1R",
                addr=(base_timer + 0x40),
                descr=f"HRTIM Timer{x} Output1 Reset Register",
                bits=output_set_reset_bits,
            )
        )
        self.append(
            MmapReg(
                name=f"HRTIM_SET{x}2R",
                addr=(base_timer + 0x44),
                descr=f"HRTIM Timer{x} Output2 Set Register",
                bits=output_set_reset_bits,
            )
        )
        self.append(
            MmapReg(
                name=f"HRTIM_RST{x}2R",
                addr=(base_timer + 0x48),
                descr=f"HRTIM Timer{x} Output2 Reset Register",
                bits=output_set_reset_bits,
            )
        )
        # ------------------------------------------------------------------------------------------
