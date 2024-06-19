"""Part of AnalyzerSTM32H743 class."""
from emb_spy import ReaderStaticResult


def report_dac(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    """Add "ADC" chapter to the report."""
    # Circular import error does not allow importin AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"
    _report_dac1(self, bits_data, md_file)
    _report_dac2(self, bits_data, md_file)


def _report_dac1(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    md_file.new_header(level=1, title="DAC1")
    ena = bits_data["DAC_CR.EN1"].val
    if ena == 0:
        md_file.new_line("* DAC1 disabled")
        md_file.new_line("***")
        return

    md_file.new_line("* DAC1 enabled")
    mode_descr = {
        0b000: "Normal mode, connected to external pin with Buffer enabled",
        0b001: "Normal mode, connected to external pin and to on chip peripherals with Buffer enabled",
        0b010: "Normal mode, connected to external pin with Buffer disabled",
        0b011: "Normal mode, connected to on chip peripherals with Buffer disabled",
        0b100: "Sample & hold mode, connected to external pin with Buffer enabled",
        0b101: "Sample & hold mode, connected to external pin and to on chip peripherals with Buffer enabled",
        0b110: "Sample & hold mode, connected to external pin and to on chip peripherals with Buffer disabled",
        0b111: "Sample & hold mode, connected to on chip peripherals with Buffer disabled",
    }[bits_data["DAC_MCR.MODE1"].val]
    md_file.new_line(f"* {mode_descr}")
    md_file.new_line("***")


def _report_dac2(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    md_file.new_header(level=1, title="DAC2")
    ena = bits_data["DAC_CR.EN2"].val
    if ena == 0:
        md_file.new_line("* DAC2 disabled")
        md_file.new_line("***")
        return

    md_file.new_line("* DAC2 enabled")
    mode_descr = {
        0b000: "Normal mode, connected to external pin with Buffer enabled",
        0b001: "Normal mode, connected to external pin and to on chip peripherals with Buffer enabled",
        0b010: "Normal mode, connected to external pin with Buffer disabled",
        0b011: "Normal mode, connected to on chip peripherals with Buffer disabled",
        0b100: "Sample & hold mode, connected to external pin with Buffer enabled",
        0b101: "Sample & hold mode, connected to external pin and to on chip peripherals with Buffer enabled",
        0b110: "Sample & hold mode, connected to external pin and to on chip peripherals with Buffer disabled",
        0b111: "Sample & hold mode, connected to on chip peripherals with Buffer disabled",
    }[bits_data["DAC_MCR.MODE2"].val]
    md_file.new_line(f"* {mode_descr}")

    md_file.new_line("***")
