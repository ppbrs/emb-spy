"""Part of AnalyzerSTM32H743 class."""

from emb_spy import ReaderStaticResult


def report_advanced_control_timers(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file,
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
    md_file,
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

    md_file.new_line("***")
