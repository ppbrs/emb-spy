"""Part of STM32H743 SoC."""

from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC
from emb_spy.socs.bits import Bits


def init_tim6_tim7(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"

    tim6_base = 0x40001000
    tim7_base = 0x40001400

    for pref, base in zip(["TIM6_", "TIM7_"], [tim6_base, tim7_base]):
        self.append(
            MmapReg(
                name=(pref + "CR1"),
                addr=(base + 0x00),
                descr="TIMx control register 1",
                bits=[
                    Bits(bits=0, name="CEN", descr="Counter enable"),
                    Bits(bits=1, name="UDIS", descr="Update disable"),
                    Bits(bits=2, name="URS", descr="Update request source"),
                    Bits(bits=3, name="OPM", descr="One-pulse mode"),
                ],
            )
        )
        self.append(
            MmapReg(
                name=(pref + "CR2"),
                addr=(base + 0x04),
                descr="TIMx control register 2",
                bits=[
                    Bits(bits=range(4, 7), name="MMS", descr="Master mode selection"),
                ],
            )
        )
        self.append(
            MmapReg(
                name=(pref + "DIER"),
                addr=(base + 0x0C),
                descr="TIMx DMA/Interrupt enable register",
                bits=[
                    Bits(bits=8, name="UDE", descr="Update DMA request enable"),
                    Bits(bits=0, name="UIE", descr="Update interrupt enable"),
                ],
            )
        )
        self.append(
            MmapReg(
                name=(pref + "SR"),
                addr=(base + 0x10),
                descr="TIMx status register",
                bits=[
                    Bits(bits=0, name="UIF", descr="Update interrupt flag"),
                ],
            )
        )
        self.append(
            MmapReg(
                name=(pref + "EGR"),
                addr=(base + 0x14),
                descr="TIMx event generation register",
                bits=[
                    Bits(bits=0, name="UG", descr="Update generation"),
                ],
            )
        )
        self.append(
            MmapReg(
                name=(pref + "ARR"),
                addr=(base + 0x2C),
                descr="TIMx auto-reload register",
                bits=[
                    Bits(bits=range(0, 16), name="ARR", descr="Prescaler value"),
                ],
            )
        )
        self.append(
            MmapReg(
                name=(pref + "CNT"),
                addr=(base + 0x24),
                descr="TIMx counter",
                bits=[
                    Bits(bits=31, name="UIFCPY", descr="UIF Copy"),
                    Bits(bits=range(0, 16), name="CNT", descr="Counter value"),
                ],
            )
        )
        self.append(
            MmapReg(
                name=(pref + "PSC"),
                addr=(base + 0x28),
                descr="TIMx prescaler",
                bits=[
                    Bits(bits=range(0, 16), name="PSC", descr="Prescaler value"),
                ],
            )
        )
