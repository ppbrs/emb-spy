"""Part of AnalyzerSTM32F051."""
from emb_spy import ReaderStaticResult


def report_usart(
    self,
    idx: int,
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    """Add USART chapters to the report."""
    assert self.__class__.__name__ == "AnalyzerSTM32F051"
    usart = f"USART{idx}"

    md_file.new_header(level=1, title=usart)

    md_file.new_line(f"* USART clock is {self.state.pclk_freq / 1e6} MHz")

    #
    # General
    #
    ena = bits_data["USART2_CR1.UE"].val
    if not ena:
        md_file.new_line("* USART disabled.")
        md_file.new_line("***")
        return

    md_file.new_line("* USART enabled.")
    brr = bits_data["USART2_BRR.BRR"].val
    over8 = bits_data["USART2_CR1.OVER8"].val
    if over8 == 0:
        baud_bps = self.state.pclk_freq / brr
        md_file.new_line(f"* BRR = {brr}, baud rate = {round(baud_bps, 2)} bps")
    else:
        raise NotImplementedError

    #
    # Receiver
    #
    r_en = bits_data["USART2_CR1.RE"].val
    md_file.new_line("* Receiver")
    md_file.new_line("\t* " + ("Enabled" if r_en else "Disabled."))

    #
    # Transmitter
    #
    t_en = bits_data["USART2_CR1.TE"].val
    md_file.new_line("* Transmitter")
    md_file.new_line("\t* " + ("Enabled" if t_en else "Disabled."))

    isr_tc = bits_data["USART2_ISR.TC"].val
    isr_txe = bits_data["USART2_ISR.TXE"].val
    md_file.new_line(f"\t* TC (Transmission complete) = {isr_tc}")
    md_file.new_line(f"\t* TXE (Transmit data register empty) = {isr_txe}")

    md_file.new_line("***")
