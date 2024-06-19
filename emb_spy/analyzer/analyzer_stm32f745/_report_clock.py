"""Part of AnalyzerSTM32F745 class."""
from emb_spy import StaticReader


def _report_clock(
    self,  # : AnalyzerSTM32F745
    bits_data: dict[str, StaticReader.Result],
    md_file
) -> None:
    # Circular import error does not allow importin AnalyzerSTM32F745 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32F745"

    md_file.new_header(level=1, title="Clock")

    hsi_rdy = bits_data["RCC_CR.HSIRDY"].val
    hsi_on = bits_data["RCC_CR.HSION"].val
    if hsi_on and hsi_rdy:
        raise NotImplementedError
        # hsi_div = {0b00: 1, 0b01: 2, 0b10: 4, 0b11: 8, }[bits_data["RCC_CR.HSIDIV"].val]
        # self.state.hsi_freq = 64e6 / hsi_div
        # md_file.new_line(
        #   f"* HSI is ON and ready, 64Mhz / {hsi_div} = {self.state.hsi_freq / 1e6} MHz.")
    md_file.new_line("* HSI is OFF or not ready")

    hse_rdy = bits_data["RCC_CR.HSERDY"].val
    hse_on = bits_data["RCC_CR.HSEON"].val
    if hse_on and hse_rdy:
        hse_cs_on = bits_data["RCC_CR.CSSON"].val
        hse_bypass = bits_data["RCC_CR.HSEBYP"].val
        if hse_bypass:
            if not isinstance(hse_freq := self.board_cfg.external_freq, int | float):
                raise ValueError("Valid `external_freq` is required.")
            md_file.new_line(f"HSE is ON and ready, external clock source, {hse_freq / 1e6}MHz.")
        else:
            if not isinstance(hse_freq := self.board_cfg.resonator_freq, int | float):
                raise ValueError("Valid `resonator_freq` is required.")
            md_file.new_line(
                f"* HSE is ON and ready, crystal/ceramic resonator, {hse_freq / 1e6} MHz.")
        self.state.hse_freq = hse_freq
        if hse_cs_on:
            md_file.new_line(
                "\t* Clock Security System (CSS) is " + ("ON" if hse_cs_on else "OFF") + " on HSE.")
    else:
        md_file.new_line("* HSE is OFF or not ready")

    md_file.new_line("***")
