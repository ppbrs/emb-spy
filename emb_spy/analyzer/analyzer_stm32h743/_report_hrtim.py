"""Part of AnalyzerSTM32H743 class."""

from emb_spy import ReaderStaticResult


def report_hrtim(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file,
) -> None:
    """Add "HRTIM" chapter to the report."""
    # Circular import error does not allow importin AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    md_file.new_header(level=1, title="HRTIM")

    master_en = bits_data["HRTIM_MCR.MCEN"].val
    tmr_a_en = bits_data["HRTIM_MCR.TACEN"].val
    tmr_b_en = bits_data["HRTIM_MCR.TBCEN"].val
    tmr_c_en = bits_data["HRTIM_MCR.TCCEN"].val
    tmr_d_en = bits_data["HRTIM_MCR.TDCEN"].val
    tmr_e_en = bits_data["HRTIM_MCR.TECEN"].val

    if master_en:
        md_file.new_line("* Master timer enabled")
    else:
        md_file.new_line("* Master timer disabled")

    if tmr_a_en:
        md_file.new_line("* Timer A enabled")
        cnt = bits_data["HRTIM_CNTAR.CNT"].val
        per = bits_data["HRTIM_PERAR.PER"].val
        ckpsc = bits_data["HRTIM_TIMACR.CKPSC"].val
        match ckpsc:
            case 0b101:
                freq = self.state.hrtim_freq
            case 0b110:
                freq = self.state.hrtim_freq / 2
            case 0b111:
                freq = self.state.hrtim_freq / 4
            case _:
                raise ValueError("HRTIM_TIMACR.CKPSC")
        md_file.new_line(f"\t* {freq} Hz")
        md_file.new_line(f"\t* CNT = {cnt}, PER = {per} = {freq / per} Hz")
    else:
        md_file.new_line("* Timer A disabled")

    if tmr_b_en:
        md_file.new_line("* Timer B enabled")
        cnt = bits_data["HRTIM_CNTBR.CNT"].val
        per = bits_data["HRTIM_PERBR.PER"].val
        md_file.new_line(f"\t* CNT = {cnt}, PER = {per}")
    else:
        md_file.new_line("* Timer B disabled")

    if tmr_c_en:
        md_file.new_line("* Timer C enabled")
        cnt = bits_data["HRTIM_CNTCR.CNT"].val
        per = bits_data["HRTIM_PERCR.PER"].val
        md_file.new_line(f"\t* CNT = {cnt}, PER = {per}")
    else:
        md_file.new_line("* Timer C disabled")

    if tmr_d_en:
        md_file.new_line("* Timer D enabled")
        cnt = bits_data["HRTIM_CNTDR.CNT"].val
        per = bits_data["HRTIM_PERDR.PER"].val
        md_file.new_line(f"\t* CNT = {cnt}, PER = {per}")
    else:
        md_file.new_line("* Timer D disabled")

    if tmr_e_en:
        cnt = bits_data["HRTIM_CNTER.CNT"].val
        per = bits_data["HRTIM_PERER.PER"].val
        md_file.new_line(f"\t* CNT = {cnt}, PER = {per}")
        md_file.new_line("* Timer E enabled")
    else:
        md_file.new_line("* Timer E disabled")

    md_file.new_line("***")
