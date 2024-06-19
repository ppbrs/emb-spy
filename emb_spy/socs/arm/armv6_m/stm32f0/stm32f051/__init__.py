"""Module for STM32F051 SoC."""
from emb_spy.socs.arm.armv6_m import ARMV6M
from emb_spy.socs.arm.armv6_m.stm32f0.stm32f051._rcc import init_rcc
from emb_spy.socs.arm.armv6_m.stm32f0.stm32f051._tim2_tim3 import \
    init_tim2_tim3
from emb_spy.socs.arm.armv6_m.stm32f0.stm32f051._usart import init_usart
from emb_spy.socs.arm.stm32._gpio import init_gpio
from emb_spy.socs.arm.stm32._tim1_tim8 import init_tim1_tim8
from emb_spy.socs.soc import SoC


class STM32F051(SoC):
    """Generates Register objects for all peripherals of STM32F051."""

    # AHB2
    GPIOF_BASE = 0x48001400
    GPIOE_BASE = 0x48001000
    GPIOD_BASE = 0x48000C00
    GPIOC_BASE = 0x48000800
    GPIOB_BASE = 0x48000400
    GPIOA_BASE = 0x48000000

    # AHB1
    TSC_BASE = 0x40024000
    CRC_BASE = 0x40023000
    FLASH_INTERFACE_BASE = 0x40022000
    DMA2_BASE = 0x40020400
    DMA_BASE = 0x40020000

    # APB
    DBGMCU_BASE = 0x40015800
    TIM17_BASE = 0x40014800
    TIM16_BASE = 0x40014400
    TIM15_BASE = 0x40014000
    SPI1_I2S1_BASE = 0x40013000
    TIM1_BASE = 0x40012C00
    ADC_BASE = 0x40012400
    EXTI_BASE = 0x40010400
    SYSCFG_COMP_BASE = 0x40010000
    CEC_BASE = 0x40007800
    DAC_BASE = 0x40007400
    PWR_BASE = 0x40007000
    CRS_BASE = 0x40006C00
    CAN_BASE = 0x40006400
    USB_CAN_SRAM_BASE = 0x40006000
    USB_BASE = 0x40005C00
    I2C2_BASE = 0x40005800
    I2C1_BASE = 0x40005400
    SPI2_BASE = 0x40003800
    IWDG_BASE = 0x40003000
    WWDG_BASE = 0x40002C00
    RTC_BASE = 0x40002800
    TIM14_BASE = 0x40002000
    TIM7_BASE = 0x40001400
    TIM6_BASE = 0x40001000
    TIM3_BASE = 0x40000400
    TIM2_BASE = 0x40000000

    def __init__(self) -> None:
        """Generate all Register objects."""
        super().__init__()
        self += ARMV6M().regs

        self._init_gpio()
        init_rcc(self)
        init_tim1_tim8(self, prefix="TIM1", base=self.TIM1_BASE)
        init_tim2_tim3(self, prefix="TIM2", base=self.TIM2_BASE)
        init_tim2_tim3(self, prefix="TIM3", base=self.TIM3_BASE)
        init_usart(self)

    def _init_gpio(self) -> None:
        init_gpio(self, prefix="GPIOA", base=self.GPIOA_BASE)
        init_gpio(self, prefix="GPIOB", base=self.GPIOB_BASE)
        init_gpio(self, prefix="GPIOC", base=self.GPIOC_BASE)
        init_gpio(self, prefix="GPIOD", base=self.GPIOD_BASE)
        init_gpio(self, prefix="GPIOF", base=self.GPIOF_BASE)
