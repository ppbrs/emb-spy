""" Module for class MmregSTM32F745."""
from emb_spy.mmreg.arm.armv7e_m import MmregARMV7EM  # pylint: disable=import-error
from emb_spy.mmreg.registers_if import Register, Registers, RegisterBits  # pylint: disable=import-error
from emb_spy.mmreg.arm.stm32 import MmregSTM32  # pylint: disable=import-error


class MmregSTM32F745(Registers):
    """
    Generates Register objects for all peripherals of STM32H743.
    """
    GPIOA_BASE = 0x40020000
    GPIOB_BASE = 0x40020400
    GPIOC_BASE = 0x40020800
    GPIOD_BASE = 0x40020C00
    GPIOE_BASE = 0x40021000
    GPIOF_BASE = 0x40021400
    GPIOG_BASE = 0x40021800
    GPIOH_BASE = 0x40021C00
    GPIOI_BASE = 0x40022000
    GPIOJ_BASE = 0x40022400
    GPIOK_BASE = 0x40022800
    TIM1_BASE = 0x40010000
    TIM8_BASE = 0x40010400

    def __init__(self):
        self.regs = []
        self.regs += MmregARMV7EM().get_list()

        self._init_gpio()
        self.regs += MmregSTM32.init_tim1_tim8(prefix="TIM1", base=self.TIM1_BASE)
        self.regs += MmregSTM32.init_tim1_tim8(prefix="TIM8", base=self.TIM8_BASE)

    def _init_gpio(self):
        self.regs += MmregSTM32.init_gpio(prefix="GPIOA", base=self.GPIOA_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOB", base=self.GPIOB_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOC", base=self.GPIOC_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOD", base=self.GPIOD_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOE", base=self.GPIOE_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOF", base=self.GPIOF_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOG", base=self.GPIOG_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOH", base=self.GPIOH_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOI", base=self.GPIOI_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOJ", base=self.GPIOJ_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOK", base=self.GPIOK_BASE)
