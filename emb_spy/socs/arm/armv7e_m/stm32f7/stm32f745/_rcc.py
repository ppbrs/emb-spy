"""Part of STM32F745 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_rcc(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32F745"
    base = 0x40023800

    self.append(MmapReg(
        name="RCC_CR", addr=(base + 0x000),
        descr="RCC clock control register.",
        bits=[
            # Bits(bits=29, name="PLL3RDY", descr="PLL3 clock ready flag",),

            Bits(bits=29, name="PLLSAIRDY", descr="PLLSAI clock ready flag",),
            Bits(bits=28, name="PLLSAION", descr="PLLSAI enable",),
            Bits(bits=27, name="PLLI2SRDY", descr="PLLI2S clock ready flag",),
            Bits(bits=26, name="PLLI2SON", descr="PLLI2S enable",),
            Bits(bits=25, name="PLLRDY", descr="Main PLL (PLL) clock ready flag",),
            Bits(bits=24, name="PLLON", descr="Main PLL (PLL) enable",),
            Bits(bits=19, name="CSSON", descr="Clock security system enable",),
            Bits(bits=18, name="HSEBYP", descr="HSE clock bypass",),
            Bits(bits=17, name="HSERDY", descr="HSE clock ready flag",),
            Bits(bits=16, name="HSEON", descr="HSE clock enable",),
            Bits(bits=range(8, 16), name="HSICAL", descr="Internal high-speed clock calibration"),
            Bits(bits=range(3, 8), name="HSITRIM", descr="Internal high-speed clock trimming"),
            Bits(bits=1, name="HSIRDY", descr="Internal high-speed clock ready flag"),
            Bits(bits=0, name="HSION", descr="Internal high-speed clock enable"),
        ]))
    self.append(MmapReg(
        name="RCC_PLLCFGR", addr=(base + 0x04),
        descr="RCC PLL configuration register.",
        bits=[
            Bits(bits=range(24, 28), name="PLLQ", descr="Main PLL (PLL) division factor for USB OTG FS, SDMMC and random number generator clocks",),
            Bits(bits=22, name="PLLSRC", descr="Main PLL(PLL) and audio PLL (PLLI2S) entry clock source",),
            # 0: HSI clock selected as PLL and PLLI2S clock entry
            # 1: HSE oscillator clock selected as PLL and PLLI2S clock entry
            Bits(bits=range(16, 18), name="PLLP", descr="Main PLL (PLL) division factor for main system clock",),
            Bits(bits=range(6, 15), name="PLLN", descr="Main PLL (PLL) multiplication factor for VCO",),
            Bits(bits=range(0, 6), name="PLLM", descr="Main PLL(PLL) and audio PLL (PLLI2S) entry clock source",),
        ]))
    self.append(MmapReg(
        name="RCC_CFGR", addr=(base + 0x08),
        descr="RCC clock configuration register.",
        bits=[
            Bits(bits=range(30, 32), name="MCO2", descr="Microcontroller clock output 2",),
            # 00: System clock (SYSCLK) selected
            # 01: PLLI2S clock selected
            # 10: HSE oscillator clock selected
            # 11: PLL clock selected
            Bits(bits=range(27, 30), name="MCO2PRE", descr="MCO2 prescaler",),
            # 0xx: no division
            # 100: division by 2
            # 101: division by 3
            # 110: division by 4
            # 111: division by 5
            Bits(bits=range(24, 27), name="MCO1PRE", descr="MCO1 prescaler",),
            # 0xx: no division
            # 100: division by 2
            # 101: division by 3
            # 110: division by 4
            # 111: division by 5
            # Bit 23 I2SSRC: I2S clock selection
            # 0: PLLI2S clock used as I2S clock source
            # 1: External clock mapped on the I2S_CKIN pin used as I2S clock source
            Bits(bits=range(21, 23), name="MCO1", descr="Microcontroller clock output 1",),
            # 00: HSI clock selected
            # 01: LSE oscillator selected
            # 10: HSE oscillator clock selected
            # 11: PLL clock selected
            # Bits 20:16 RTCPRE: HSE division factor for RTC clock
            # 00000: no clock
            # 00001: no clock
            # 00010: HSE/2
            # 00011: HSE/3
            # 00100: HSE/4
            # ...
            # 11110: HSE/30
            # 11111: HSE/31
            # Bits 15:13 PPRE2: APB high-speed prescaler (APB2)
            # 0xx: AHB clock not divided
            # 100: AHB clock divided by 2
            # 101: AHB clock divided by 4
            # 110: AHB clock divided by 8
            # 111: AHB clock divided by 16
            # Bits 12:10 PPRE1: APB Low-speed prescaler (APB1)
            # 0xx: AHB clock not divided
            # 100: AHB clock divided by 2
            # 101: AHB clock divided by 4
            # 110: AHB clock divided by 8
            # 111: AHB clock divided by 16
            # Bits 7:4 HPRE: AHB prescaler
            # 0xxx: system clock not divided
            # 1000: system clock divided by 2
            # 1001: system clock divided by 4
            # 1010: system clock divided by 8
            # 1011: system clock divided by 16
            # 1100: system clock divided by 64
            # 1101: system clock divided by 128
            # 1110: system clock divided by 256
            # 1111: system clock divided by 512
            Bits(bits=range(2, 4), name="SWS", descr="System clock switch status",),
            # Bits 3:2 SWS: System clock switch status
            # 00: HSI oscillator used as the system clock
            # 01: HSE oscillator used as the system clock
            # 10: PLL used as the system clock
            # Bits 3:2 SWS: System clock switch status
            # 00: HSI oscillator selected as system clock
            # 01: HSE oscillator selected as system clock
            # 10: PLL selected as system clock
        ]))
    self.append(MmapReg(
        name="RCC_CIR", addr=(base + 0x0C),
        descr="RCC clock interrupt register",
        bits=[]))
    # ----------------------------------------------------------------------------------------------
    self.append(MmapReg(
        name="RCC_AHB1RSTR", addr=(base + 0x10),
        descr="RCC AHB1 peripheral reset register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_AHB2RSTR", addr=(base + 0x14),
        descr="RCC AHB2 peripheral reset register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_AHB3RSTR", addr=(base + 0x18),
        descr="RCC AHB3 peripheral reset register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_APB1RSTR", addr=(base + 0x20),
        descr="RCC APB1 peripheral reset register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_APB2RSTR", addr=(base + 0x24),
        descr="RCC APB2 peripheral reset register",
        bits=[]))
    # ----------------------------------------------------------------------------------------------
    self.append(MmapReg(
        name="RCC_AHB1ENR", addr=(base + 0x30),
        descr="RCC AHB1 peripheral clock register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_AHB2ENR", addr=(base + 0x34),
        descr="RCC AHB2 peripheral clock enable register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_AHB3ENR", addr=(base + 0x38),
        descr="RCC AHB3 peripheral clock enable register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_APB1ENR", addr=(base + 0x40),
        descr="RCC APB1 peripheral clock enable register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_APB2ENR", addr=(base + 0x44),
        descr="RCC APB2 peripheral clock enable register",
        bits=[]))
    # ----------------------------------------------------------------------------------------------
    self.append(MmapReg(
        name="RCC_AHB1LPENR", addr=(base + 0x50),
        descr="RCC AHB1 peripheral clock enable in low-power mode register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_AHB2LPENR", addr=(base + 0x54),
        descr="RCC AHB2 peripheral clock enable in low-power mode register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_AHB3LPENR", addr=(base + 0x58),
        descr="RCC AHB3 peripheral clock enable in low-power mode register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_APB1LPENR", addr=(base + 0x60),
        descr="RCC APB1 peripheral clock enable in low-power mode register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_APB2LPENR", addr=(base + 0x64),
        descr="RCC APB2 peripheral clock enabled in low-power mode register",
        bits=[]))
    # ----------------------------------------------------------------------------------------------
    self.append(MmapReg(
        name="RCC_BDCR", addr=(base + 0x70),
        descr="RCC backup domain control register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_CSR", addr=(base + 0x74),
        descr="RCC clock control & status register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_SSCGR", addr=(base + 0x80),
        descr="RCC spread spectrum clock generation register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_PLLI2SCFGR", addr=(base + 0x84),
        descr="RCC PLLI2S configuration register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_PLLSAICFGR", addr=(base + 0x88),
        descr="RCC PLLSAI configuration register",
        bits=[]))
    self.append(MmapReg(
        name="RCC_DCKCFGR1", addr=(base + 0x8C),
        descr="RCC dedicated clocks configuration register",
        bits=[]))
    self.append(MmapReg(
        name="DCKCFGR2", addr=(base + 0x90),
        descr="RCC dedicated clocks configuration register",
        bits=[]))
    # ----------------------------------------------------------------------------------------------
