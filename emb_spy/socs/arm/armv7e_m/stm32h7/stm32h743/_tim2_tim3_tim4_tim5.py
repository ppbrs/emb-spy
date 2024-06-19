"""Part of STM32H743 SoC."""
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_tim2_tim3_tim4_tim5(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"

    tim2_base = 0x40000000
    tim3_base = 0x40000400
    tim4_base = 0x40000800
    tim5_base = 0x40000C00

    for pref, base in zip(["TIM2_", "TIM3_", "TIM4_", "TIM5_"],
                          [tim2_base, tim3_base, tim4_base, tim5_base]):
        self.append(MmapReg(
            name=(pref + "CR1"), addr=(base + 0x00), descr="TIMx control register 1", ))
        self.append(MmapReg(
            name=(pref + "CR2"), addr=(base + 0x04), descr="TIMx control register 2", ))
        self.append(MmapReg(
            name=(pref + "SMCR"), addr=(base + 0x08), descr="TIMx slave mode control register", ))
        self.append(MmapReg(
            name=(pref + "DIER"), addr=(base + 0x0C), descr="TIMx DMA/Interrupt enable register", ))
        self.append(MmapReg(
            name=(pref + "SR"), addr=(base + 0x10), descr="TIMx status register", ))
        self.append(MmapReg(
            name=(pref + "EGR"), addr=(base + 0x14), descr="TIMx event generation register", ))
        self.append(MmapReg(
            name=(pref + "CCMR1"),
            addr=(base + 0x18), descr="TIMx capture/compare mode register 1", ))
        self.append(MmapReg(
            name=(pref + "CCMR2"), addr=(base + 0x1C),
            descr="TIMx capture/compare mode register 2", ))
        self.append(MmapReg(
            name=(pref + "CNT"), addr=(base + 0x24), descr="TIMx counter", ))
        self.append(MmapReg(
            name=(pref + "PSC"), addr=(base + 0x28), descr="TIMx prescaler", ))
        self.append(MmapReg(
            name=(pref + "ARR"), addr=(base + 0x2C), descr="TIMx auto-reload register", ))
        self.append(MmapReg(
            name=(pref + "CCR1"), addr=(base + 0x34), descr="TIMx capture/compare register 1", ))
        self.append(MmapReg(
            name=(pref + "CCR2"), addr=(base + 0x38), descr="TIMx capture/compare register 2", ))
        self.append(MmapReg(
            name=(pref + "CCR3"), addr=(base + 0x3C), descr="TIMx capture/compare register 3", ))
        self.append(MmapReg(
            name=(pref + "CCR4"), addr=(base + 0x40), descr="TIMx capture/compare register 4", ))
        self.append(MmapReg(
            name=(pref + "DCR"), addr=(base + 0x48), descr="TIMx DMA control register", ))
        self.append(MmapReg(
            name=(pref + "DMAR"), addr=(base + 0x4C), descr="TIMx DMA address for full transfer", ))
        self.append(MmapReg(
            name=(pref + "AF1"), addr=(base + 0x60),
            descr="TIM2 alternate function option register 1", ))
        self.append(MmapReg(
            name=(pref + "TISEL"), addr=(base + 0x68),
            descr="TIM2 timer input selection register", ))
