# 0x52000000 - 0x52000FFFMDMA

"""Part of STM32H743 SoC."""
from emb_spy.socs.soc import SoC


def init_mdma(self: SoC):
    assert self.__class__.__name__ == "STM32H743"
