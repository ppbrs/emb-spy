""" Module for class RegistersSTM32H743."""
# Disabling line-too-long because it's impossible to keep
# human-readable register and bit descriptions short.
# pylint: disable=line-too-long


from emb_spy.mmreg.registers_if import Register, Registers, RegisterBits  # pylint: disable=import-error
from emb_spy.mmreg.arm.armv6_m.mmreg_armv6_m import MmregARMV6M  # pylint: disable=import-error
from emb_spy.mmreg.arm.stm32 import MmregSTM32  # pylint: disable=import-error


class MmregSTM32F051(Registers):
    """ Generates Register objects for all peripherals of STM32H743.
    """
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
    RCC_BASE = 0x40021000
    DMA2_BASE = 0x40020400
    DMA_BASE = 0x40020000

    # APB
    DBGMCU_BASE = 0x40015800
    TIM17_BASE = 0x40014800
    TIM16_BASE = 0x40014400
    TIM15_BASE = 0x40014000
    USART1_BASE = 0x40013800
    SPI1_I2S1_BASE = 0x40013000
    TIM1_BASE = 0x40012C00
    ADC_BASE = 0x40012400
    USART8_BASE = 0x40011C00
    USART7_BASE = 0x40011800
    USART6_BASE = 0x40011400
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
    USART5_BASE = 0x40005000
    USART4_BASE = 0x40004C00
    USART3_BASE = 0x40004800
    USART2_BASE = 0x40004400
    SPI2_BASE = 0x40003800
    IWDG_BASE = 0x40003000
    WWDG_BASE = 0x40002C00
    RTC_BASE = 0x40002800
    TIM14_BASE = 0x40002000
    TIM7_BASE = 0x40001400
    TIM6_BASE = 0x40001000
    TIM3_BASE = 0x40000400
    TIM2_BASE = 0x40000000

    def __init__(self):
        self.regs = []
        self.regs += MmregARMV6M().get_list()

        self._init_gpio()
        self._init_rcc()
        self.regs += MmregSTM32.init_tim1_tim8(prefix="TIM1", base=self.TIM1_BASE)
        self._init_tim2_tim3(prefix="TIM2", base=self.TIM2_BASE)
        self._init_tim2_tim3(prefix="TIM3", base=self.TIM3_BASE)

    def _init_gpio(self):
        self.regs += MmregSTM32.init_gpio(prefix="GPIOA", base=self.GPIOA_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOB", base=self.GPIOB_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOC", base=self.GPIOC_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOD", base=self.GPIOD_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOE", base=self.GPIOE_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOF", base=self.GPIOF_BASE)

    def _init_rcc(self):

        self.regs += [
            Register(
                name="RCC_CR", addr=(self.RCC_BASE + 0x00), descr="Clock control register",
                register_bits=[
                    RegisterBits(bits=25, name="PLLRDY", descr="PLL clock ready flag", values={}),
                    RegisterBits(bits=24, name="PLLON", descr="PLL enable", values={}),
                    RegisterBits(bits=19, name="CSSON", descr="Clock security system enable", values={}),
                    RegisterBits(bits=18, name="HSEBYP", descr="HSE crystal oscillator bypass", values={}),
                    RegisterBits(bits=17, name="HSERDY", descr="HSE clock ready flag", values={}),
                    RegisterBits(bits=16, name="HSEON", descr="HSE clock enable", values={}),
                    RegisterBits(bits=range(8, 16), name="HSICAL", descr="HSI clock calibration", values={}),
                    RegisterBits(bits=range(3, 8), name="HSITRIM", descr="HSI clock trimming", values={}),
                    RegisterBits(bits=1, name="HSIRDY", descr="HSI clock ready flag", values={}),
                    RegisterBits(bits=0, name="HSION", descr="HSI clock enable", values={}),
                ]
            ),
            Register(
                name="RCC_CFGR", addr=(self.RCC_BASE + 0x04), descr="Clock configuration register",
                register_bits=[
                    RegisterBits(bits=range(24, 28), name="MCO", descr="Microcontroller clock output"),
                    RegisterBits(bits=range(18, 22), name="PLLMUL", descr="PLL multiplication factor", values={
                        0b0000: "PLL input clock x 2",
                        0b0001: "PLL input clock x 3",
                        0b0010: "PLL input clock x 4",
                        0b0011: "PLL input clock x 5",
                        0b0100: "PLL input clock x 6",
                        0b0101: "PLL input clock x 7",
                        0b0110: "PLL input clock x 8",
                        0b0111: "PLL input clock x 9",
                        0b1000: "PLL input clock x 10",
                        0b1001: "PLL input clock x 11",
                        0b1010: "PLL input clock x 12",
                        0b1011: "PLL input clock x 13",
                        0b1100: "PLL input clock x 14",
                        0b1101: "PLL input clock x 15",
                        0b1110: "PLL input clock x 16",
                        0b1111: "PLL input clock x 16", }),
                    RegisterBits(bits=17, name="PLLXTPRE", descr="HSE divider for PLL input clock"),
                    RegisterBits(bits=[15, 16], name="PLLSRC", descr="PLL input clock source", values={
                        0b00: "HSI/2 selected as PLL input clock",
                        0b01: "HSI/PREDIV selected as PLL input clock",
                        0b10: "HSE/PREDIV selected as PLL input clock",
                        0b11: "HSI48/PREDIV selected as PLL input clock", }),
                    RegisterBits(bits=14, name="ADCPRE", descr="ADC prescaler"),
                    RegisterBits(bits=range(8, 11), name="PPRE", descr="PCLK prescaler"),
                    RegisterBits(bits=range(4, 8), name="HPRE", descr="HCLK prescaler"),
                    RegisterBits(bits=[2, 3], name="SWS", descr="System clock switch status", values={
                        0b00: "HSI used as system clock",
                        0b01: "HSE used as system clock",
                        0b10: "PLL used as system clock",
                        0b11: "HSI48 used as system clock (when available)", }),
                    RegisterBits(bits=[0, 1], name="SW", descr="System clock switch", values={
                        0b00: "HSI selected as system clock",
                        0b01: "HSE selected as system clock",
                        0b10: "PLL selected as system clock",
                        0b11: "HSI48 selected as system clock (when available)", }),
                ]
            ),
            Register(
                name="RCC_AHBENR", addr=(self.RCC_BASE + 0x14), descr="AHB peripheral clock enable register",
                register_bits=[
                    RegisterBits(bits=24, name="TSCEN", descr="Touch sensing controller clock enable"),
                    RegisterBits(bits=22, name="IOPFEN", descr="I/O port F clock enable"),
                    RegisterBits(bits=21, name="IOPEEN", descr="I/O port E clock enable"),
                    RegisterBits(bits=20, name="IOPDEN", descr="I/O port D clock enable"),
                    RegisterBits(bits=19, name="IOPCEN", descr="I/O port C clock enable"),
                    RegisterBits(bits=18, name="IOPBEN", descr="I/O port B clock enable"),
                    RegisterBits(bits=17, name="IOPAEN", descr="I/O port A clock enable"),
                    RegisterBits(bits=6, name="CRCEN", descr="CRC clock enable"),
                    RegisterBits(bits=4, name="FLITFEN", descr="FLITF clock enable"),
                    RegisterBits(bits=2, name="SRAMEN", descr="SRAM interface clock enable"),
                    RegisterBits(bits=1, name="DMA2EN", descr="DMA2 clock enable"),
                    RegisterBits(bits=0, name="DMAEN", descr="DMA clock enable"),
                ]
            ),
            Register(
                name="RCC_APB2ENR", addr=(self.RCC_BASE + 0x18), descr="APB peripheral clock enable register 2",
                register_bits=[
                ]
            ),
            Register(
                name="RCC_APB1ENR", addr=(self.RCC_BASE + 0x1C), descr="APB peripheral clock enable register 1",
                register_bits=[
                    RegisterBits(bits=30, name="CECEN", descr="HDMI CEC clock enable"),
                    RegisterBits(bits=29, name="DACEN", descr="DAC interface clock enable"),
                    RegisterBits(bits=28, name="PWREN", descr="Power interface clock enable"),
                    RegisterBits(bits=27, name="CRSEN", descr="Clock recovery system interface clock enable"),
                    RegisterBits(bits=25, name="CANEN", descr="CAN interface clock enable"),
                    RegisterBits(bits=23, name="USBEN", descr="USB interface clock enable"),
                    RegisterBits(bits=22, name="I2C2EN", descr="I2C2 clock enable"),
                    RegisterBits(bits=21, name="I2C1EN", descr="I2C1 clock enable"),
                    RegisterBits(bits=20, name="USART5EN", descr="USART5 clock enable"),
                    RegisterBits(bits=19, name="USART4EN", descr="USART4 clock enable"),
                    RegisterBits(bits=18, name="USART3EN", descr="USART3 clock enable"),
                    RegisterBits(bits=17, name="USART2EN", descr="USART2 clock enable"),
                    RegisterBits(bits=14, name="SPI2EN", descr="SPI2 clock enable"),
                    RegisterBits(bits=11, name="WWDGEN", descr="Window watchdog clock enable"),
                    RegisterBits(bits=8, name="TIM14EN", descr="TIM14 timer clock enable"),
                    RegisterBits(bits=5, name="TIM7EN", descr="TIM7 timer clock enable"),
                    RegisterBits(bits=4, name="TIM6EN", descr="TIM6 timer clock enable"),
                    RegisterBits(bits=1, name="TIM3EN", descr="TIM3 timer clock enable"),
                    RegisterBits(bits=0, name="TIM2EN", descr="TIM2 timer clock enable"),
                ]
            ),
        ]

    def _init_tim2_tim3(self, prefix: str, base: int) -> None:

        self.regs += [
            Register(
                name=prefix + "_CNT", addr=(base + 0x24), descr=f"{prefix} counter",
            ),
            Register(
                name=prefix + "_PSC", addr=(base + 0x28), descr=f"{prefix} counter",
            ),
            Register(
                name=prefix + "_ARR", addr=(base + 0x2C), descr=f"{prefix} counter",
            ),
            Register(
                name=prefix + "_CCR1", addr=(base + 0x34), descr=f"{prefix} counter",
            ),
            Register(
                name=prefix + "_CCR2", addr=(base + 0x38), descr=f"{prefix} counter",
            ),
            Register(
                name=prefix + "_CCR3", addr=(base + 0x3C), descr=f"{prefix} counter",
            ),
            Register(
                name=prefix + "_CCR4", addr=(base + 0x40), descr=f"{prefix} counter",
            ),
        ]
