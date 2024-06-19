"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC

DAC12_BASE = 0x40007400


def init_dac(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"

    self.append(MmapReg(
        name="DAC_CR", addr=(DAC12_BASE + 0x00), descr="DAC control register",
        bits=[
            Bits(bits=0, name="EN1", descr="DAC channel1 enable"),
            Bits(bits=16, name="EN2", descr="DAC channel2 enable"),
        ]))

    self.append(MmapReg(
        name="DAC_MCR", addr=(DAC12_BASE + 0x3C), descr="DAC mode control register",
        bits=[
            Bits(bits=range(0, 3), name="MODE1", descr="DAC channel1 mode"),
            # – DAC channel1 in Normal mode
            # 000: DAC channel1 is connected to external pin with Buffer enabled
            # 001: DAC channel1 is connected to external pin and to on chip peripherals with Buffer
            # enabled
            # 010: DAC channel1 is connected to external pin with Buffer disabled
            # 011: DAC channel1 is connected to on chip peripherals with Buffer disabled
            # – DAC channel1 in sample & hold mode
            # 100: DAC channel1 is connected to external pin with Buffer enabled
            # 101: DAC channel1 is connected to external pin and to on chip peripherals with Buffer
            # enabled
            # 110: DAC channel1 is connected to external pin and to on chip peripherals with Buffer
            # disabled
            # 111: DAC channel1 is connected to on chip peripherals with Buffer disabled
            Bits(bits=range(16, 19), name="MODE2", descr="DAC channel2 mode"),
            # – DAC channel2 in Normal mode
            # 000: DAC channel2 is connected to external pin with Buffer enabled
            # 001: DAC channel2 is connected to external pin and to on chip peripherals with buffer
            # enabled
            # 010: DAC channel2 is connected to external pin with buffer disabled
            # 011: DAC channel2 is connected to on chip peripherals with Buffer disabled
            # – DAC channel2 in Sample and hold mode
            # 100: DAC channel2 is connected to external pin with Buffer enabled
            # 101: DAC channel2 is connected to external pin and to on chip peripherals with Buffer
            # enabled
            # 110: DAC channel2 is connected to external pin and to on chip peripherals with Buffer
            # disabled
            # 111: DAC channel2 is connected to on chip peripherals with Buffer disabled
        ]))
