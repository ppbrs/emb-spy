"""Part of AnalyzerSTM32H743 class."""

from mdutils.mdutils import MdUtils  # type: ignore
from emb_spy import ReaderStaticResult


def report_advanced_control_timers(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file: MdUtils,
) -> None:
    """Add "Advanced-control timers" chapter to the report."""
    # Circular import error does not allow importin AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    md_file.new_header(level=1, title="Advanced-control timers")
    md_file.new_line(f"* TIMx clock: {self.state.timx_freq / 1e6} MHz.")

    _report_advanced_control_timer(self, bits_data=bits_data, idx=1, md_file=md_file)
    _report_advanced_control_timer(self, bits_data=bits_data, idx=8, md_file=md_file)


def _report_advanced_control_timer(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    idx: int,
    md_file: MdUtils,
) -> None:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"
    assert idx in (1, 8)
    tim = f"TIM{idx}"

    enabled = bits_data[f"{tim}_CR1.CEN"].val
    if not enabled:
        md_file.new_header(level=2, title=tim + " (disabled)")
        md_file.new_line("***")
        return

    md_file.new_header(level=2, title=tim)
    md_file.new_line("* enabled")

    arr = bits_data[f"{tim}_ARR.ARR"].val
    freq = self.state.timx_freq / (arr + 1)
    period = 1 / freq
    md_file.new_line(f"* ARR = {arr} = {freq} Hz = {round(period * 1e9)} ns")

    # Slave mode
    sms = bits_data[f"{tim}_SMCR.SMS"].val
    match sms:
        case 0b000:
            md_file.new_line("* Slave mode: disabled")
        case 0b0001:
            md_file.new_line("* Slave mode: Encoder mode 1")
        case 0b0010:
            md_file.new_line("* Slave mode: Encoder mode 2")
        case 0b0011:
            md_file.new_line("* Slave mode: Encoder mode 3")
        case 0b0100:
            md_file.new_line("* Slave mode: Reset Mode")
        case 0b0101:
            md_file.new_line("* Slave mode: Gated Mode")
        case 0b0110:
            md_file.new_line("* Slave mode: Trigger Mode")
        case 0b0111:
            md_file.new_line("* Slave mode: External Clock Mode 1")
        case 0b1000:
            md_file.new_line("* Slave mode: Combined reset + trigger mode")
        case _:
            raise ValueError(f"{tim}_SMSR.SMS")
    if sms in {0b0110, 0b1000}:
        ts = bits_data[f"{tim}_SMCR.TS"].val
        match ts:
            case 0b00000:
                md_file.new_line("\t* Internal Trigger 0 (ITR0)")
            case 0b00001:
                md_file.new_line("\t* Internal Trigger 1 (ITR1)")
            case 0b00010:
                md_file.new_line("\t* Internal Trigger 2 (ITR2)")
            case 0b00011:
                md_file.new_line("\t* Internal Trigger 3 (ITR3)")
            case 0b00100:
                md_file.new_line("\t* TI1 Edge Detector (TI1F_ED)")
            case 0b00101:
                md_file.new_line("\t* Filtered Timer Input 1 (TI1FP1)")
            case 0b00110:
                md_file.new_line("\t* Filtered Timer Input 2 (TI2FP2)")
            case 0b00111:
                md_file.new_line("\t* External Trigger input (ETRF)")
            case _:
                raise ValueError(f"{tim}_SMSR.TS")

    # Master mode
    trgo = bits_data[f"{tim}_CR2.MMS"].val
    match trgo:
        case 0b000:
            md_file.new_line(
                "* Master mode - trigger output TRGO: "
                "0: Reset - the UG bit from the TIMx_EGR register is used as TRGO."
            )
        case 0b001:
            md_file.new_line(
                "* Master mode - trigger output TRGO: "
                "1: Enable - the Counter Enable signal CNT_EN is used as TRGO."
            )
        case 0b010:
            md_file.new_line(
                "* Master mode - trigger output TRGO: "
                "2: Update - The update event is selected as TRGO."
            )
        case 0b011:
            md_file.new_line(
                "* Master mode - trigger output TRGO: "
                "3: Compare Pulse - The trigger output send a positive pulse when the CC1IF flag "
                "is to be set as soon as a capture or a compare match occurred."
            )
        case 0b100:
            md_file.new_line(
                "* Master mode - trigger output TRGO: 4: Compare - OC1REFC signal is used as TRGO"
            )
        case 0b101:
            md_file.new_line(
                "* Master mode - trigger output TRGO: 5: Compare - OC2REFC signal is used as TRGO"
            )
        case 0b110:
            md_file.new_line(
                "* Master mode - trigger output TRGO: 6: Compare - OC3REFC signal is used as TRGO"
            )
        case 0b111:
            md_file.new_line(
                "* Master mode - trigger output TRGO: 7: Compare - OC4REFC signal is used as TRGO"
            )
        case _:
            raise ValueError(f"{tim}_CR2.MMS")

    md_file.new_line("***")
