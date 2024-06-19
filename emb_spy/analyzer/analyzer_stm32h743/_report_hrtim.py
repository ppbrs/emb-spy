"""Part of AnalyzerSTM32H743 class."""
from emb_spy import ReaderStaticResult


def report_hrtim(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
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
    else:
        md_file.new_line("* Timer A disabled")

    if tmr_b_en:
        md_file.new_line("* Timer B enabled")
    else:
        md_file.new_line("* Timer B disabled")

    if tmr_c_en:
        md_file.new_line("* Timer C enabled")
    else:
        md_file.new_line("* Timer C disabled")

    if tmr_d_en:
        md_file.new_line("* Timer D enabled")
    else:
        md_file.new_line("* Timer D disabled")

    if tmr_e_en:
        md_file.new_line("* Timer E enabled")
    else:
        md_file.new_line("* Timer E disabled")

    md_file.new_line("***")
