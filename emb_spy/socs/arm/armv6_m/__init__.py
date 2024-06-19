"""Module for ARM-v6-m core SoC."""
from emb_spy.socs.arm.armv6_m._debug import init_debug
from emb_spy.socs.arm.armv6_m._nvic import init_nvic
from emb_spy.socs.arm.armv6_m._scb import init_scb
from emb_spy.socs.arm.armv6_m._systick import init_systick
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import CoreReg
from emb_spy.socs.soc import SoC


class ARMV6M(SoC):
    """Generates Register objects for ARM-v6-m core and all core peripherals."""

    def __init__(self) -> None:
        """Generate all Register objects."""
        super().__init__()
        self.init_core_registers()
        init_debug(self)
        init_nvic(self)
        init_scb(self)
        init_systick(self)

    def init_core_registers(self) -> None:
        """Generate Register objects for all ARM-v6-m core registers."""
        for i in range(13):
            self.append(CoreReg(
                name=f"R{i}", addr=f"r{i}", descr=f"General purpose register {i}."))

        self.append(CoreReg(name="SP", addr="sp", descr="Stack pointer"))
        self.append(CoreReg(name="PSP", addr="psp", descr="Stack pointer"))
        self.append(CoreReg(name="MSP", addr="msp", descr="Stack pointer"))

        self.append(CoreReg(name="LR", addr="lr", descr="Link register"))
        self.append(CoreReg(name="PC", addr="pc", descr="Program counter"))

        xpsr_exc_num_bit_descr_vals = {
            0: "Thread mode",
            2: "NMI",
            3: "HardFault",
            11: "SVCall",
            14: "PendSV",
            15: "SysTick", }
        for irq_idx in range(0, 16):
            xpsr_exc_num_bit_descr_vals[16 + irq_idx] = "IRQ" + str(irq_idx)
        self.append(CoreReg(
            name="PSR", addr="xPSR", descr="Program status regiser", bits=[
                Bits(
                    bits=range(0, 6), name="IPSR:ExceptionNumber",
                    descr_vals=xpsr_exc_num_bit_descr_vals),
                Bits(bits=24, name="EPSR:T", descr="Thumb State bit"),
                Bits(bits=28, name="APSR:V", descr="Overflow flag"),
                Bits(bits=29, name="APSR:C", descr="Carry or borrow flag"),
                Bits(bits=30, name="APSR:Z", descr="Zero flag"),
                Bits(bits=31, name="APSR:N", descr="Negative flag"),
            ]))

        self.append(CoreReg(
            name="PRIMASK", addr="primask", descr="Priority Mask Register", bits=[
                Bits(
                    bits=0, name="PRIMASK", descr="PRIMASK",
                    descr_vals={
                        0: "no effect",
                        1: "prevents the activation of all exceptions with configurable priority."
                    }), ]))
        self.append(CoreReg(
            name="CONTROL", addr="control", descr="CONTROL register", bits=[
                Bits(
                    bits=1, name="SPSEL", descr="Defines the current stack", descr_vals={
                        0: "MSP is the current stack pointer",
                        1: "PSP is the current stack pointer."}),]))
