"""Local module for STM32H743 general purpose timers 2, 3, 4, and 5."""
# Disabling line-too-long because it's impossible to keep human-readable descriptions short.
# pylint: disable=line-too-long

from emb_spy.mmreg.registers_if import Register, Registers  # pylint: disable=import-error


class _Tim2Tim3Tim4Tim5(Registers):

    TIM2_BASE = 0x40000000
    TIM3_BASE = 0x40000400
    TIM4_BASE = 0x40000800
    TIM5_BASE = 0x40000C00

    def __init__(self):
        self.regs = []

        for pref, base in zip(["TIM2_", "TIM3_", "TIM4_", "TIM5_"],
                              [self.TIM2_BASE, self.TIM3_BASE, self.TIM4_BASE, self.TIM5_BASE]):
            self.regs += [
                Register(name=(pref + "CR1"), addr=(base + 0x00), descr="TIMx control register 1", register_bits=[]),
                Register(name=(pref + "CR2"), addr=(base + 0x04), descr="TIMx control register 2", register_bits=[]),
                Register(name=(pref + "SMCR"), addr=(base + 0x08), descr="TIMx slave mode control register", register_bits=[]),
                Register(name=(pref + "DIER"), addr=(base + 0x0C), descr="TIMx DMA/Interrupt enable register", register_bits=[]),
                Register(name=(pref + "SR"), addr=(base + 0x10), descr="TIMx status register", register_bits=[]),
                Register(name=(pref + "EGR"), addr=(base + 0x14), descr="TIMx event generation register", register_bits=[]),
                Register(name=(pref + "CCMR1"), addr=(base + 0x18), descr="TIMx capture/compare mode register 1", register_bits=[]),
                Register(name=(pref + "CCMR2"), addr=(base + 0x1C), descr="TIMx capture/compare mode register 2", register_bits=[]),
                Register(name=(pref + "CNT"), addr=(base + 0x24), descr="TIMx counter", register_bits=[]),
                Register(name=(pref + "PSC"), addr=(base + 0x28), descr="TIMx prescaler", register_bits=[]),
                Register(name=(pref + "ARR"), addr=(base + 0x2C), descr="TIMx auto-reload register", register_bits=[]),
                Register(name=(pref + "CCR1"), addr=(base + 0x34), descr="TIMx capture/compare register 1", register_bits=[]),
                Register(name=(pref + "CCR2"), addr=(base + 0x38), descr="TIMx capture/compare register 2", register_bits=[]),
                Register(name=(pref + "CCR3"), addr=(base + 0x3C), descr="TIMx capture/compare register 3", register_bits=[]),
                Register(name=(pref + "CCR4"), addr=(base + 0x40), descr="TIMx capture/compare register 4", register_bits=[]),
                Register(name=(pref + "DCR"), addr=(base + 0x48), descr="TIMx DMA control register", register_bits=[]),
                Register(name=(pref + "DMAR"), addr=(base + 0x4C), descr="TIMx DMA address for full transfer", register_bits=[]),
                Register(name=(pref + "AF1"), addr=(base + 0x60), descr="TIM2 alternate function option register 1", register_bits=[]),
                Register(name=(pref + "TISEL"), addr=(base + 0x68), descr="TIM2 timer input selection register", register_bits=[]),
            ]
