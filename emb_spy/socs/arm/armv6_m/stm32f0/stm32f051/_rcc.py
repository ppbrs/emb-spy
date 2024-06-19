"""Part of STM32F051 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_rcc(self: SoC):
    """Generate Register objects for RCC peripheral."""
    assert self.__class__.__name__ == "STM32F051"

    base = 0x40021000
    self += [
        MmapReg(
            name="RCC_CR", addr=(base + 0x00), descr="Clock control register",
            bits=[
                Bits(bits=25, name="PLLRDY", descr="PLL clock ready flag"),
                Bits(bits=24, name="PLLON", descr="PLL enable"),
                Bits(bits=19, name="CSSON", descr="Clock security system enable"),
                Bits(bits=18, name="HSEBYP", descr="HSE crystal oscillator bypass"),
                Bits(bits=17, name="HSERDY", descr="HSE clock ready flag"),
                Bits(bits=16, name="HSEON", descr="HSE clock enable"),
                Bits(bits=range(8, 16), name="HSICAL", descr="HSI clock calibration"),
                Bits(bits=range(3, 8), name="HSITRIM", descr="HSI clock trimming"),
                Bits(bits=1, name="HSIRDY", descr="HSI clock ready flag"),
                Bits(bits=0, name="HSION", descr="HSI clock enable"),
            ]
        ),
        MmapReg(
            name="RCC_CFGR", addr=(base + 0x04), descr="Clock configuration register",
            bits=[
                Bits(bits=range(24, 28), name="MCO", descr="Microcontroller clock output"),
                Bits(bits=range(18, 22), name="PLLMUL", descr="PLL multiplication factor",
                     descr_vals={
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
                Bits(bits=17, name="PLLXTPRE", descr="HSE divider for PLL input clock"),
                Bits(bits=[15, 16], name="PLLSRC", descr="PLL input clock source", descr_vals={
                    0b00: "HSI/2 selected as PLL input clock",
                    0b01: "HSI/PREDIV selected as PLL input clock",
                    0b10: "HSE/PREDIV selected as PLL input clock",
                    0b11: "HSI48/PREDIV selected as PLL input clock", }),
                Bits(bits=14, name="ADCPRE", descr="ADC prescaler"),
                Bits(bits=range(8, 11), name="PPRE", descr="PCLK prescaler"),
                Bits(bits=range(4, 8), name="HPRE", descr="HCLK prescaler"),
                Bits(bits=[2, 3], name="SWS", descr="System clock switch status", descr_vals={
                    0b00: "HSI used as system clock",
                    0b01: "HSE used as system clock",
                    0b10: "PLL used as system clock",
                    0b11: "HSI48 used as system clock (when available)", }),
                Bits(bits=[0, 1], name="SW", descr="System clock switch", descr_vals={
                    0b00: "HSI selected as system clock",
                    0b01: "HSE selected as system clock",
                    0b10: "PLL selected as system clock",
                    0b11: "HSI48 selected as system clock (when available)", }),
            ]
        ),
        MmapReg(
            name="RCC_AHBENR", addr=(base + 0x14),
            descr="AHB peripheral clock enable register",
            bits=[
                Bits(bits=24, name="TSCEN", descr="Touch sensing controller clock enable"),
                Bits(bits=22, name="IOPFEN", descr="I/O port F clock enable"),
                Bits(bits=21, name="IOPEEN", descr="I/O port E clock enable"),
                Bits(bits=20, name="IOPDEN", descr="I/O port D clock enable"),
                Bits(bits=19, name="IOPCEN", descr="I/O port C clock enable"),
                Bits(bits=18, name="IOPBEN", descr="I/O port B clock enable"),
                Bits(bits=17, name="IOPAEN", descr="I/O port A clock enable"),
                Bits(bits=6, name="CRCEN", descr="CRC clock enable"),
                Bits(bits=4, name="FLITFEN", descr="FLITF clock enable"),
                Bits(bits=2, name="SRAMEN", descr="SRAM interface clock enable"),
                Bits(bits=1, name="DMA2EN", descr="DMA2 clock enable"),
                Bits(bits=0, name="DMAEN", descr="DMA clock enable"),
            ]
        ),
        MmapReg(
            name="RCC_APB2ENR", addr=(base + 0x18),
            descr="APB peripheral clock enable register 2",
            bits=[
                Bits(bits=22, name="DBGMCUEN", descr="MCU debug module clock enable"),
                Bits(bits=18, name="TIM17EN", descr="TIM17 timer clock enable"),
                Bits(bits=17, name="TIM16EN", descr="TIM16 timer clock enable"),
                Bits(bits=16, name="TIM15EN", descr="TIM15 timer clock enable"),
                Bits(bits=14, name="USART1EN", descr="USART1 clock enable"),
                Bits(bits=12, name="SPI1EN", descr="SPI1 clock enable"),
                Bits(bits=11, name="TIM1EN", descr="TIM1 timer clock enable"),
                Bits(bits=9, name="ADCEN", descr="ADC interface clock enable"),
                Bits(bits=7, name="USART8EN", descr="USART8 clock enable"),
                Bits(bits=6, name="USART7EN", descr="USART7 clock enable"),
                Bits(bits=5, name="USART6EN", descr="USART6 clock enable"),
                Bits(bits=0, name="SYSCFGCOMPEN", descr="SYSCFG & COMP clock enable"),
            ]
        ),
        MmapReg(
            name="RCC_APB1ENR", addr=(base + 0x1C),
            descr="APB peripheral clock enable register 1",
            bits=[
                Bits(bits=30, name="CECEN", descr="HDMI CEC clock enable"),
                Bits(bits=29, name="DACEN", descr="DAC interface clock enable"),
                Bits(bits=28, name="PWREN", descr="Power interface clock enable"),
                Bits(bits=27, name="CRSEN",
                     descr="Clock recovery system interface clock enable"),
                Bits(bits=25, name="CANEN", descr="CAN interface clock enable"),
                Bits(bits=23, name="USBEN", descr="USB interface clock enable"),
                Bits(bits=22, name="I2C2EN", descr="I2C2 clock enable"),
                Bits(bits=21, name="I2C1EN", descr="I2C1 clock enable"),
                Bits(bits=20, name="USART5EN", descr="USART5 clock enable"),
                Bits(bits=19, name="USART4EN", descr="USART4 clock enable"),
                Bits(bits=18, name="USART3EN", descr="USART3 clock enable"),
                Bits(bits=17, name="USART2EN", descr="USART2 clock enable"),
                Bits(bits=14, name="SPI2EN", descr="SPI2 clock enable"),
                Bits(bits=11, name="WWDGEN", descr="Window watchdog clock enable"),
                Bits(bits=8, name="TIM14EN", descr="TIM14 timer clock enable"),
                Bits(bits=5, name="TIM7EN", descr="TIM7 timer clock enable"),
                Bits(bits=4, name="TIM6EN", descr="TIM6 timer clock enable"),
                Bits(bits=1, name="TIM3EN", descr="TIM3 timer clock enable"),
                Bits(bits=0, name="TIM2EN", descr="TIM2 timer clock enable"),
            ]
        ),
        MmapReg(
            name="RCC_APB2RSTR", addr=(base + 0x0C),
            descr="APB peripheral reset register 2",
            bits=[
                Bits(bits=22, name="DBGMCURST", descr="Debug MCU reset"),
                Bits(bits=18, name="TIM17RST", descr="TIM17 timer reset"),
                Bits(bits=17, name="TIM16RST", descr="TIM16 timer reset"),
                Bits(bits=16, name="TIM15RST", descr="TIM15 timer reset"),
                Bits(bits=14, name="USART1RST", descr="USART1 reset"),
                Bits(bits=12, name="SPI1RST", descr="SPI1 reset"),
                Bits(bits=11, name="TIM1RST", descr="TIM1 timer reset"),
                Bits(bits=9, name="ADCRST", descr="ADC interface reset"),
                Bits(bits=7, name="USART8RST", descr="USART8 reset"),
                Bits(bits=6, name="USART7RST", descr="USART7 reset"),
                Bits(bits=5, name="USART6RST", descr="USART6 reset"),
                Bits(bits=0, name="SYSCFGRST", descr="SYSCFG reset"),
            ],
        ),
        MmapReg(
            name="RCC_APB1RSTR", addr=(base + 0x10),
            descr="APB peripheral reset register 1",
            bits=[
                Bits(bits=30, name="CECRST", descr="HDMI CEC reset"),
                Bits(bits=29, name="DACRST", descr="DAC interface reset"),
                Bits(bits=28, name="PWRRST", descr="Power interface reset"),
                Bits(bits=27, name="CRSRST", descr="Clock recovery system interface reset"),
                Bits(bits=25, name="CANRST", descr="CAN interface reset"),
                Bits(bits=23, name="USBRST", descr="USB interface reset"),
                Bits(bits=22, name="I2C2RST", descr="I2C2 reset"),
                Bits(bits=21, name="I2C1RST", descr="I2C1 reset"),
                Bits(bits=20, name="USART5RST", descr="USART5 reset"),
                Bits(bits=19, name="USART4RST", descr="USART4 reset"),
                Bits(bits=18, name="USART3RST", descr="USART3 reset"),
                Bits(bits=17, name="USART2RST", descr="USART2 reset"),
                Bits(bits=14, name="SPI2RST", descr="SPI2 reset"),
                Bits(bits=11, name="WWDGRST", descr="Window watchdog reset"),
                Bits(bits=8, name="TIM14RST", descr="TIM14 timer reset"),
                Bits(bits=5, name="TIM7RST", descr="TIM7 timer reset"),
                Bits(bits=4, name="TIM6RST", descr="TIM6 timer reset"),
                Bits(bits=1, name="TIM3RST", descr="TIM3 timer reset"),
                Bits(bits=0, name="TIM2RST", descr="TIM2 timer reset"),
            ],
        ),
        MmapReg(
            name="RCC_AHBRSTR", addr=(base + 0x28), descr="AHB peripheral reset register",
            bits=[
                Bits(bits=24, name="TSCRST", descr="Touch sensing controller reset"),
                Bits(bits=22, name="IOPFRST", descr="I/O port F reset"),
                Bits(bits=21, name="IOPERST", descr="I/O port E reset"),
                Bits(bits=20, name="IOPDRST", descr="I/O port D reset"),
                Bits(bits=19, name="IOPCRST", descr="I/O port C reset"),
                Bits(bits=18, name="IOPBRST", descr="I/O port B reset"),
                Bits(bits=17, name="IOPARST", descr="I/O port A reset"),
            ],
        ),
        MmapReg(
            name="RCC_CFGR2", addr=(base + 0x2C), descr="Clock configuration register 2",
            bits=[],
        ),
        MmapReg(
            name="RCC_CFGR3", addr=(base + 0x30), descr="Clock configuration register 3",
            bits=[],
        ),
        MmapReg(
            name="RCC_CR2", addr=(base + 0x34), descr="Clock control register 2",
            bits=[],
        ),
    ]
