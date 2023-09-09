"""
Registers of ARM V7E-M core and core peripherals.
"""
# Disabling line-too-long because it's impossible to keep
# human-readable register and bit descriptions short.
# pylint: disable=line-too-long

from emb_spy.mmreg.registers_if import Register, RegisterBits, Registers  # pylint: disable=import-error


class MmregARMV6M(Registers):
    """ An instance of this class generates the list of Register objects
    for the core and core peripherals. """

    def __init__(self) -> None:
        self.regs = []

        self._init_core()
        self._init_nvic()
        self._init_scb()
        self._init_systick()

    def _init_core(self) -> None:
        self.regs += [
            Register(name="PRIMASK", addr="primask", descr="Priority Mask Register", register_bits=[
                RegisterBits(bits=0, name="PRIMASK", descr="Thumb State bit", values={
                    0: "no effect", 1: "prevents the activation of all exceptions with configurable priority."}),]),
        ]
        self.regs += [
            Register(name="CONTROL", addr="control", descr="CONTROL register", register_bits=[
                RegisterBits(bits=1, name="SPSEL", descr="Defines the current stack", values={
                    0: "MSP is the current stack pointer", 1: "PSP is the current stack pointer."}),]),
        ]
        self.regs += [
            Register(name="SP", addr="sp", descr="Stack pointer"),
        ]
        self.regs += [
            Register(name="PSP", addr="psp", descr="Stack pointer"),
        ]
        self.regs += [
            Register(name="MSP", addr="msp", descr="Stack pointer"),
        ]
        self.regs += [
            Register(name="LR", addr="lr", descr="Link register"),
        ]
        self.regs += [
            Register(name="PC", addr="pc", descr="Program counter"),
        ]

        xpsr_exc_num_bit_vals = {
            0: "Thread mode",
            2: "NMI",
            3: "HardFault",
            11: "SVCall",
            14: "PendSV",
            15: "SysTick", }
        for irq_idx in range(0, 16):
            xpsr_exc_num_bit_vals[16 + irq_idx] = "IRQ" + str(irq_idx)
        self.regs += [
            Register(name="xPSR", addr="xPSR", descr="Program status regiser", register_bits=[
                RegisterBits(bits=range(0, 6), name="Exception Number", descr="", values=xpsr_exc_num_bit_vals),
                RegisterBits(bits=24, name="T", descr="Thumb State bit", values={}),
            ]),
        ]

    def _init_nvic(self) -> None:
        self.regs += [
            Register(name="ISER", addr=0xE000E100, descr="Interrupt Set-enable Register"),
            Register(name="ICER", addr=0xE000E180, descr="Interrupt Clear-enable Register"),
            Register(name="ISPR", addr=0xE000E200, descr="Interrupt Set-pending Register"),
            Register(name="ICPR", addr=0xE000E280, descr="Interrupt Clear-pending Register"),

            Register(name="IPR0", addr=0xE000E400 + 0, descr="Interrupt Priority Register 0", register_bits=[
                RegisterBits(bits=range(0, 8), name="PRI_0"),
                RegisterBits(bits=range(8, 16), name="PRI_1"),
                RegisterBits(bits=range(16, 24), name="PRI_2"),
                RegisterBits(bits=range(24, 32), name="PRI_3"),]),
            Register(name="IPR1", addr=0xE000E400 + 1, descr="Interrupt Priority Register 1"),
            Register(name="IPR2", addr=0xE000E400 + 2, descr="Interrupt Priority Register 2"),
            Register(name="IPR3", addr=0xE000E400 + 3, descr="Interrupt Priority Register 3"),
            Register(name="IPR4", addr=0xE000E400 + 4, descr="Interrupt Priority Register 4"),
            Register(name="IPR5", addr=0xE000E400 + 5, descr="Interrupt Priority Register 5"),
            Register(name="IPR6", addr=0xE000E400 + 6, descr="Interrupt Priority Register 6"),
            Register(name="IPR7", addr=0xE000E400 + 7, descr="Interrupt Priority Register 7"),
        ]

    def _init_scb(self) -> None:

        self.regs += [
            Register(name="CPUID", addr=0xE000ED00, descr="CPUID Register"),
            Register(name="ICSR", addr=0xE000ED04, descr="Interrupt Control and State Register"),
            Register(name="AIRCR", addr=0xE000ED0C, descr="a0xFA050000 Application Interrupt and Reset Control Register"),
            Register(name="SCR", addr=0xE000ED10, descr="System Control Register"),
            Register(name="CCR", addr=0xE000ED14, descr="Configuration and Control Register"),
            Register(name="SHPR2", addr=0xE000ED1C, descr="System Handler Priority Register 2", register_bits=[
                RegisterBits(bits=range(24, 32), name="PRI_11", descr="Priority of system handler 11, SVCall"),]),
            Register(name="SHPR3", addr=0xE000ED20, descr="System Handler Priority Register 3", register_bits=[
                RegisterBits(bits=range(24, 32), name="PRI_15", descr="Priority of system handler 15, SysTick exception"),
                RegisterBits(bits=range(16, 24), name="PRI_14", descr="Priority of system handler 14, PendSV"),]),
        ]

    def _init_systick(self) -> None:
        self.regs += [
            Register(
                name="SYST_CSR",
                addr=0xE000E010, descr="SysTick Control and Status Register",
                comment="The SysTick SYST_CSR register enables the SysTick features.",
                register_bits=[
                    RegisterBits(bits=16, name="COUNTFLAG",
                                 descr="Returns 1 if timer counted to 0 since last time this was read."),
                    RegisterBits(bits=2, name="CLKSOURCE", descr="Indicates the clock source",
                                 values={0: "External clock.", 1: "Processor clock.", }),
                    RegisterBits(bits=1, name="TICKINT", descr="Enables SysTick exception request",
                                 values={
                                     0: "Counting down to zero does not assert the SysTick exception request.",
                                     1: "Counting down to zero asserts the SysTick exception request.",
                                 }),
                    RegisterBits(bits=0, name="ENABLE", descr="Enables the counter",
                                 values={0: "Counter disabled.", 1: "Counter enabled.", }),
                ]
            ),
            Register(name="SYST_RVR", addr=0xE000E014, descr="SysTick Reload Value Register"),
            Register(name="SYST_CVR", addr=0xE000E018, descr="SysTick Current Value Register"),
            Register(name="SYST_CALIB", addr=0xE000E01C, descr="SysTick Calibration Value Register"),
        ]
