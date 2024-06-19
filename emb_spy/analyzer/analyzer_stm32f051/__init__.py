"""Create a report about an STM32F051 connected via OpenOCD."""
from __future__ import annotations

import logging
import pathlib
import pprint

from mdutils import MdUtils  # type: ignore

from emb_spy import STM32F051
from emb_spy import ReaderStaticResult
from emb_spy.analyzer.analyzer import Analyzer
from emb_spy.analyzer.analyzer_stm32f051._bits_config import _get_bits_config
from emb_spy.analyzer.analyzer_stm32f051._report_clock import report_clock
from emb_spy.analyzer.analyzer_stm32f051._report_clock_enable import report_clock_enable
from emb_spy.analyzer.analyzer_stm32f051._report_gpio import _get_af_descr
from emb_spy.analyzer.analyzer_stm32f051._report_nvic import report_nvic
from emb_spy.analyzer.analyzer_stm32f051._report_usart import report_usart
from emb_spy.analyzer.analyzer_stm32f051._state import StateSTM32F051


# pylint: disable-next=too-few-public-methods
class AnalyzerSTM32F051(Analyzer):
    """Class containing all fucntion necessary for creating a report on an STM32F051 SoC."""

    def __init__(
        self,
        board_cfg: Analyzer.BoardConfig,
        report_file_path: pathlib.PosixPath,
        server: tuple[str, int] | None = None,
    ) -> None:
        """Prepare the analyzer."""
        super().__init__(board_cfg=board_cfg, report_file_path=report_file_path, server=server)
        self.state = StateSTM32F051()

    def run(self) -> None:
        """Run the analyzer."""
        bits_data = self.read_bits(soc=STM32F051(), config=_get_bits_config(self))
        md_file = MdUtils(file_name=str(self.report_file_path), title="STM32F051 Analyzer Report")
        self._report(bits_data=bits_data, md_file=md_file)
        md_file.create_md_file()

    def _report(
        self,
        bits_data: dict[str, ReaderStaticResult],
        md_file
    ) -> None:
        """Analyze bits and write human-readable report to the file."""
        self.report_environment(md_file)
        self.report_core_armv6_m(bits_data, md_file)
        self.report_gpio_stm32(
            bits_data, md_file, port_list=["A", "B", "C"], af_descr_getter=_get_af_descr)
        report_clock(self, bits_data, md_file)
        report_clock_enable(self, bits_data, md_file)
        self.report_systick_stm32(bits_data, md_file)
        report_nvic(self, bits_data, md_file)
        report_usart(self, idx=2, bits_data=bits_data, md_file=md_file)

        pprint.PrettyPrinter(indent=4, width=40,).pprint(self.state)


def main():
    """Run the analyzer."""
    logging.basicConfig(level=logging.INFO)

    board_cfg = Analyzer.BoardConfig(
        jtag_target_name="stm32f0x.cpu",
    )
    AnalyzerSTM32F051(
        board_cfg=board_cfg,
        report_file_path=pathlib.PosixPath("analyzer_stm32f051.md"),
    ).run()


if __name__ == "__main__":
    main()
