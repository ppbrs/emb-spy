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
