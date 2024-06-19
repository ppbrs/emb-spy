"""Part of ARMV7EM SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg


def init_cache(self) -> None:
    assert self.__class__.__name__ == "ARMV7EM"
    # The System Control Block (SCB) provides system implementation information, and system
    # control. This includes configuration, control, and reporting of the system exceptions.

    self.append(MmapReg(
        name="CLIDR", addr=0xE000ED78, descr="Cache Level ID Register",
        bits=[
        ],
    ))

    self.append(MmapReg(
        name="CTR", addr=0xE000ED7C, descr="Cache Type Register",
        bits=[],
    ))

    self.append(MmapReg(
        name="CCSIDR", addr=0xE000ED80, descr="Cache Size ID Register",
        bits=[],
    ))

    self.append(MmapReg(
        name="CSSELR", addr=0xE000ED84, descr="Cache Size Selection Register",
        bits=[
            Bits(bits=0, name="InD", descr="Enables selection of instruction or data cache"),
        ],
    ))
