"""Part of AnalyzerSTM32H743 class."""

from mdutils.mdutils import MdUtils
from emb_spy import ReaderStaticResult


def report_usb(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file: MdUtils,
) -> None:
    """Add "USB" chapter to the report."""
    # Circular import error does not allow importin AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    md_file.new_header(level=1, title="USB")

    # Common (USB1 and USB2) kernel clock source:
    ker_clk_sel = bits_data["RCC_D2CCIP2R.USBSEL"].val
    match ker_clk_sel:
        case 0:
            md_file.new_line("* Kernel clock disabled.")
        case 1:
            md_file.new_line(f"* Kernel clock PLL1.Q, {self.state.pll3_q_freq} Hz.")
        case 2:
            md_file.new_line(f"* Kernel clock PLL3.Q, {self.state.pll3_q_freq} Hz.")
        case 3:
            md_file.new_line(f"* Kernel clock HSI48, {self.state.hsi48_freq} Hz.")

    # USB regulator
    usb_reg_en = bits_data["PWR_CR3.USBREGEN"].val
    if usb_reg_en:
        md_file.new_line("* USB regulator enabled = USB regulator supply")
    else:
        md_file.new_line("* USB regulator disabled = external USB supply")
    md_file.new_line(f"* USB33RDY: {bits_data['PWR_CR3.USB33RDY'].val}")
    md_file.new_line(f"* USB33DEN: {bits_data['PWR_CR3.USB33DEN'].val}")

    md_file.new_line("***")
