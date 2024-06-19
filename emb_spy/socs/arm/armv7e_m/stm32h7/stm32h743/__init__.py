"""Module for STM32H743 SoC."""
from emb_spy.socs.arm.armv7e_m import ARMV7EM
from emb_spy.socs.arm.stm32._gpio import init_gpio
from emb_spy.socs.arm.stm32._tim1_tim8 import init_tim1_tim8
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC

from ._adc import init_adc
from ._bdma import init_bdma
from ._dac import init_dac
from ._dma import init_dma
from ._dma_mux import init_dma_mux
from ._i2c import init_i2c
from ._mdma import init_mdma
from ._pwr import init_pwr
from ._quadspi import init_quadspi
from ._rcc import init_rcc
from ._syscfg import init_syscfg
from ._system_flash import init_system_flash
from ._tim2_tim3_tim4_tim5 import init_tim2_tim3_tim4_tim5
from ._hrtim import init_hrtim


class STM32H743(SoC):
    """Generates Register objects for all peripherals of STM32H743."""

    FLASH_BASE = 0x52002000
    GPIOA_BASE = 0x58020000
    GPIOB_BASE = 0x58020400
    GPIOC_BASE = 0x58020800
    GPIOD_BASE = 0x58020C00
    GPIOE_BASE = 0x58021000
    GPIOF_BASE = 0x58021400
    GPIOG_BASE = 0x58021800
    GPIOH_BASE = 0x58021C00
    GPIOI_BASE = 0x58022000
    GPIOJ_BASE = 0x58022400
    GPIOK_BASE = 0x58022800
    I2C1_BASE = 0x40005400
    I2C2_BASE = 0x40005800
    I2C3_BASE = 0x40005C00
    I2C4_BASE = 0x58001C00
    TIM1_BASE = 0x40010000
    TIM8_BASE = 0x40010400

    def __init__(self):
        """Generate all Register objects."""
        super().__init__()
        self += ARMV7EM().regs
        init_adc(self)
        init_bdma(self)
        init_dac(self)
        init_dma(self)
        init_dma_mux(self)
        init_hrtim(self)
        init_i2c(self)
        init_mdma(self)
        init_pwr(self)
        init_quadspi(self)
        init_rcc(self)
        init_syscfg(self)
        init_system_flash(self)
        init_tim1_tim8(self, prefix="TIM1", base=self.TIM1_BASE)
        init_tim1_tim8(self, prefix="TIM8", base=self.TIM8_BASE)
        init_tim2_tim3_tim4_tim5(self)
        self._init_flash()
        self._init_gpio()

    def _init_flash(self):
        self += [
            MmapReg(
                name="FLASH_OPTSR_CUR", addr=(self.FLASH_BASE + 0x01C),
                descr="Reflects the current values of corresponding option bits",
                comment="These bits reflects the power level that generates a system reset",
                bits=[
                    Bits(
                        bits=range(2, 4), name="BOR_LEV", descr="Brownout level option status bit",
                        descr_vals={
                            0b00: "VBOR0, brownout reset threshold 0 (1.67..1.62 V)",
                            0b01: "VBOR1, brownout reset threshold 1 (2.10..2.00 V)",
                            0b10: "VBOR2, brownout reset threshold 2 (2.41..2.31 V)",
                            0b11: "VBOR3, brownout reset threshold 3 (2.70..2.61 V)",
                        }),
                ]),
        ]

    def _init_gpio(self):
        init_gpio(self, prefix="GPIOA", base=self.GPIOA_BASE)
        init_gpio(self, prefix="GPIOB", base=self.GPIOB_BASE)
        init_gpio(self, prefix="GPIOC", base=self.GPIOC_BASE)
        init_gpio(self, prefix="GPIOD", base=self.GPIOD_BASE)
        init_gpio(self, prefix="GPIOE", base=self.GPIOE_BASE)
        init_gpio(self, prefix="GPIOF", base=self.GPIOF_BASE)
        init_gpio(self, prefix="GPIOG", base=self.GPIOG_BASE)
        init_gpio(self, prefix="GPIOH", base=self.GPIOH_BASE)
        init_gpio(self, prefix="GPIOI", base=self.GPIOI_BASE)
        init_gpio(self, prefix="GPIOJ", base=self.GPIOJ_BASE)
        init_gpio(self, prefix="GPIOK", base=self.GPIOK_BASE)
