"""Part of AnalyzerSTM32H743 class."""

from emb_spy import ReaderStaticResult


def report_basic_timers(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file,
) -> None:
    """Add "HRTIM" chapter to the report."""
    # Circular import error does not allow importin AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    md_file.new_header(level=1, title="TIM6")
    tim6_clock_enabled = bits_data["RCC_APB1LENR.TIM6EN"].val != 0
    if tim6_clock_enabled:
        md_file.new_line("* clock enabled")
        _report_basic_timer(
            bits_data=bits_data, md_file=md_file, pref="TIM6", timx_freq=self.state.timx_freq
        )
    else:
        md_file.new_line("* clock disabled")
    md_file.new_line("***")

    md_file.new_header(level=1, title="TIM7")
    tim7_clock_enabled = bits_data["RCC_APB1LENR.TIM7EN"].val != 0
    if tim7_clock_enabled:
        md_file.new_line("* clock enabled")
        _report_basic_timer(
            bits_data=bits_data, md_file=md_file, pref="TIM7", timx_freq=self.state.timx_freq
        )
    else:
        md_file.new_line("* clock disabled")

    md_file.new_line("***")


def _report_basic_timer(
    bits_data: dict[str, ReaderStaticResult], md_file, pref: str, timx_freq: int
) -> None:
    cen = bits_data[f"{pref}_CR1.CEN"].val
    md_file.new_line(f"* counter {'enabled' if cen else 'disabled'}")

    psc = bits_data[f"{pref}_PSC.PSC"].val
    freq = timx_freq / (psc + 1)
    md_file.new_line(f"* frequency {timx_freq} / ({psc + 1}) = {freq}")

    arr = bits_data[f"{pref}_ARR.ARR"].val
    md_file.new_line(f"* ARR = {arr}, updates once per {arr / freq} s")

    cnt = bits_data[f"{pref}_CNT.CNT"].val
    md_file.new_line(f"* CNT = {cnt}")
