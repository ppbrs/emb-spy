"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_quadspi(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"

    # 0x52005000 QUADSPI control registers
    # 0x52006000 Delay Block QUADSPI
    base = 0x52005000

    self.append(MmapReg(
        name="QUADSPI_CR", addr=(base + 0x000),
        descr="QUADSPI control register",
        bits=[
            Bits(bits=0, name="EN", descr="QUADSPI enable"),
            Bits(bits=range(24, 32), name="PRESCALER", descr="Clock prescaler"),
        ]))
    self.append(MmapReg(
        name="QUADSPI_DCR", addr=(base + 0x004),
        descr="QUADSPI device configuration register",
        bits=[
            Bits(bits=range(16, 21), name="FSIZE", descr="Flash memory size"),
        ]))
    self.append(MmapReg(
        name="QUADSPI_SR", addr=(base + 0x008),
        descr="QUADSPI status register",
        bits=[]))
    self.append(MmapReg(
        name="QUADSPI_FCR", addr=(base + 0x00C),
        descr="QUADSPI flag clear register",
        bits=[]))
    self.append(MmapReg(
        name="QUADSPI_DLR", addr=(base + 0x010),
        descr="QUADSPI data length register",
        bits=[]))
    self.append(MmapReg(
        name="QUADSPI_CCR", addr=(base + 0x014),
        descr="QUADSPI communication configuration register",
        bits=[]))
    self.append(MmapReg(
        name="QUADSPI_AR", addr=(base + 0x018),
        descr="QUADSPI address register",
        bits=[]))
    self.append(MmapReg(
        name="QUADSPI_ABR", addr=(base + 0x01C),
        descr="QUADSPI alternate-byte register",
        bits=[]))
    self.append(MmapReg(
        name="QUADSPI_DR", addr=(base + 0x020),
        descr="QUADSPI data register",
        bits=[]))
    self.append(MmapReg(
        name="QUADSPI_PSMKR", addr=(base + 0x024),
        descr="QUADSPI polling status mask register",
        bits=[]))
    self.append(MmapReg(
        name="QUADSPI_PSMAR", addr=(base + 0x028),
        descr="QUADSPI polling status match register",
        bits=[]))
    self.append(MmapReg(
        name="QUADSPI_PIR", addr=(base + 0x02C),
        descr="QUADSPI polling interval register",
        bits=[]))
    self.append(MmapReg(
        name="QUADSPI_LPTR", addr=(base + 0x030),
        descr="QUADSPI low-power timeout register",
        bits=[]))
