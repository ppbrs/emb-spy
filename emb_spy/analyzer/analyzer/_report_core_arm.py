"""Part of Analyzer class."""
import inspect

from emb_spy import ReaderStaticResult


def _report_stack(
    bits_data: dict[str, ReaderStaticResult],
    md_file,
) -> None:
    sp_val = bits_data["SP"].val
    msp_val = bits_data["MSP"].val
    psp_val = bits_data["PSP"].val
    spsel_val = bits_data["CONTROL.SPSEL"].val
    md_file.new_line(f"* SP = Stack Pointer = R13 = 0x{sp_val:08x}")
    md_file.new_line(f"\t* MSP = Main Stack Pointer = 0x{msp_val:08x}")
    md_file.new_line(f"\t* PSP = Process Stack Pointer = 0x{psp_val:08x}")
    spsel_descr = {0: "MSP", 1: "PSP"}[spsel_val] + " is the current stack pointer."
    md_file.new_line(f"\t* SPSEL = {spsel_val} = {spsel_descr}")


def _report_pc_lr(
    bits_data: dict[str, ReaderStaticResult],
    md_file,
) -> None:
    pc_val = bits_data["PC"].val
    md_file.new_line(f"* PC = Program Counter = R15 = 0x{pc_val:08x}")
    lr_val = bits_data["LR"].val
    md_file.new_line(f"* LR = Link Register = R14 = 0x{lr_val:08x}")


def report_core_armv7e_m(
    self,
    bits_data: dict[str, ReaderStaticResult],
    md_file,
) -> None:
    """Add a Core chapter to the report."""
    assert "Analyzer" in [cls.__name__ for cls in inspect.getmro(self.__class__)]
    # which is basically the same as issublass(self.__class__, Analyzer).

    md_file.new_header(level=1, title="Core (ARM v7e-m)")

    pcsr = bits_data["DWT_PCSR.EIASAMPLE"].val
    md_file.new_line(f"* PC from PCSR = 0x{pcsr:08x}")

    if self.state.target_state != "halted":
        md_file.new_line(
            f"* Core is {self.state.target_state}. Core must be halted for reading core registers.")
        md_file.new_line("***")
        # return

    _report_pc_lr(bits_data=bits_data, md_file=md_file)
    _report_stack(bits_data=bits_data, md_file=md_file)

    npriv_val = bits_data["CONTROL.nPRIV"].val
    npriv_descr = ("Thread mode privilege level is "
                   + {0: "Privileged.", 1: "Unprivileged."}[npriv_val])
    md_file.new_line(f"* nPRIV = {npriv_val} = {npriv_descr}")

    fpca_val = bits_data["CONTROL.FPCA"].val
    fpca_descr = {
        0: "No floating-point context active.", 1: "Floating-point context active.."}[fpca_val]
    md_file.new_line(f"* FPCA = {fpca_val} = {fpca_descr}")

    def report_exceptions_interrupts() -> None:
        md_file.new_line("* Exceptions and interrupts:")
        primask_val = bits_data["PRIMASK.PRIMASK"].val
        faultmask_val = bits_data["FAULTMASK.FAULTMASK"].val
        basepri_val = bits_data["BASEPRI.BASEPRI"].val
        isr_number_val = bits_data["PSR.IPSR:ISR_NUMBER"].val
        primask_descr = {
            0: "No effect.",
            1: "Prevents the activation of all exceptions with configurable priority.",
        }[primask_val]
        md_file.new_line(f"\t* PRIMASK = {primask_val} = {primask_descr}")
        faultmask_descr = {
            0: "No effect.",
            1: "Prevents the activation of all exceptions except for NMI.",
        }[faultmask_val]
        md_file.new_line(f"\t* FAULTMASK = {faultmask_val} = {faultmask_descr}")
        if basepri_val == 0:
            basepri_descr = "No effect."
        else:
            basepri_descr = ("The processor does not process any exception "
                             f"with a priority value ≥ {basepri_val}.")
        md_file.new_line(f"\t* BASEPRI = {basepri_val} = {basepri_descr}")
        isr_number_options = {
            0: "Thread mode.",
            2: "NMI.",
            3: "HardFault.",
            4: "MemManage.",
            5: "BusFault.",
            6: "UsageFault.",
            11: "SVCall.",
            14: "PendSV.",
            15: "SysTick.",
        }
        for irqn in range(0, 240):
            isr_number_options[16 + irqn] = f"IRQ{irqn}"
        md_file.new_line(
            f"\t* ISR_NUMBER = {isr_number_val} = {isr_number_options[isr_number_val]}")
    report_exceptions_interrupts()

    def report_apsr_epsr() -> None:
        md_file.new_line("* APSR = Application status:")
        n_val = bits_data["PSR.APSR:N"].val
        z_val = bits_data["PSR.APSR:Z"].val
        c_val = bits_data["PSR.APSR:C"].val
        v_val = bits_data["PSR.APSR:V"].val
        q_val = bits_data["PSR.APSR:Q"].val
        ge_val = bits_data["PSR.APSR:GE"].val
        md_file.new_line(f"\t* N = Negative flag = {n_val}")
        md_file.new_line(f"\t* Z = Zero flag = {z_val}")
        md_file.new_line(f"\t* C = Carry or borrow flag = {c_val}")
        md_file.new_line(f"\t* V = Overflow flag = {v_val}")
        md_file.new_line(f"\t* Q = DSP overflow and saturation flag = {q_val}")
        md_file.new_line(f"\t* GE = Greater than or Equal flags = {ge_val}")

        md_file.new_line("* EPSR = Execution status:")
        ici_it_val = bits_data["PSR.EPSR:ICI/IT"].val
        thumb_val = bits_data["PSR.EPSR:T"].val
        md_file.new_line(
            f"\t* ICI/IT = Interruptible-continuable instruction / = IT instruction = {ici_it_val}")
        md_file.new_line(f"\t* T = Thumb state = {thumb_val}")
    report_apsr_epsr()

    md_file.new_line("***")

    icache_ena = bits_data["SCB_CCR.IC"].val
    dcache_ena = bits_data["SCB_CCR.DC"].val
    md_file.new_line("* I-Cache " + ("enabled" if icache_ena else "disabled"))
    md_file.new_line("* D-Cache " + ("enabled" if dcache_ena else "disabled"))

    md_file.new_line("***")


def report_core_armv6_m(
    self,
    bits_data: dict[str, ReaderStaticResult],
    md_file,
) -> None:
    """Add a System Timer chapter to the report."""
    assert "Analyzer" in [cls.__name__ for cls in inspect.getmro(self.__class__)]
    # which is basically the same as issublass(self.__class__, Analyzer).

    md_file.new_header(level=1, title="Core (ARM v6-m)")

    pcsr = bits_data["DWT_PCSR.EIASAMPLE"].val
    md_file.new_line(f"* PC from PCSR = 0x{pcsr:08x}")

    if self.state.target_state != "halted":
        md_file.new_line(
            f"* Core is {self.state.target_state}. Core must be halted for reading core registers.")
        md_file.new_line("***")
        return

    _report_pc_lr(bits_data=bits_data, md_file=md_file)
    _report_stack(bits_data=bits_data, md_file=md_file)

    def report_exceptions_interrupts() -> None:
        md_file.new_line("* Exceptions and interrupts:")
        primask_val = bits_data["PRIMASK.PRIMASK"].val
        isr_number_val = bits_data["PSR.IPSR:ExceptionNumber"].val
        primask_descr = {
            0: "No effect.",
            1: "Prevents the activation of all exceptions with configurable priority.",
        }[primask_val]
        md_file.new_line(f"\t* PRIMASK = {primask_val} = {primask_descr}")
        isr_number_options = {
            0: "Thread mode.",
            2: "NMI.",
            3: "HardFault.",
            11: "SVCall.",
            14: "PendSV.",
            15: "SysTick.",
        }
        for irqn in range(0, 32):
            isr_number_options[16 + irqn] = f"IRQ{irqn}"
        md_file.new_line(
            f"\t* ISR_NUMBER = {isr_number_val} = {isr_number_options[isr_number_val]}")
    report_exceptions_interrupts()

    def report_apsr_epsr() -> None:
        md_file.new_line("* APSR = Application status:")
        n_val = bits_data["PSR.APSR:N"].val
        z_val = bits_data["PSR.APSR:Z"].val
        c_val = bits_data["PSR.APSR:C"].val
        v_val = bits_data["PSR.APSR:V"].val
        md_file.new_line(f"\t* N = Negative flag = {n_val}")
        md_file.new_line(f"\t* Z = Zero flag = {z_val}")
        md_file.new_line(f"\t* C = Carry or borrow flag = {c_val}")
        md_file.new_line(f"\t* V = Overflow flag = {v_val}")

        md_file.new_line("* EPSR = Execution status:")
        thumb_val = bits_data["PSR.EPSR:T"].val
        md_file.new_line(f"\t* T = Thumb state = {thumb_val}")
    report_apsr_epsr()

    md_file.new_line("***")
