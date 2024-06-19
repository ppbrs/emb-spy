"""Create a report about an STM32F745 connected via OpenOCD."""
from __future__ import annotations

import logging
import pathlib
import pprint

from mdutils import MdUtils  # type: ignore

from emb_spy import STM32F745
from emb_spy import ReaderStaticResult
from emb_spy.analyzer.analyzer import Analyzer
from emb_spy.analyzer.analyzer_stm32f745._bits_config import _get_bits_config
from emb_spy.analyzer.analyzer_stm32f745._report_clock import _report_clock
from emb_spy.analyzer.analyzer_stm32f745._report_gpio import _get_af_descr
from emb_spy.analyzer.analyzer_stm32f745._report_nvic import report_nvic
from emb_spy.analyzer.analyzer_stm32f745._state import StateSTM32F745


class AnalyzerSTM32F745(Analyzer):
    """Class containing all fucntion necessary for creating a report on an STM32F745 SoC."""

    def __init__(
        self,
        board_cfg: Analyzer.BoardConfig,
        report_file_path: pathlib.PosixPath | None = None,
        server: tuple[str, int] | None = None,
    ) -> None:
        """Prepare the analyzer."""
        super().__init__(board_cfg=board_cfg, report_file_path=report_file_path, server=server)
        self.state = StateSTM32F745()

    def run(
        self,
    ) -> None:
        """Run the analyzer."""
        bits_data = self.read_bits(soc=STM32F745(), config=_get_bits_config(self))
        md_file = MdUtils(file_name=str(self.report_file_path), title="STM32F745 Analyzer Report")
        self._report(bits_data=bits_data, md_file=md_file)
        md_file.create_md_file()

    def _report(
        self,
        bits_data: dict[str, ReaderStaticResult],
        md_file
    ) -> None:
        """Analyze bits and write human-readable report to the file."""
        # self.state.is_rev_v = bits_data["DBGMCU_IDC.REV_ID"].val == 0x2003

        self.report_environment(md_file)
        # self._report_general(bits_data, md_file)

        _report_clock(self, bits_data, md_file)
        self.report_systick_stm32(bits_data, md_file)
        self.report_core_armv7e_m(bits_data, md_file)

        self.report_gpio_stm32(
            bits_data=bits_data,
            md_file=md_file,
            port_list=["A", "B", "C", "D", "E"],
            af_descr_getter=_get_af_descr,
        )
        report_nvic(self, bits_data, md_file)

        # _report_clock(self, bits_data, md_file)
        # _report_adc(self, bits_data, md_file)

        # _report_advanced_control_timers(self, bits_data, md_file)
        # _report_dma(self, bits_data, md_file)
        # _report_dma_mux(self, bits_data, md_file)
        # _report_clock_enable(self, bits_data, md_file)

        pprint.PrettyPrinter(indent=4, width=40,).pprint(self.state)
