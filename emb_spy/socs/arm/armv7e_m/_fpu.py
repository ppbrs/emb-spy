"""Part of ARMV7EM SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg


def init_fpu(self) -> None:
    assert self.__class__.__name__ == "ARMV7EM"

    self += [
        MmapReg(name="FPCCR", addr=0xE000EF34, descr="Floating-point Context Control Register"),
        MmapReg(name="FPCAR", addr=0xE000EF38, descr="Floating-point Context Address Register"),
        MmapReg(name="FPDSCR", addr=0xE000EF3C, descr="Floating-point Default Status Control"),
        MmapReg(name="MVFR0", addr=0xE000EF40, descr="Media and VFP Feature Register 0", bits=[
            Bits(bits=range(28, 32), name="FP rounding modes"),
            Bits(bits=range(24, 28), name="Short vectors"),
            Bits(bits=range(20, 24), name="Square root"),
            Bits(bits=range(16, 20), name="Divide"),
            Bits(bits=range(12, 16), name="FP exception trapping"),
            Bits(bits=range(8, 12), name="Double-precision"),
            Bits(bits=range(4, 8), name="Single-precision"),
            Bits(bits=range(0, 4), name="A_SIMD registers"),
        ]),
        MmapReg(name="MVFR1", addr=0xE000EF44, descr="Media and VFP Feature Register 1", bits=[
            Bits(bits=range(28, 32), name="FP fused MAC"),
            Bits(bits=range(24, 28), name="FP HPFP"),
            Bits(bits=range(4, 8), name="D_NaN mode,"),
            Bits(bits=range(0, 4), name="FtZ mode"),
        ]),
        MmapReg(name="MVFR2", addr=0xE000EF48, descr="Media and VFP Feature Register 2", bits=[
            Bits(bits=range(4, 8), name="VFP_Misc"),
        ]),

    ]
