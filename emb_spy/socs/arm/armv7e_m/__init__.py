"""Module for ARM-v7e-m core SoC."""
from emb_spy.socs.arm.armv7e_m._cache import init_cache
from emb_spy.socs.arm.armv7e_m._debug import init_debug
from emb_spy.socs.arm.armv7e_m._fpu import init_fpu
from emb_spy.socs.arm.armv7e_m._mpu import init_mpu
from emb_spy.socs.arm.armv7e_m._nvic import init_nvic
from emb_spy.socs.arm.armv7e_m._scb import init_scb
from emb_spy.socs.arm.armv7e_m._systick import init_systick
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import CoreReg
from emb_spy.socs.soc import SoC


class ARMV7EM(SoC):
    """Generates Register objects for all ARM-v7e-m core peripherals."""

    def __init__(self):
        """Generate all Register objects."""
        super().__init__()

        self.init_core_registers()
        init_cache(self)
        init_debug(self)
        init_fpu(self)
        init_mpu(self)
        init_nvic(self)
        init_scb(self)
        init_systick(self)

    def init_core_registers(self) -> None:
        """Generate Register objects for all ARM-v7e-m core registers."""
        for i in range(13):
            self.append(CoreReg(
                name=f"R{i}", addr=f"r{i}", descr=f"General purpose register {i}."))

        self.append(CoreReg(name="SP", addr="sp", descr="Stack pointer"))
        self.append(CoreReg(name="PSP", addr="psp", descr="Stack pointer"))
        self.append(CoreReg(name="MSP", addr="msp", descr="Stack pointer"))

        self.append(CoreReg(name="LR", addr="lr", descr="Link register"))
        self.append(CoreReg(name="PC", addr="pc", descr="Program counter"))

        self.append(CoreReg(
            name="PSR", addr="xPSR", descr="(Combined) Program Status Register",
            bits=[
                Bits(bits=31, name="APSR:N", descr="Negative flag"),
                Bits(bits=30, name="APSR:Z", descr="Zero flag."),
                Bits(bits=29, name="APSR:C", descr="Carry or borrow flag."),
                Bits(bits=28, name="APSR:V", descr="Overflow flag."),
                Bits(bits=27, name="APSR:Q", descr="DSP overflow and saturation flag."),
                Bits(bits=range(16, 20), name="APSR:GE", descr="Greater than or Equal flags"),
                Bits(bits=range(0, 9), name="IPSR:ISR_NUMBER"),
                Bits(
                    bits=list(range(10, 16)) + list(range(25, 27)), name="EPSR:ICI/IT",
                    descr="Interruptible-continuable instruction bits / IT instruction state bits"
                ),
                Bits(bits=24, name="EPSR:T", descr="Thumb state bit"),
            ],
        ))

        self.append(CoreReg(
            name="PRIMASK", addr="primask", descr="Priority Mask Register", bits=[
                Bits(
                    bits=0, name="PRIMASK", descr="PRIMASK",
                    descr_vals={
                        0: "no effect",
                        1: "Prevents the activation of all exceptions with configurable priority."
                    }), ]))

        self.append(CoreReg(
            name="FAULTMASK", addr="faultmask", descr="Fault Mask Register", bits=[
                Bits(
                    bits=0, name="FAULTMASK", descr="FAULTMASK",
                    descr_vals={
                        0: "no effect",
                        1: "Prevents the activation of all exceptions except for NMI."})]))

        self.append(CoreReg(
            name="BASEPRI", addr="faultmask", descr="Base Priority Mask Register", bits=[
                Bits(bits=range(0, 8), name="BASEPRI", descr="Priority mask bits", )]))

        self.append(CoreReg(
            name="CONTROL", addr="control", descr="CONTROL register", bits=[
                Bits(
                    bits=0, name="nPRIV", descr="Defines the Thread mode privilege level",
                    descr_vals={
                        0: "Privileged",
                        1: "Unprivileged"}),
                Bits(
                    bits=1, name="SPSEL", descr="Defines the current stack",
                    descr_vals={
                        0: "MSP is the current stack pointer",
                        1: "PSP is the current stack pointer."}),
                Bits(
                    bits=2, name="FPCA",
                    descr="When floating-point is implemented this bit indicates whether "
                          "floating-point context is active",
                    descr_vals={
                        0: "No floating-point context active",
                        1: "Floating-point context active"}),
            ]))
