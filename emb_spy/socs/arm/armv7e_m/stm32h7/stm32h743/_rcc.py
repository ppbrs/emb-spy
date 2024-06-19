"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_rcc(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"
    base = 0x58024400
    # ==============================================================================================
    self.append(MmapReg(
        name="RCC_CR", addr=(base + 0x000),
        descr="RCC source control register.",
        bits=[
            Bits(bits=29, name="PLL3RDY", descr="PLL3 clock ready flag",),
            Bits(bits=28, name="PLL3ON", descr="PLL3 enable",),
            Bits(bits=27, name="PLL2RDY", descr="PLL2 clock ready flag",),
            Bits(bits=26, name="PLL2ON", descr="PLL2 enable",),
            Bits(bits=25, name="PLL1RDY", descr="PLL1 clock ready flag",),
            Bits(bits=24, name="PLL1ON", descr="PLL1 enable",),
            Bits(bits=19, name="HSECSSON", descr="HSE Clock Security System enable",),
            Bits(bits=18, name="HSEBYP", descr="HSE clock bypass",),
            Bits(bits=17, name="HSERDY", descr="HSE clock ready flag",),
            Bits(bits=16, name="HSEON", descr="HSE clock enable",),
            Bits(bits=15, name="D2CKRDY", descr="D2 domain clocks ready flag",),
            Bits(bits=14, name="D1CKRDY", descr="D1 domain clocks ready flag",),
            Bits(bits=13, name="HSI48RDY", descr="HSI48 clock ready flag",),
            Bits(bits=12, name="HSI48ON", descr="HSI48 clock enable",),
            Bits(bits=9, name="CSIKERON", descr="CSI clock enable in Stop mode",),
            Bits(bits=8, name="CSIRDY", descr="CSI clock ready flag",),
            Bits(bits=7, name="CSION", descr="CSI clock enable",),
            Bits(bits=6, name="Reserved", descr="must be kept at reset value.",),
            Bits(bits=5, name="HSIDIVF", descr="HSI divider flag",),
            Bits(bits=range(3, 5), name="HSIDIV", descr="HSI clock divider",),
            Bits(bits=2, name="HSIRDY", descr="HSI clock ready flag",),
            Bits(bits=1, name="HSIKERON", descr="High Speed Internal clock enable in Stop mode",),
            Bits(bits=0, name="HSION", descr="High Speed Internal clock enable",),
        ]))
    self.append(MmapReg(
        name="RCC_CFGR", addr=(base + 0x010),
        descr="RCC clock configuration register.",
        bits=[
            Bits(bits=range(29, 32), name="MCO2", descr="Micro-controller clock output 2"),
            Bits(bits=range(25, 29), name="MCO2PRE", descr="MCO2 prescaler"),
            Bits(bits=range(22, 25), name="MCO1", descr="Micro-controller clock output 1"),
            Bits(bits=range(18, 22), name="MCO1PRE", descr="MCO1 prescaler"),
            Bits(bits=15, name="TIMPRE", descr="Timers clocks prescaler selection"),
            Bits(bits=14, name="HRTIMSEL", descr="High Resolution Timer clock prescaler selection"),
            # Bits 13:8 RTCPRE[5:0]: HSE division factor for RTC clock
            # Bit 7 STOPKERWUCK: Kernel clock selection after a wake up from system Stop
            # Bit 6 STOPWUCK: System clock selection after a wake up from system Stop
            Bits(bits=range(3, 6), name="SWS", descr="System clock switch status"),
            Bits(bits=range(0, 3), name="SW", descr="System clock switch"),
        ]))
    # ==============================================================================================
    self.append(MmapReg(
        name="RCC_D1CFGR", addr=(base + 0x018),
        descr="RCC domain 1 clock configuration register",
        bits=[
            Bits(bits=range(8, 12), name="D1CPRE", descr="D1 domain Core prescaler"),
            Bits(bits=range(4, 7), name="D1PPRE", descr="D1 domain APB3 prescaler"),
            Bits(bits=range(0, 4), name="HPRE", descr="D1 domain AHB prescaler"),
        ]))

    self.append(MmapReg(
        name="RCC_D2CFGR", addr=(base + 0x01C),
        descr="RCC domain 2 clock configuration register",
        bits=[
            Bits(bits=range(8, 11), name="D2PPRE2", descr="D2 domain APB2 prescaler"),
            Bits(bits=range(4, 7), name="D2PPRE1", descr="D2 domain APB1 prescaler"),
        ]))

    self.append(MmapReg(
        name="RCC_D3CFGR", addr=(base + 0x020),
        descr="RCC domain 3 clock configuration register",
        bits=[
            Bits(bits=range(4, 7), name="D3PPRE", descr="D3 domain APB4 prescaler"),
        ]))
    # ==============================================================================================
    self.append(MmapReg(
        name="RCC_PLLCKSELR", addr=(base + 0x028),
        descr="RCC PLL clock source selection register",
        bits=[
            Bits(bits=range(20, 26), name="DIVM3", descr="Prescaler for PLL3"),
            Bits(bits=range(12, 18), name="DIVM2", descr="Prescaler for PLL2"),
            Bits(bits=range(4, 10), name="DIVM1", descr="Prescaler for PLL1"),
            Bits(
                bits=range(0, 2), name="PLLSRC", descr="DIVMx and PLLs clock source selection",
                # 00: HSI selected as PLL clock (hsi_ck) (default after reset)
                # 01: CSI selected as PLL clock (csi_ck)
                # 10: HSE selected as PLL clock (hse_ck)
                # 11: No clock send to DIVMx divider and PLLs
            ),
        ]))

    self.append(MmapReg(
        name="RCC_PLLCFGR", addr=(base + 0x02C),
        descr="RCC PLL configuration register",
        bits=[
            Bits(bits=24, name="DIVR3EN", descr="PLL3 DIVR divider output enable"),
            Bits(bits=23, name="DIVQ3EN", descr="PLL3 DIVQ divider output enable"),
            Bits(bits=22, name="DIVP3EN", descr="PLL3 DIVP divider output enable"),
            Bits(bits=21, name="DIVR2EN", descr="PLL2 DIVR divider output enable"),
            Bits(bits=20, name="DIVQ2EN", descr="PLL2 DIVQ divider output enable"),
            Bits(bits=19, name="DIVP2EN", descr="PLL2 DIVP divider output enable"),
            Bits(bits=18, name="DIVR1EN", descr="PLL1 DIVR divider output enable"),
            Bits(bits=17, name="DIVQ1EN", descr="PLL1 DIVQ divider output enable"),
            Bits(bits=16, name="DIVP1EN", descr="PLL1 DIVP divider output enable"),
            Bits(bits=range(10, 12), name="PLL3RGE", descr="PLL3 input frequency range"),
            Bits(bits=9, name="PLL3VCOSEL", descr="PLL3 VCO selection"),
            Bits(bits=8, name="PLL3FRACEN", descr="PLL3 fractional latch enable"),
            Bits(bits=range(6, 8), name="PLL2RGE", descr="PLL2 input frequency range"),
            Bits(bits=5, name="PLL2VCOSEL", descr="PLL2 VCO selection"),
            Bits(bits=4, name="PLL2FRACEN", descr="PLL2 fractional latch enable"),
            Bits(bits=range(2, 4), name="PLL1RGE", descr="PLL1 input frequency range"),
            Bits(bits=1, name="PLL1VCOSEL", descr="PLL1 VCO selection"),
            Bits(bits=0, name="PLL1FRACEN", descr="PLL1 fractional latch enable"),
        ]))

    self.append(MmapReg(
        name="RCC_PLL1DIVR", addr=(base + 0x030),
        descr="RCC PLL1 dividers configuration register",
        bits=[
            Bits(bits=range(24, 31), name="DIVR1", descr="PLL1 DIVR division factor"),
            Bits(bits=range(16, 23), name="DIVQ1", descr="PLL1 DIVQ division factor"),
            Bits(bits=range(9, 16), name="DIVP1", descr="PLL1 DIVP division factor"),
            Bits(bits=range(0, 9), name="DIVN1", descr="Multiplication factor for PLL1 VCO"),
        ]))
    self.append(MmapReg(
        name="RCC_PLL1FRACR", addr=(base + 0x034),
        descr="RCC PLL1 fractional divider register",
        bits=[
            Bits(
                bits=range(3, 16), name="FRACN1",
                descr="Fractional part of the multiplication factor for PLL1 VCO"),
        ]))
    self.append(MmapReg(
        name="RCC_PLL2DIVR", addr=(base + 0x038),
        descr="RCC PLL2 divider configuration register",
        bits=[
            Bits(bits=range(24, 31), name="DIVR2", descr="PLL2 DIVR division factor"),
            Bits(bits=range(16, 23), name="DIVQ2", descr="PLL2 DIVQ division factor"),
            Bits(bits=range(9, 16), name="DIVP2", descr="PLL2 DIVP division factor"),
            Bits(bits=range(0, 9), name="DIVN2", descr="Multiplication factor for PLL2 VCO"),
        ]))
    self.append(MmapReg(
        name="RCC_PLL2FRACR", addr=(base + 0x03C),
        descr="RCC PLL2 fractional divider register",
        bits=[
            Bits(
                bits=range(3, 16), name="FRACN2",
                descr="Fractional part of the multiplication factor for PLL2 VCO"),
        ]))
    self.append(MmapReg(
        name="RCC_PLL3DIVR", addr=(base + 0x040),
        descr="RCC PLL3 divider configuration register",
        bits=[
            Bits(bits=range(24, 31), name="DIVR3", descr="PLL3 DIVR division factor"),
            Bits(bits=range(16, 23), name="DIVQ3", descr="PLL3 DIVQ division factor"),
            Bits(bits=range(9, 16), name="DIVP3", descr="PLL3 DIVP division factor"),
            Bits(bits=range(0, 9), name="DIVN3", descr="Multiplication factor for PLL3 VCO"),
        ]))
    self.append(MmapReg(
        name="RCC_PLL3FRACR", addr=(base + 0x044),
        descr="RCC PLL3 fractional divider register",
        bits=[
            Bits(
                bits=range(3, 16), name="FRACN3",
                descr="Fractional part of the multiplication factor for PLL3 VCO"),
        ]))
    # ==============================================================================================
    self.append(MmapReg(
        name="RCC_D1CCIPR", addr=(base + 0x04C),
        descr="RCC Domain 1 Kernel Clock Configuration Register",
        bits=[
            Bits(bits=range(16, 17), name="CKPERSEL", descr="per_ck clock source selection"),
            # 00: hsi_ker_ck clock selected as per_ck clock (default after reset)
            # 01: csi_ker_ck clock selected as per_ck clock
            # 10: hse_ck clock selected as per_ck clock
            # 11: reserved, the per_ck clock is disabled
            Bits(bits=range(16, 17), name="SDMMCSEL", descr="SDMMC kernel clock source selection"),
            # Bit 16 SDMMCSEL: SDMMC kernel clock source selection
            # 0: pll1_q_ck clock is selected as kernel peripheral clock (default after reset)
            # 1: pll2_r_ck clock is selected as kernel peripheral clock
            Bits(bits=range(4, 6), name="QSPISEL", descr="QUADSPI kernel clock source selection"),
            # 00: rcc_hclk3 clock selected as kernel peripheral clock (default after reset)
            # 01: pll1_q_ck clock selected as kernel peripheral clock
            # 10: pll2_r_ck clock selected as kernel peripheral clock
            # 11: per_ck clock selected as kernel peripheral clock
            Bits(bits=range(0, 2), name="FMCSEL", descr="FMC kernel clock source selection"),
            # 00: rcc_hclk3 clock selected as kernel peripheral clock (default after reset)
            # 01: pll1_q_ck clock selected as kernel peripheral clock
            # 10: pll2_r_ck clock selected as kernel peripheral clock
            # 11: per_ck clock selected as kernel peripheral clock

        ]))
    self.append(MmapReg(
        name="RCC_D2CCIP1R", addr=(base + 0x050),
        descr="RCC Domain 2 Kernel Clock Configuration Register",
        bits=[
        ]))
    self.append(MmapReg(
        name="RCC_D2CCIP2R", addr=(base + 0x054),
        descr="RCC Domain 2 Kernel Clock Configuration Register",
        bits=[
            Bits(
                bits=[12, 13], name="I2C123SEL", descr="I2C1,2,3 kernel clock source selection",
                descr_vals={
                    0: "rcc_pclk1 clock is selected as kernel clock (default after reset)",
                    1: "pll3_r_ck clock is selected as kernel clock",
                    2: "hsi_ker_ck clock is selected as kernel clock",
                    3: "csi_ker_ck clock is selected as kernel clock", })
        ]))

    self.append(MmapReg(
        name="RCC_D3CCIPR", addr=(base + 0x058),
        descr="RCC Domain 3 Kernel Clock Configuration Register",
        bits=[
            Bits(bits=[28, 29, 30], name="SPI6SEL"),
            Bits(bits=[24, 25, 26], name="SAI4BSEL"),
            Bits(bits=[21, 22, 23], name="SAI4ASEL"),
            Bits(
                bits=[16, 17], name="ADCSEL", descr="SAR ADC kernel clock source selection",
                descr_vals={
                    0: "pll2_p_ck clock selected as kernel peripheral clock",
                    1: "pll3_r_ck clock selected as kernel peripheral clock",
                    2: "per_ck clock selected as kernel peripheral clock",
                    3: "the kernel clock is disabled", }),
            Bits(bits=[13, 14, 15], name="LPTIM345SEL"),
            Bits(bits=[10, 11, 12], name="LPTIM2SEL"),
            Bits(
                bits=[8, 9], name="I2C4SEL", descr="I2C4 kernel clock source selection",
                descr_vals={
                    0: "rcc_pclk4 clock selected as kernel peripheral clock (default after reset)",
                    1: "pll3_r_ck clock selected as kernel peripheral clock",
                    2: "hsi_ker_ck clock selected as kernel peripheral clock",
                    3: "csi_ker_ck clock selected as kernel peripheral clock", }),
            Bits(bits=[0, 1, 2], name="LPUART1SEL"),
        ]))

    # ==============================================================================================
    self.append(MmapReg(
        name="RCC_APB1LENR", addr=(base + 0x0E8), descr="RCC APB1 Clock Register",
        bits=[
            Bits(bits=31, name="UART8EN", descr="UART8 Peripheral Clocks Enable"),
            Bits(bits=30, name="UART7EN", descr="UART7 Peripheral Clocks Enable"),
            Bits(bits=29, name="DAC12EN", descr="DAC1 and 2 peripheral clock enable"),
            Bits(bits=27, name="CECEN", descr="HDMI-CEC peripheral clock enable"),
            Bits(bits=23, name="I2C3EN", descr="I2C3 Peripheral Clocks Enable"),
            Bits(bits=22, name="I2C2EN", descr="I2C2 Peripheral Clocks Enable"),
            Bits(bits=21, name="I2C1EN", descr="I2C1 Peripheral Clocks Enable"),
            Bits(bits=20, name="UART5EN", descr="UART5 Peripheral Clocks Enable"),
            Bits(bits=19, name="UART4EN", descr="UART4 Peripheral Clocks Enable"),
            Bits(bits=18, name="USART3EN", descr="USART3 Peripheral Clocks Enable"),
            Bits(bits=17, name="USART2EN", descr="USART2 Peripheral Clocks Enable"),
            Bits(bits=16, name="SPDIFRXEN", descr="SPDIFRX Peripheral Clocks Enable"),
            Bits(bits=15, name="SPI3EN", descr="SPI3 Peripheral Clocks Enable"),
            Bits(bits=14, name="SPI2EN", descr="SPI2 Peripheral Clocks Enable"),
            Bits(bits=9, name="LPTIM1EN", descr="LPTIM1 Peripheral Clocks Enable"),
            Bits(bits=8, name="TIM14EN", descr="TIM14 peripheral clock enable"),
            Bits(bits=7, name="TIM13EN", descr="TIM13 peripheral clock enable"),
            Bits(bits=6, name="TIM12EN", descr="TIM12 peripheral clock enable"),
            Bits(bits=5, name="TIM7EN", descr="TIM7 peripheral clock enable"),
            Bits(bits=4, name="TIM6EN", descr="TIM6 peripheral clock enable"),
            Bits(bits=3, name="TIM5EN", descr="TIM5 peripheral clock enable"),
            Bits(bits=2, name="TIM4EN", descr="TIM4 peripheral clock enable"),
            Bits(bits=1, name="TIM3EN", descr="TIM3 peripheral clock enable"),
            Bits(bits=0, name="TIM2EN", descr="TIM2 peripheral clock enable"),
        ]))
    self.append(MmapReg(
        name="RCC_APB1HENR", addr=(base + 0x0EC), descr="RCC APB1 Clock Register",
        bits=[
            Bits(bits=8, name="FDCANEN", descr="FDCAN Peripheral Clocks Enable"),
            Bits(bits=5, name="MDIOSEN", descr="MDIOS peripheral clock enable"),
            Bits(bits=4, name="OPAMPEN", descr="OPAMP peripheral clock enable"),
            Bits(bits=2, name="SWPEN", descr="SWPMI Peripheral Clocks Enable"),
            Bits(bits=1, name="CRSEN", descr="Clock Recovery System peripheral clock enable"),
        ]))
    self.append(MmapReg(
        name="RCC_APB2ENR", addr=(base + 0x0F0), descr="RCC APB2 Clock Register",
        bits=[
            Bits(bits=29, name="HRTIMEN", descr="HRTIM peripheral clock enable"),
            Bits(bits=28, name="DFSDM1EN", descr="DFSDM1 Peripheral Clocks Enable"),
            Bits(bits=24, name="SAI3EN", descr="SAI3 Peripheral Clocks Enable"),
            Bits(bits=23, name="SAI2EN", descr="SAI2 Peripheral Clocks Enable"),
            Bits(bits=22, name="SAI1EN", descr="SAI1 Peripheral Clocks Enable"),
            Bits(bits=20, name="SPI5EN", descr="SPI5 Peripheral Clocks Enable"),
            Bits(bits=18, name="TIM17EN", descr="TIM17 peripheral clock enable"),
            Bits(bits=17, name="TIM16EN", descr="TIM16 peripheral clock enable"),
            Bits(bits=16, name="TIM15EN", descr="TIM15 peripheral clock enable"),
            Bits(bits=13, name="SPI4EN", descr="SPI4 Peripheral Clocks Enable"),
            Bits(bits=12, name="SPI1EN", descr="SPI1 Peripheral Clocks Enable"),
            Bits(bits=5, name="USART6EN", descr="USART6 Peripheral Clocks Enable"),
            Bits(bits=4, name="USART1EN", descr="USART1 Peripheral Clocks Enable"),
            Bits(bits=1, name="TIM8EN", descr="TIM8 peripheral clock enable"),
            Bits(bits=0, name="TIM1EN", descr="TIM1 peripheral clock enable"),
        ]))
    self.append(MmapReg(
        name="RCC_APB3ENR", addr=(base + 0x0E4), descr="RCC APB3 Clock Register",
        bits=[
            Bits(bits=6, name="WWDG1EN", descr="WWDG1 Clock Enable"),
            Bits(bits=3, name="LTDCEN", descr="LTDC peripheral clock enable"),
        ]))
    self.append(MmapReg(
        name="RCC_APB4ENR", addr=(base + 0x0F4), descr="RCC APB4 Clock Register",
        bits=[
            Bits(bits=21, name="SAI4EN", descr="SAI4 Peripheral Clocks Enable"),
            Bits(bits=16, name="RTCAPBEN", descr="RTC APB Clock Enable"),
            Bits(bits=15, name="VREFEN", descr="VREF peripheral clock enable"),
            Bits(bits=14, name="COMP12EN", descr="COMP1/2 peripheral clock enable"),
            Bits(bits=12, name="LPTIM5EN", descr="LPTIM5 Peripheral Clocks Enable"),
            Bits(bits=11, name="LPTIM4EN", descr="LPTIM4 Peripheral Clocks Enable"),
            Bits(bits=10, name="LPTIM3EN", descr="LPTIM3 Peripheral Clocks Enable"),
            Bits(bits=9, name="LPTIM2EN", descr="LPTIM2 Peripheral Clocks Enable"),
            Bits(bits=7, name="I2C4EN", descr="I2C4 Peripheral Clocks Enable"),
            Bits(bits=5, name="SPI6EN", descr="SPI6 Peripheral Clocks Enable"),
            Bits(bits=3, name="LPUART1EN", descr="LPUART1 Peripheral Clocks Enable"),
            Bits(bits=1, name="SYSCFGEN", descr="SYSCFG peripheral clock enable"),
        ]))
    # ==============================================================================================
    self.append(MmapReg(
        name="RCC_APB3RSTR", addr=(base + 0x08C),
        descr="RCC APB3 peripheral reset register", bits=[
            # Bit 6 WWDG1EN: WWDG1 Clock Enable
            # Bit 3 LTDCEN: LTDC peripheral clock enable
        ]))
    self.append(MmapReg(
        name="RCC_APB1LRSTR", addr=(base + 0x090),
        descr="RCC APB1 peripheral reset register", bits=[]))
    self.append(MmapReg(
        name="RCC_APB1HRSTR", addr=(base + 0x094),
        descr="RCC APB1 peripheral reset register", bits=[]))
    self.append(MmapReg(
        name="RCC_APB2RSTR", addr=(base + 0x098),
        descr="RCC APB2 peripheral reset register", bits=[]))
    self.append(MmapReg(
        name="RCC_APB4RSTR", addr=(base + 0x09C),
        descr="RCC APB4 peripheral reset register", bits=[]))
    # ==============================================================================================
    self.append(MmapReg(
        name="RCC_AHB1ENR", addr=(base + 0x0D8), descr="RCC AHB1 Clock Register",
        bits=[
            Bits(bits=28, name="USB2OTGHSULPIEN", descr="Enable USB_PHY2 clocks"),
            Bits(bits=27, name="USB2OTGHSEN", descr="USB2OTG (OTG_HS2) Peripheral Clocks Enable"),
            Bits(bits=26, name="USB1OTGHSULPIEN", descr="USB_PHY1 Clocks Enable"),
            Bits(bits=25, name="USB1OTGHSEN", descr="USB1OTG (OTG_HS1) Peripheral Clocks Enable"),
            Bits(bits=17, name="ETH1RXEN", descr="Ethernet Reception Clock Enable"),
            Bits(bits=16, name="ETH1TXEN", descr="Ethernet Transmission Clock Enable"),
            Bits(bits=15, name="ETH1MACEN", descr="Ethernet MAC bus interface Clock Enable"),
            Bits(bits=5, name="ADC12EN", descr="ADC1/2 Peripheral Clocks Enable"),
            Bits(bits=1, name="DMA2EN", descr="DMA2 Clock Enable"),
            Bits(bits=0, name="DMA1EN", descr="DMA1 Clock Enable"),
        ]))
    self.append(MmapReg(
        name="RCC_AHB2ENR", addr=(base + 0x0DC), descr="RCC AHB2 Clock Register",
        bits=[
        ]))
    self.append(MmapReg(
        name="RCC_AHB3ENR", addr=(base + 0x0D4), descr="RCC AHB3 Clock Register", bits=[
            Bits(bits=16, name="SDMMC1EN", descr="SDMMC1 and SDMMC1 Delay Clock Enable"),
            Bits(bits=14, name="QSPIEN", descr="QUADSPI and QUADSPI Delay Clock Enable"),
            Bits(bits=12, name="FMCEN", descr="FMC Peripheral Clocks Enable"),
            Bits(bits=5, name="JPGDECEN", descr="JPGDEC Peripheral Clock Enable"),
            Bits(bits=4, name="DMA2DEN", descr="DMA2D Peripheral Clock Enable"),
            Bits(bits=0, name="MDMAEN", descr="MDMA Peripheral Clock Enable"),
        ]))
    self.append(MmapReg(
        name="RCC_AHB4ENR", addr=(base + 0x0E0), descr="RCC AHB4 Clock Register",
        bits=[
            Bits(bits=28, name="BKPRAMEN", descr="Backup RAM Clock Enable"),
            Bits(bits=25, name="HSEMEN", descr="HSEM peripheral clock enable"),
            Bits(bits=24, name="ADC3EN", descr="ADC3 Peripheral Clocks Enable"),
            Bits(bits=21, name="BDMAEN", descr="BDMA and DMAMUX2 Clock Enable"),
            Bits(bits=19, name="CRCEN", descr="CRC peripheral clock enable"),
            Bits(bits=10, name="GPIOKEN", descr="GPIOK peripheral clock enable"),
            Bits(bits=9, name="GPIOJEN", descr="GPIOJ peripheral clock enable"),
            Bits(bits=8, name="GPIOIEN", descr="GPIOI peripheral clock enable"),
            Bits(bits=7, name="GPIOHEN", descr="GPIOH peripheral clock enable"),
            Bits(bits=6, name="GPIOGEN", descr="GPIOG peripheral clock enable"),
            Bits(bits=5, name="GPIOFEN", descr="GPIOF peripheral clock enable"),
            Bits(bits=4, name="GPIOEEN", descr="GPIOE peripheral clock enable"),
            Bits(bits=3, name="GPIODEN", descr="GPIOD peripheral clock enable"),
            Bits(bits=2, name="GPIOCEN", descr="GPIOC peripheral clock enable"),
            Bits(bits=1, name="GPIOBEN", descr="GPIOB peripheral clock enable"),
            Bits(bits=0, name="GPIOAEN", descr="GPIOA peripheral clock enable"),
        ]))
    # ==============================================================================================
    self.append(MmapReg(
        name="RCC_AHB1RSTR", addr=(base + 0x080),
        descr="RCC AHB1 peripheral reset register", bits=[]))
    self.append(MmapReg(
        name="RCC_AHB2RSTR", addr=(base + 0x084),
        descr="RCC AHB2 peripheral reset register", bits=[]))
    self.append(MmapReg(
        name="RCC_AHB3RSTR", addr=(base + 0x07C),
        descr="RCC AHB3 peripheral reset register", bits=[]))
    self.append(MmapReg(
        name="RCC_AHB4RSTR", addr=(base + 0x088),
        descr="RCC AHB4 peripheral reset register", bits=[
            Bits(bits=25, name="HSEMRST", descr="HSEM block reset"),
            Bits(bits=24, name="ADC3RST", descr="ADC3 block reset"),
            Bits(bits=21, name="BDMARST", descr="BDMA block reset"),
            Bits(bits=19, name="CRCRST", descr="CRC block reset"),
            Bits(bits=10, name="GPIOKRST", descr="GPIOK block reset"),
            Bits(bits=9, name="GPIOJRST", descr="GPIOJ block reset"),
            Bits(bits=8, name="GPIOIRST", descr="GPIOI block reset"),
            Bits(bits=7, name="GPIOHRST", descr="GPIOH block reset"),
            Bits(bits=6, name="GPIOGRST", descr="GPIOG block reset"),
            Bits(bits=5, name="GPIOFRST", descr="GPIOF block reset"),
            Bits(bits=4, name="GPIOERST", descr="GPIOE block reset"),
            Bits(bits=3, name="GPIODRST", descr="GPIOD block reset"),
            Bits(bits=2, name="GPIOCRST", descr="GPIOC block reset"),
            Bits(bits=1, name="GPIOBRST", descr="GPIOB block reset"),
            Bits(bits=0, name="GPIOARST", descr="GPIOA block reset"),
        ]))
    # ==============================================================================================
