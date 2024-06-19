"""Part of ARMV6M SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_debug(self: SoC) -> None:
    """Generate Register objects for ARM v6-m debug infrastructure."""

    # See more Data Watchpoint and Trace registers:
    # https://developer.arm.com/documentation/ddi0419/c/Debug-Architecture/ARMv6-M-Debug/The-Data-Watchpoint-and-Trace-unit/DWT-register-summary
    self.append(
        MmapReg(name="DWT_PCSR", addr=0xE000101C, descr="Program Counter Sample Register", bits=[
            Bits(bits=range(0, 32), name="EIASAMPLE"), ]))
