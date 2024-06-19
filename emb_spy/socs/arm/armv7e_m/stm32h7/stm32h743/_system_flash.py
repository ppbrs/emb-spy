"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_system_flash(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"

    self.append(MmapReg(
        name="SYS_FLASH_SIZE", addr=0x1FF1E880, descr="Flash memory size",
        bits=[
            Bits(bits=range(16), name="F_SIZE", descr="Flash memory size in KBytes."),
        ]))

    self.append(MmapReg(
        name="SYS_UID0", addr=0x1FF1E800, descr="Unique device ID register [0:31]",
        bits=[
            Bits(bits=range(32), name="UID0", descr="Unique device ID register [0:31]."),
        ]))
    self.append(MmapReg(
        name="SYS_UID1", addr=0x1FF1E800 + 4, descr="Unique device ID register [32:63]",
        bits=[
            Bits(bits=range(32), name="UID1", descr="Unique device ID register [32:63]."),
        ]))
    self.append(MmapReg(
        name="SYS_UID2", addr=0x1FF1E800 + 8, descr="Unique device ID register [64:95]",
        bits=[
            Bits(bits=range(32), name="UID2", descr="Unique device ID register [64:95]."),
        ]))
