"""Part of ARMV7EM SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg


def init_systick(self) -> None:
    assert self.__class__.__name__ == "ARMV7EM"

    self.append(MmapReg(
        name="SYST_CSR",
        addr=0xE000E010, descr="SysTick Control and Status Register",
        comment="The SysTick SYST_CSR register enables the SysTick features.",
        bits=[
            Bits(
                bits=16, name="COUNTFLAG",
                descr="Returns 1 if timer counted to 0 since last time this was read."),
            Bits(
                bits=2, name="CLKSOURCE", descr="Indicates the clock source",
                descr_vals={0: "External clock.", 1: "Processor clock.", }),
            Bits(
                bits=1, name="TICKINT", descr="Enables SysTick exception request",
                descr_vals={
                    0: "Counting down to zero does not assert the SysTick exception request.",
                    1: "Counting down to zero asserts the SysTick exception request.", }),
            Bits(
                bits=0, name="ENABLE", descr="Enables the counter",
                descr_vals={0: "Counter disabled.", 1: "Counter enabled.", }),
        ]
    ))
    self.append(MmapReg(
        name="SYST_RVR", addr=0xE000E014, descr="SysTick Reload Value Register", bits=[
            Bits(
                bits=range(0, 24), name="RELOAD",
                descr="Value to load into the SYST_CVR register when the counter is enabled "
                      "and when it reaches 0."),
        ]))
    self.append(MmapReg(
        name="SYST_CVR", addr=0xE000E018, descr="SysTick Current Value Register", bits=[
            Bits(bits=range(0, 24), name="CURRENT"),
        ]))
    self.append(MmapReg(
        name="SYST_CALIB", addr=0xE000E01C, descr="SysTick Calibration Value Register", bits=[
            Bits(bits=31, name="NOREF"),
            # Indicates whether the device provides a reference clock to the processor:
            # 0 Reference clock provided.
            # 1 No reference clock provided.
            # If your device does not provide a reference clock, the SYST_CSR.CLKSOURCE bit
            # reads-as-one and ignores writes.
            Bits(bits=30, name="SKEW"),
            # Indicates whether the TENMS value is exact:
            # 0 TENMS value is exact.
            # 1 TENMS value is inexact, or not given.
            # An inexact TENMS value can affect the suitability of SysTick as a software
            # real time clock.
            Bits(bits=range(0, 24), name="TENMS"),
            # Reload value for 10ms (100Hz) timing, subject to system clock skew errors.
            # If the value reads as zero, the calibration value is not known.
        ]))
