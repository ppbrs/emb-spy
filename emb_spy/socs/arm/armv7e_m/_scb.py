"""Part of ARMV7EM SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg


def init_scb(self) -> None:
    assert self.__class__.__name__ == "ARMV7EM"
    # The System Control Block (SCB) provides system implementation information, and system
    # control. This includes configuration, control, and reporting of the system exceptions.

    # 0xE000E008 ACTLR Auxiliary Control Register
    # 0xE000ED00 CPUID CPUID Base Register
    # 0xE000ED04 ICSRb Interrupt Control and State Register
    # 0xE000ED08 VTOR Vector Table Offset Register
    # 0xE000ED0C AIRCR Application Interrupt and Reset Control Register

    self.append(MmapReg(
        name="SCB_SCR", addr=0xE000ED10, descr="0xE000ED10",
        bits=[
        ],
    ))

    self.append(MmapReg(
        name="SCB_CCR", addr=0xE000ED14, descr="Configuration and Control Register",
        bits=[
            Bits(
                bits=17, name="IC", descr="Enables L1 instruction cache."),
            Bits(
                bits=16, name="DC", descr="Enables L1 data cache."),
        ],
    ))

    self.append(MmapReg(
        name="SCB_SHPR1", addr=0xE000ED18, descr="System Handler Priority Register 1",
        bits=[
            Bits(
                bits=range(16, 24), name="PRI_6", descr="Priority of system handler 6, UsageFault"),
            Bits(
                bits=range(8, 16), name="PRI_5", descr="Priority of system handler 5, BusFault"),
            Bits(
                bits=range(0, 8), name="PRI_4", descr="Priority of system handler 4, MemManage"),
        ],
    ))
    self.append(MmapReg(
        name="SCB_SHPR2", addr=0xE000ED1C, descr="System Handler Priority Register 2",
        bits=[
            Bits(bits=range(24, 32), name="PRI_11", descr="Priority of system handler 11, SVCall"),
        ],
    ))
    self.append(MmapReg(
        name="SCB_SHPR3", addr=0xE000ED20, descr="System Handler Priority Register 3",
        bits=[
            Bits(
                bits=range(24, 32), name="PRI_15",
                descr="Priority of system handler 15, SysTick exception"),
            Bits(
                bits=range(16, 24), name="PRI_14",
                descr="Priority of system handler 14, PendSV"),
        ],
    ))
    self.append(MmapReg(
        name="SCB_SHCSR", addr=0xE000ED24, descr="System Handler Control and State Register",
        bits=[
            Bits(
                bits=18, name="USGFAULTENA",
                descr="UsageFault enable bit, set to 1 to enable"),
            Bits(
                bits=17, name="BUSFAULTENA",
                descr="BusFault enable bit, set to 1 to enable"),
            Bits(
                bits=16, name="MEMFAULTENA",
                descr="MemManage enable bit, set to 1 to enable"),
            Bits(
                bits=15, name="SVCALLPENDED",
                descr="SVCall pending bit, reads as 1 if exception is pending"),
            Bits(
                bits=14, name="BUSFAULTPENDED",
                descr="BusFault exception pending bit, reads as 1 if exception is pending"),
            Bits(
                bits=13, name="MEMFAULTPENDED",
                descr="MemManage exception pending bit, reads as 1 if exception is pending"),
            Bits(
                bits=12, name="USGFAULTPENDED",
                descr="UsageFault exception pending bit, reads as 1 if exception is pending"),
            Bits(
                bits=11, name="SYSTICKACT",
                descr="SysTick exception active bit, reads as 1 if exception is active"),
            Bits(
                bits=10, name="PENDSVACT",
                descr="PendSV exception active bit, reads as 1 if exception is active"),
            Bits(
                bits=8, name="MONITORACT",
                descr="Debug monitor active bit, reads as 1 if Debug monitor is active"),
            Bits(
                bits=7, name="SVCALLACT",
                descr="SVCall active bit, reads as 1 if SVC call is active"),
            Bits(
                bits=3, name="USGFAULTACT",
                descr="UsageFault exception active bit, reads as 1 if exception is active"),
            Bits(
                bits=1, name="BUSFAULTACT",
                descr="BusFault exception active bit, reads as 1 if exception is active"),
            Bits(
                bits=0, name="MEMFAULTACT",
                descr="MemManage exception active bit, reads as 1 if exception is active"),
        ],
    ))
    self.append(MmapReg(
        name="SCB_CFSR", addr=0xE000ED28, descr="Configurable Fault Status Register",
        comment="Indicates the cause of a MemManage fault, BusFault, or UsageFault.",
        bits=[
            # Memory management fault:
            Bits(
                bits=range(0, 8), name="MMFSR", descr="Memory Management Fault Status Register.", ),

            Bits(
                bits=7, name="MMFSR:MMARVALID",
                descr="MemManage Fault Address Register (MMFAR) valid flag", ),
            # 0 Value in MMAR is not a valid fault address.
            # 1 MMAR holds a valid fault address.
            # If a MemManage fault occurs and is escalated to a HardFault because of priority,
            # the HardFault handler must set this bit to 0. This prevents problems on return
            # to a stacked active MemManage fault handler whose MMAR value has been overwritten.

            Bits(
                bits=5, name="MMFSR:MLSPERR", ),
            # 0 = No MemManage fault occurred during floating-point lazy state preservation.
            # 1 = A MemManage fault occurred during floating-point lazy state preservation.

            Bits(
                bits=4, name="MMFSR:MSTKERR",
                descr="MemManage fault on stacking for exception entry", ),
            # 0 No stacking fault.
            # 1 Stacking for an exception entry has caused one or more access violations.
            # When this bit is 1, the SP is still adjusted but the values in the context
            # area on the stack might be incorrect. The processor has not written a fault
            # address to the MMAR.

            Bits(
                bits=3, name="MMFSR:MUNSTKERR",
                descr="MemManage fault on unstacking for a return from exception", ),
            # 0 No unstacking fault.
            # 1 Unstack for an exception return has caused one or more access violations.
            # This fault is chained to the handler. This means that when this bit is 1, the
            # original return stack is still present. The processor has not adjusted the SP
            # from the failing return, and has not performed a new save. The processor has
            # not written a fault address to the MMAR.

            Bits(bits=1, name="MMFSR:DACCVIOL", descr="Data access violation flag", ),
            # 0 No data access violation fault.
            # 1 The processor attempted a load or store at a location that does not permit the
            # operation.
            # When this bit is 1, the PC value stacked for the exception return points to the
            # faulting instruction. The processor has loaded the MMAR with the address of
            # the attempted access.

            Bits(
                bits=0, name="MMFSR:IACCVIOL", descr="Instruction access violation flag",
                descr_vals={
                    0: "No instruction access violation fault.",
                    1: "The processor attempted an instruction fetch from a location "
                       "that does not permit execution.",
                }),
            # This fault occurs on any access to an XN region, even when the MPU is disabled
            # or not present.
            # When this bit is 1, the PC value stacked for the exception return points to the
            #  faulting instruction. The processor has not written a fault address to the MMAR.

            # Bust fault:
            Bits(bits=range(8, 16), name="BFSR", descr="Bus Fault Status Register", ),
            Bits(bits=(8 + 7), name="BFSR:BFARVALID", descr="Address Register (BFAR) valid flag", ),
            Bits(bits=(8 + 5), name="BFSR:LSPERR", ),
            Bits(bits=(8 + 4), name="BFSR:STKERR", ),
            Bits(bits=(8 + 3), name="BFSR:UNSTKERR", ),
            Bits(bits=(8 + 2), name="BFSR:IMPRECISERR", ),
            Bits(bits=(8 + 1), name="BFSR:PRECISERR", ),
            Bits(bits=(8 + 0), name="BFSR:IBUSERR", ),

            # Usage fault:
            Bits(bits=range(16, 32), name="UFSR", descr="Usage Fault Status Register"),

            Bits(bits=(16 + 9), name="UFSR:DIVBYZERO"),
            Bits(bits=(16 + 8), name="UFSR:UNALIGNED"),
            Bits(bits=(16 + 3), name="UFSR:NOCP"),
            Bits(bits=(16 + 2), name="UFSR:INVPC"),
            Bits(bits=(16 + 1), name="UFSR:INVSTATE"),
            Bits(bits=(16 + 0), name="UFSR:UNDEFINSTR"),
        ],
    ))
    # 0xE000ED28 MMFSR age Fault Status Register
    self.append(MmapReg(
        name="SCB_HFSR", addr=0xE000ED2C, descr="HardFault Status Register",
        comment="Gives information about events that activate the HardFault handler.",
        bits=[
            Bits(
                bits=1, name="VECTTBL",
                descr="Indicates a BusFault on a vector table read during exception processing.",
                descr_vals={
                    0: "No BusFault on vector table read.",
                    1: "BusFault on vector table read.", }),
            Bits(
                bits=30, name="FORCED",
                descr="Indicates a forced hard fault, generated by escalation of a fault "
                      "with configurable priority that cannot be handled, either because "
                      "of priority or because it is disabled.",
                descr_vals={
                    0: "No forced HardFault.",
                    1: "Forced HardFault.", }),
            Bits(bits=31, name="DEBUGEVT", descr="Reserved for Debug use."),
        ],
    ))
    # 0xE000ED29 BFSR Status Register
    # 0xE000ED2A UFSR eFault Status Register
    # 0xE000ED2C HFSR HardFault Status Register
    # 0xE000ED34 MMFAR MemManage Fault Address Register
    # 0xE000ED38 BFAR BusFault Address Register

    self.append(MmapReg(
        name="SCB_CPACR", addr=0xE000ED88, descr="Coprocessor Access Control Register",
        comment="The CPACR register specifies the access privileges for coprocessors.",
        bits=[
            Bits(
                bits=[20, 21], name="CP10",
                descr="Access privileges for coprocessor 10.",
                descr_vals={
                    0: "Access denied. Any attempted access generates a NOCP UsageFault.",
                    1: "Privileged access only. An unprivileged access generates a NOCP fault.",
                    2: "Reserved. The result of any access is Unpredictable.",
                    3: "Full access.", }
            ),
            Bits(
                bits=[22, 23], name="CP11",
                descr="Access privileges for coprocessor 11.",
                descr_vals={
                    0: "Access denied. Any attempted access generates a NOCP UsageFault.",
                    1: "Privileged access only. An unprivileged access generates a NOCP fault.",
                    2: "Reserved. The result of any access is Unpredictable.",
                    3: "Full access.", }
            ),
        ],
    ))

    self.append(MmapReg(name="MMFSR", addr=0xE000ED28, descr="MemManage Fault Status Register"))
    self.append(MmapReg(name="MMFAR", addr=0xE000ED34, descr="MemManage Fault Address Register"))
