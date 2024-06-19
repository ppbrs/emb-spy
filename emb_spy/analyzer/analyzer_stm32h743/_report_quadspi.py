"""Part of AnalyzerSTM32H743 class."""
from emb_spy import ReaderStaticResult


def report_quadspi(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    """Add "QUADSPI" chapter to the report."""
    # Circular import error does not allow importin AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    md_file.new_header(level=1, title="QUADSPI")

    ck_sel = bits_data["RCC_D1CCIPR.QSPISEL"].val
    if ck_sel == 0b00:
        # 00: rcc_hclk3 clock selected as kernel peripheral clock (default after reset)
        self.state.quadspi_ker_freq = self.state.ahb3_freq
        md_file.new_line(
            f"* QUADSPI kernel input clock is from AHB3: {self.state.quadspi_ker_freq / 1e6} MHz.")
    else:
        raise NotImplementedError
        # 01: pll1_q_ck clock selected as kernel peripheral clock
        # 10: pll2_r_ck clock selected as kernel peripheral clock
        # 11: per_ck clock selected as kernel peripheral clock

    enabled = bits_data["QUADSPI_CR.EN"].val
    md_file.new_line("* Enabled." if enabled else "* Disabled.")

    div = bits_data["QUADSPI_CR.PRESCALER"].val + 1
    clk_freq = self.state.quadspi_ker_freq / div
    md_file.new_line(
        "* QUADSPI CLK frequency = "
        f"{self.state.quadspi_ker_freq / 1e6} MHz / {div} = {clk_freq / 1e6} MHz.")

    fsize = bits_data["QUADSPI_DCR.FSIZE"].val
    fsize_bytes = 2**(fsize + 1)
    md_file.new_line(
        f"* size = 2^({fsize}+1) = {fsize_bytes} B = {round(fsize_bytes / 1024 / 1024, 1)} MB")

    md_file.new_line("***")
