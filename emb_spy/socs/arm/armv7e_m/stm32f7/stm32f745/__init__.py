"""Module for class STM32F745 SoC."""
from emb_spy.socs.arm.armv7e_m import ARMV7EM
from emb_spy.socs.arm.stm32._gpio import init_gpio
from emb_spy.socs.arm.stm32._tim1_tim8 import init_tim1_tim8
from emb_spy.socs.soc import SoC
from emb_spy.socs.arm.armv7e_m.stm32f7.stm32f745._rcc import init_rcc

# 0xA0001000 QuadSPI Control Register
# 0xA0000000 FMC control register
# 0x50060800 RNG
# 0x50060400 HASH
# 0x50060000 CRYP
# 0x50050000 DCMI
# 0x50000000 USB OTG FS
# 0x40040000 USB OTG HS
# 0x4002B000 Chrom-ART (DMA2D)
# 0x40028000 ETHERNET MAC
# 0x40026400 DMA2
# 0x40026000 DMA1
# 0x40024000 BKPSRAM
# 0x40023C00 Flash interface register
# 0x40023800 RCC
# 0x40023000 CRC
# 0x40016800 LCD-TFT
# 0x40015C00 SAI2
# 0x40015800 SAI1
# 0x40015400 SPI6
# 0x40015000 SPI5
# 0x40014800 TIM11
# 0x40014400 TIM10
# 0x40014000 TIM9
# 0x40013C00 EXTI
# 0x40013800 SYSCFG
# 0x40013400 SPI4
# 0x40013000 SPI1
# 0x40012C00 SDMMC1
# 0x40012000  ADC1 ADC2 ADC3
# 0x40011400 USART6
# 0x40011000 USART1
# 0x40010400 TIM8
# 0x40010000 TIM1
# 0x40007C00 UART8
# 0x40007800 UART7
# 0x40007400 DAC
# 0x40007000 PWR
# 0x40006C00 HDMI-CEC
# 0x40006800 CAN2
# 0x40006400 CAN1
# 0x40006000 I2C4
# 0x40005C00 I2C3
# 0x40005800 I2C2
# 0x40005400 I2C1
# 0x40005000 UART5
# 0x40004C00 UART4
# 0x40004800 USART3
# 0x40004400 USART2
# 0x40004000 SPDIFRX
# 0x40003C00 SPI3 / I2S3
# 0x40003800 SPI2 / I2S2
# 0x40003000 IWDG
# 0x40002C00 WWDG
# 0x40002800 RTC & BKP Registers
# 0x40002400 LPTIM1
# 0x40002000 TIM14
# 0x40001C00 TIM13
# 0x40001800 TIM12
# 0x40001400 TIM7
# 0x40001000 TIM6
# 0x40000C00 TIM5
# 0x40000800 TIM4
# 0x40000400 TIM3
# 0x40000000 TIM2


class STM32F745(SoC):
    """Generates Register objects for all peripherals of STM32F745."""

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
        """Generate all Register objects."""
        super().__init__()
        self.extend(ARMV7EM().regs)

        self.init_gpio()
        init_rcc(self)
        init_tim1_tim8(self, prefix="TIM1", base=self.TIM1_BASE)
        init_tim1_tim8(self, prefix="TIM8", base=self.TIM8_BASE)

    def init_gpio(self):
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
