"""Part of Analyzer class."""
import inspect

from emb_spy import ReaderStaticResult


def report_systick_stm32(
    self,
    bits_data: dict[str, ReaderStaticResult],
    md_file,
) -> None:
    """Add a System Timer chapter to the report."""
    assert "Analyzer" in [cls.__name__ for cls in inspect.getmro(self.__class__)]
    # which is basically the same as issublass(self.__class__, Analyzer).

    enabled = bits_data["SYST_CSR.ENABLE"].val
    if not enabled:
        md_file.new_header(level=1, title="SysTick (System Timer) - disabled")
        md_file.new_line("***")
        return

    md_file.new_header(level=1, title="SysTick (System Timer)")
    current = bits_data["SYST_CVR.CURRENT"].val
    md_file.new_line(f"* Timer enabled. Current value = {current}.")

    src = bits_data["SYST_CSR.CLKSOURCE"].val
    if src == 0:
        systick_freq = self.state.systick_freq
        md_file.new_line(f"* Clock source = external clock, {systick_freq / 1e6} MHz")
    else:
        systick_freq = getattr(self.state, "sys_freq", None)
        if systick_freq is None:
            return  # todo
        md_file.new_line(f"* Clock source = processor clock, {systick_freq / 1e6} MHz")

    period_ticks = bits_data["SYST_RVR.RELOAD"].val + 1
    period = period_ticks / systick_freq
    freq = 1 / period
    md_file.new_line(f"* Reload frequency: {freq} Hz.")
    md_file.new_line(f"* Reload period: {period_ticks} ticks = {round(period * 1e9)} ns.")

    exception = bits_data["SYST_CSR.TICKINT"].val
    if exception:
        md_file.new_line("* SysTick exception enabled.")
    else:
        md_file.new_line("* SysTick exception disabled.")

    noref = bits_data["SYST_CALIB.NOREF"].val
    skew = bits_data["SYST_CALIB.SKEW"].val
    tenms = bits_data["SYST_CALIB.TENMS"].val
    md_file.new_line(f"* Calibration: NOREF={noref}, SKEW={skew}, TENMS={tenms}")

    md_file.new_line("***")
