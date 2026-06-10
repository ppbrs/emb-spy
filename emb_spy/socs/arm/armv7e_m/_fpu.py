"""Part of ARMV7EM SoC."""

from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg


def init_fpu(self) -> None:
    """
    Populate FPU registers.

    https://developer.arm.com/documentation/dui0646/c/Cortex-M7-Peripherals/Floating-Point-Unit
    """
    assert self.__class__.__name__ == "ARMV7EM"

    self += [
        MmapReg(
            name="FPCCR",
            addr=0xE000EF34,
            descr="Floating-point Context Control Register",
            bits=[
                Bits(bits=31, name="ASPEN"),
                Bits(bits=30, name="LSPEN"),
                Bits(bits=8, name="MONRDY"),
                Bits(bits=6, name="BFRDY"),
                Bits(bits=5, name="MMRDY"),
                Bits(bits=4, name="HFRDY"),
                Bits(bits=3, name="THREAD"),
                Bits(bits=1, name="USER"),
                Bits(bits=0, name="LSPACT"),
            ],
        ),
        MmapReg(
            name="FPCAR",
            addr=0xE000EF38,
            descr="Floating-point Context Address Register",
            bits=[
                Bits(
                    bits=range(3, 32),
                    name="ADDRESS",
                    descr="The location of the unpopulated floating-point register space allocated on an exception stack frame.",
                ),
            ],
        ),
        # FPSCR (Floating-point Status Control)  is not memory-mapped,
        # it can be accessed using the VMSR and VMRS instructions,
        MmapReg(
            name="FPDSCR",
            addr=0xE000EF3C,
            descr="Floating-point Default Status Control",
            bits=[
                # Bits(bits=31, name="N"),
                # Bits(bits=30, name="Z"),
                # Bits(bits=29, name="C"),
                # Bits(bits=28, name="V"),
                Bits(bits=26, name="AHP", descr="Alternative half-precision control bit"),
                Bits(bits=25, name="DN", descr="Default NaN mode control bit"),
                Bits(bits=24, name="FZ", descr="Flush-to-zero mode control bit"),
                Bits(bits=range(22,24), name="RMode", descr="Rounding Mode control field"),
                # Bits(bits=7, name="IDC"),
                # Bits(bits=4, name="IXC"),
                # Bits(bits=3, name="UFC"),
                # Bits(bits=2, name="OFC"),
                # Bits(bits=1, name="DZC"),
                # Bits(bits=0, name="IOC"),
            ],
        ),
        MmapReg(
            name="MVFR0",
            addr=0xE000EF40,
            descr="Media and VFP Feature Register 0",
            bits=[
                Bits(bits=range(28, 32), name="FP rounding modes"),
                Bits(bits=range(24, 28), name="Short vectors"),
                Bits(bits=range(20, 24), name="Square root"),
                Bits(bits=range(16, 20), name="Divide"),
                Bits(bits=range(12, 16), name="FP exception trapping"),
                Bits(bits=range(8, 12), name="Double-precision"),
                Bits(bits=range(4, 8), name="Single-precision"),
                Bits(bits=range(0, 4), name="A_SIMD registers"),
            ],
        ),
        MmapReg(
            name="MVFR1",
            addr=0xE000EF44,
            descr="Media and VFP Feature Register 1",
            bits=[
                Bits(bits=range(28, 32), name="FP fused MAC"),
                Bits(bits=range(24, 28), name="FP HPFP"),
                Bits(bits=range(4, 8), name="D_NaN mode,"),
                Bits(bits=range(0, 4), name="FtZ mode"),
            ],
        ),
        MmapReg(
            name="MVFR2",
            addr=0xE000EF48,
            descr="Media and VFP Feature Register 2",
            bits=[
                Bits(bits=range(4, 8), name="VFP_Misc"),
            ],
        ),
    ]
