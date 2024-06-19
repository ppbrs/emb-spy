"""Part of STM32F051 SoC."""
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_tim2_tim3(self: SoC, prefix: str, base: int) -> None:
    """Generate Register objects for USART peripheral."""
    assert self.__class__.__name__ == "STM32F051"

    self.append(MmapReg(
        name=prefix + "_CNT", addr=(base + 0x24), descr=f"{prefix} counter",
    ))
    self.append(MmapReg(
        name=prefix + "_PSC", addr=(base + 0x28), descr=f"{prefix} counter",
    ))
    self.append(MmapReg(
        name=prefix + "_ARR", addr=(base + 0x2C), descr=f"{prefix} counter",
    ))
    self.append(MmapReg(
        name=prefix + "_CCR1", addr=(base + 0x34), descr=f"{prefix} counter",
    ))
    self.append(MmapReg(
        name=prefix + "_CCR2", addr=(base + 0x38), descr=f"{prefix} counter",
    ))
    self.append(MmapReg(
        name=prefix + "_CCR3", addr=(base + 0x3C), descr=f"{prefix} counter",
    ))
    self.append(MmapReg(
        name=prefix + "_CCR4", addr=(base + 0x40), descr=f"{prefix} counter",
    ))
