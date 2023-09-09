"""
Registers of ARM V7E-M core and core peripherals.
"""
# Disabling line-too-long because it's impossible to keep
# human-readable register and bit descriptions short.
# pylint: disable=line-too-long

from emb_spy.mmreg.registers_if import Register, RegisterBits, Registers  # pylint: disable=import-error

from ._nvic import _Nvic


class MmregARMV7EM(Registers):
    """ An instance of this class generates the list of Register objects
    for the core and core peripherals. """

    def get_list(self) -> list[Register]:
        """ Return the list of all Register objects. """
        return self.regs

    def __init__(self):
        self.regs = []

        self._init_core()
        self._init_fpu()
        self._init_scb()
        self._init_systick()
        self.regs += _Nvic().get_list()

    def _init_core(self) -> None:
        self.regs.append(
            Register(
                name="xPSR", addr="xPSR", descr="(Combined) Program Status Register",
                register_bits=[
                    RegisterBits(bits=31, name="APSR:N", descr="Negative flag", values={}),
                    RegisterBits(bits=30, name="APSR:Z", descr="Zero flag.", values={}),
                    RegisterBits(bits=29, name="APSR:C", descr="Carry or borrow flag.", values={}),
                    RegisterBits(bits=28, name="APSR:V", descr="Overflow flag.", values={}),
                    RegisterBits(bits=27, name="APSR:Q", descr="DSP overflow and saturation flag.", values={}),
                    RegisterBits(bits=range(16, 20), name="APSR:GE", descr="Greater than or Equal flags", values={}),
                    RegisterBits(bits=range(0, 9), name="IPSR:ISR_NUMBER", descr="", values={}),
                    RegisterBits(bits=range(25, 27), name="EPSR:ICI/IT", descr="Interruptible-continuable instruction bits / IT instruction state bits", values={}),
                    RegisterBits(bits=24, name="EPSR:T", descr="Thumb state bit", values={}),
                ],
            ))

    def _init_scb(self) -> None:
        """
        The System Control Block (SCB) provides system implementation information, and system
        control. This includes configuration, control, and reporting of the system exceptions.
        """
        self.regs += [
            # 0xE000E008 ACTLR Auxiliary Control Register
            # 0xE000ED00 CPUID CPUID Base Register
            # 0xE000ED04 ICSRb Interrupt Control and State Register
            # 0xE000ED08 VTOR Vector Table Offset Register
            # 0xE000ED0C AIRCR Application Interrupt and Reset Control Register
            # 0xE000ED10 SCR System Control Register
            # 0xE000ED14 CCR Configuration and Control Register

            Register(
                name="SHPR1", addr=0xE000ED18, descr="System Handler Priority Register 1",
                register_bits=[
                    RegisterBits(bits=range(16, 24), name="PRI_6", descr="Priority of system handler 6, UsageFault", values={}),
                    RegisterBits(bits=range(8, 16), name="PRI_5", descr="Priority of system handler 5, BusFault", values={}),
                    RegisterBits(bits=range(0, 8), name="PRI_4", descr="Priority of system handler 4, MemManage", values={}),
                ],
            ),
            Register(
                name="SHPR2", addr=0xE000ED1C, descr="System Handler Priority Register 2",
                register_bits=[
                    RegisterBits(bits=range(24, 32), name="PRI_11", descr="Priority of system handler 11, SVCall", values={}),
                ],
            ),
            Register(
                name="SHPR3", addr=0xE000ED20, descr="System Handler Priority Register 3",
                register_bits=[
                    RegisterBits(bits=range(24, 32), name="PRI_15", descr="Priority of system handler 15, SysTick exception", values={}),
                    RegisterBits(bits=range(16, 24), name="PRI_14", descr="Priority of system handler 14, PendSV", values={}),
                ],
            ),
            Register(
                name="SHCSR", addr=0xE000ED24, descr="System Handler Control and State Register",
                register_bits=[
                    RegisterBits(bits=18, name="USGFAULTENA", descr="UsageFault enable bit, set to 1 to enable", values={}),
                    RegisterBits(bits=17, name="BUSFAULTENA", descr="BusFault enable bit, set to 1 to enable", values={}),
                    RegisterBits(bits=16, name="MEMFAULTENA", descr="MemManage enable bit, set to 1 to enable", values={}),
                    RegisterBits(bits=15, name="SVCALLPENDED", descr="SVCall pending bit, reads as 1 if exception is pending", values={}),
                    RegisterBits(bits=14, name="BUSFAULTPENDED", descr="BusFault exception pending bit, reads as 1 if exception is pending", values={}),
                    RegisterBits(bits=13, name="MEMFAULTPENDED", descr="MemManage exception pending bit, reads as 1 if exception is pending", values={}),
                    RegisterBits(bits=12, name="USGFAULTPENDED", descr="UsageFault exception pending bit, reads as 1 if exception is pending", values={}),
                    RegisterBits(bits=11, name="SYSTICKACT", descr="SysTick exception active bit, reads as 1 if exception is active", values={}),
                    RegisterBits(bits=10, name="PENDSVACT", descr="PendSV exception active bit, reads as 1 if exception is active", values={}),
                    RegisterBits(bits=8, name="MONITORACT", descr="Debug monitor active bit, reads as 1 if Debug monitor is active", values={}),
                    RegisterBits(bits=7, name="SVCALLACT", descr="SVCall active bit, reads as 1 if SVC call is active", values={}),
                    RegisterBits(bits=3, name="USGFAULTACT", descr="UsageFault exception active bit, reads as 1 if exception is active", values={}),
                    RegisterBits(bits=1, name="BUSFAULTACT", descr="BusFault exception active bit, reads as 1 if exception is active", values={}),
                    RegisterBits(bits=0, name="MEMFAULTACT", descr="MemManage exception active bit, reads as 1 if exception is active", values={}),
                ],
            ),
            Register(
                name="CFSR", addr=0xE000ED28, descr="Configurable Fault Status Register",
                comment="Indicates the cause of a MemManage fault, BusFault, or UsageFault.",
                register_bits=[
                    # Memory management fault:
                    RegisterBits(bits=range(0, 8), name="MMFSR", descr="Memory Management Fault Status Register.", ),

                    RegisterBits(bits=7, name="MMFSR:MMARVALID", descr="MemManage Fault Address Register (MMFAR) valid flag", ),
                    # 0 Value in MMAR is not a valid fault address.
                    # 1 MMAR holds a valid fault address.
                    # If a MemManage fault occurs and is escalated to a HardFault because of priority, the HardFault
                    # handler must set this bit to 0. This prevents problems on return to a stacked active MemManage
                    # fault handler whose MMAR value has been overwritten.

                    RegisterBits(bits=5, name="MMFSR:MLSPERR", descr="", ),
                    # 0 = No MemManage fault occurred during floating-point lazy state preservation.
                    # 1 = A MemManage fault occurred during floating-point lazy state preservation.

                    RegisterBits(bits=4, name="MMFSR:MSTKERR", descr="MemManage fault on stacking for exception entry", ),
                    # 0 No stacking fault.
                    # 1 Stacking for an exception entry has caused one or more access violations.
                    # When this bit is 1, the SP is still adjusted but the values in the context area on the stack might
                    # be incorrect. The processor has not written a fault address to the MMAR.

                    RegisterBits(bits=3, name="MMFSR:MUNSTKERR", descr="MemManage fault on unstacking for a return from exception", ),
                    # 0 No unstacking fault.
                    # 1 Unstack for an exception return has caused one or more access violations.
                    # This fault is chained to the handler. This means that when this bit is 1, the original return stack
                    # is still present. The processor has not adjusted the SP from the failing return, and has not
                    # performed a new save. The processor has not written a fault address to the MMAR.

                    RegisterBits(bits=1, name="MMFSR:DACCVIOL", descr="Data access violation flag", ),
                    # 0 No data access violation fault.
                    # 1 The processor attempted a load or store at a location that does not permit the
                    # operation.
                    # When this bit is 1, the PC value stacked for the exception return points to the faulting
                    # instruction. The processor has loaded the MMAR with the address of the attempted access.

                    RegisterBits(bits=0, name="MMFSR:IACCVIOL", descr="Instruction access violation flag",
                                 values={
                                     0: "No instruction access violation fault.",
                                     1: "The processor attempted an instruction fetch from a location that does not permit execution.", }),
                    # This fault occurs on any access to an XN region, even when the MPU is disabled or not present.
                    # When this bit is 1, the PC value stacked for the exception return points to the faulting
                    # instruction. The processor has not written a fault address to the MMAR.

                    # Bust fault:
                    RegisterBits(bits=range(8, 16), name="BFSR", descr="Bus Fault Status Register", ),
                    RegisterBits(bits=(8 + 7), name="BFSR:BFARVALID", descr="Address Register (BFAR) valid flag", ),
                    RegisterBits(bits=(8 + 5), name="BFSR:LSPERR", descr="", ),
                    RegisterBits(bits=(8 + 4), name="BFSR:STKERR", descr="", ),
                    RegisterBits(bits=(8 + 3), name="BFSR:UNSTKERR", descr="", ),
                    RegisterBits(bits=(8 + 2), name="BFSR:IMPRECISERR", descr="", ),
                    RegisterBits(bits=(8 + 1), name="BFSR:PRECISERR", descr="", ),
                    RegisterBits(bits=(8 + 0), name="BFSR:IBUSERR", descr="", ),

                    # Usage fault:
                    RegisterBits(bits=range(16, 32), name="UFSR", descr="Usage Fault Status Register"),

                    RegisterBits(bits=(16 + 9), name="UFSR:DIVBYZERO", descr=""),
                    RegisterBits(bits=(16 + 8), name="UFSR:UNALIGNED", descr=""),
                    RegisterBits(bits=(16 + 3), name="UFSR:NOCP", descr=""),
                    RegisterBits(bits=(16 + 2), name="UFSR:INVPC", descr=""),
                    RegisterBits(bits=(16 + 1), name="UFSR:INVSTATE", descr=""),
                    RegisterBits(bits=(16 + 0), name="UFSR:UNDEFINSTR", descr=""),


                ],
            ),
            # 0xE000ED28 MMFSR age Fault Status Register
            Register(
                name="HFSR", addr=0xE000ED2C, descr="HardFault Status Register",
                comment="Gives information about events that activate the HardFault handler.",
                register_bits=[
                    RegisterBits(bits=1, name="VECTTBL", descr="Indicates a BusFault on a vector table read during exception processing.",
                                 values={
                                     0: "No BusFault on vector table read.",
                                     1: "BusFault on vector table read.", }
                                 ),
                    RegisterBits(bits=30, name="FORCED", descr="Indicates a forced hard fault, generated by escalation of a fault with configurable priority that cannot be handled, either because of priority or because it is disabled.",
                                 values={
                                     0: "No forced HardFault.",
                                     1: "Forced HardFault.", }
                                 ),
                    RegisterBits(bits=31, name="DEBUGEVT", descr="Reserved for Debug use."),
                ],
            ),
            # 0xE000ED29 BFSR Status Register
            # 0xE000ED2A UFSR eFault Status Register
            # 0xE000ED2C HFSR HardFault Status Register
            # 0xE000ED34 MMFAR MemManage Fault Address Register
            # 0xE000ED38 BFAR BusFault Address Register

            Register(
                name="CPACR", addr=0xE000ED88, descr="Coprocessor Access Control Register",
                comment="The CPACR register specifies the access privileges for coprocessors.",
                register_bits=[
                    RegisterBits(bits=[20, 21], name="CP10", descr="Access privileges for coprocessor 10.",
                                 values={
                                     0: "Access denied. Any attempted access generates a NOCP UsageFault.",
                                     1: "Privileged access only. An unprivileged access generates a NOCP fault.",
                                     2: "Reserved. The result of any access is Unpredictable.",
                                     3: "Full access.", }
                                 ),
                    RegisterBits(bits=[22, 23], name="CP11", descr="Access privileges for coprocessor 11.",
                                 values={
                                     0: "Access denied. Any attempted access generates a NOCP UsageFault.",
                                     1: "Privileged access only. An unprivileged access generates a NOCP fault.",
                                     2: "Reserved. The result of any access is Unpredictable.",
                                     3: "Full access.", }
                                 ),
                ],
            ),


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

    def _init_fpu(self) -> None:

        self.regs += [
            Register(name="FPCCR", addr=0xE000EF34, descr="Floating-point Context Control Register"),
            Register(name="FPCAR", addr=0xE000EF38, descr="Floating-point Context Address Register"),
            Register(name="FPDSCR", addr=0xE000EF3C, descr="Floating-point Default Status Control"),
            Register(name="MVFR0", addr=0xE000EF40, descr="Media and VFP Feature Register 0", register_bits=[
                RegisterBits(bits=range(28, 32), name="FP rounding modes", descr=""),
                RegisterBits(bits=range(24, 28), name="Short vectors", descr=""),
                RegisterBits(bits=range(20, 24), name="Square root", descr=""),
                RegisterBits(bits=range(16, 20), name="Divide", descr=""),
                RegisterBits(bits=range(12, 16), name="FP exception trapping", descr=""),
                RegisterBits(bits=range(8, 12), name="Double-precision", descr=""),
                RegisterBits(bits=range(4, 8), name="Single-precision", descr=""),
                RegisterBits(bits=range(0, 4), name="A_SIMD registers", descr=""),
            ]),
            Register(name="MVFR1", addr=0xE000EF44, descr="Media and VFP Feature Register 1", register_bits=[
                RegisterBits(bits=range(28, 32), name="FP fused MAC", descr=""),
                RegisterBits(bits=range(24, 28), name="FP HPFP", descr=""),
                RegisterBits(bits=range(4, 8), name="D_NaN mode,", descr=""),
                RegisterBits(bits=range(0, 4), name="FtZ mode", descr=""),
            ]),
            Register(name="MVFR2", addr=0xE000EF48, descr="Media and VFP Feature Register 2", register_bits=[
                RegisterBits(bits=range(4, 8), name="VFP_Misc", descr=""),
            ]),

        ]
