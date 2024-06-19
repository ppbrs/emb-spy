"""Create a report about an STM32H743 connected via OpenOCD."""
from __future__ import annotations

import pathlib
import pprint

from mdutils import MdUtils  # type: ignore

from emb_spy import STM32H743
from emb_spy import ReaderStaticResult
from emb_spy.analyzer.analyzer import Analyzer
from emb_spy.analyzer.analyzer_stm32h743._bits_config import get_bits_config
from emb_spy.analyzer.analyzer_stm32h743._report_adc import report_adc
from emb_spy.analyzer.analyzer_stm32h743._report_advanced_control_timers import \
    report_advanced_control_timers
from emb_spy.analyzer.analyzer_stm32h743._report_clock import report_clock
from emb_spy.analyzer.analyzer_stm32h743._report_clock_enable import report_clock_enable
from emb_spy.analyzer.analyzer_stm32h743._report_dac import report_dac
from emb_spy.analyzer.analyzer_stm32h743._report_dma import report_dma
from emb_spy.analyzer.analyzer_stm32h743._report_dma_mux import report_dma_mux
from emb_spy.analyzer.analyzer_stm32h743._report_gpio import get_af_descr
from emb_spy.analyzer.analyzer_stm32h743._report_hrtim import report_hrtim
from emb_spy.analyzer.analyzer_stm32h743._report_quadspi import report_quadspi
from emb_spy.analyzer.analyzer_stm32h743._state import StateSTM32H743


class AnalyzerSTM32H743(Analyzer):
    """Class containing all fucntion necessary for creating a report on an STM32H743 SoC."""

    def __init__(
        self,
        board_cfg: Analyzer.BoardConfig,
        report_file_path: pathlib.PosixPath | None = None,
        server: tuple[str, int] | None = None,
    ) -> None:
        """Prepare the analyzer."""
        super().__init__(board_cfg=board_cfg, report_file_path=report_file_path, server=server)
        self.state = StateSTM32H743()

    def run(
        self,
    ) -> None:
        """Run the analyzer."""
        bits_data = self.read_bits(soc=STM32H743(), config=get_bits_config(self))
        md_file = MdUtils(file_name=str(self.report_file_path), title="STM32H743 Analyzer Report")
        self._report(bits_data=bits_data, md_file=md_file)
        md_file.create_md_file()

    def _report(
        self,
        bits_data: dict[str, ReaderStaticResult],
        md_file
    ) -> None:
        """Analyze bits and write human-readable report to the file."""
        self.state.is_rev_v = bits_data["DBGMCU_IDC.REV_ID"].val == 0x2003

        self.report_environment(md_file)
        self._report_general(bits_data, md_file)

        report_clock(self, bits_data, md_file)
        self.report_systick_stm32(bits_data, md_file)
        self.report_core_armv7e_m(bits_data, md_file)
        self.report_mpu_armv7e_m(bits_data, md_file)
        report_adc(self, bits_data, md_file)
        report_dac(self, bits_data, md_file)
        self.report_gpio_stm32(
            bits_data, md_file, port_list=["A", "B", "C", "D", "F", ], af_descr_getter=get_af_descr)
        report_advanced_control_timers(self, bits_data, md_file)
        report_hrtim(self, bits_data, md_file)
        report_dma(self, bits_data, md_file)
        report_dma_mux(self, bits_data, md_file)
        report_clock_enable(self, bits_data, md_file)
        report_quadspi(self, bits_data, md_file)

        pprint.PrettyPrinter(indent=4, width=40,).pprint(self.state)

    def _report_general(
        self,
        bits_data: dict[str, ReaderStaticResult],
        md_file
    ) -> None:
        flash_size_kb = bits_data["SYS_FLASH_SIZE.F_SIZE"].val
        md_file.new_line(f"Flash size = {flash_size_kb} kB.")

        revision = {
            0x1001: "Revision Z",
            0x1003: "Revision Y",
            0x2001: "Revision X",
            0x2003: "Revision V", }[bits_data["DBGMCU_IDC.REV_ID"].val]
        md_file.new_line(revision)

        package = {
            0b0000: "LQFP100",
            0b0010: "TQFP144",
            0b0101: "TQFP176/UFBGA176",
            0b1000: "LQFP208/TFBGA240", }[bits_data["SYSCFG_PKGR.PKG"].val]
        md_file.new_line(f"Package = {package}.")

        uid0 = bits_data["SYS_UID0.UID0"].val
        uid1 = bits_data["SYS_UID1.UID1"].val
        uid2 = bits_data["SYS_UID2.UID2"].val
        md_file.new_line(f"UID = {uid2:08x} {uid1:08x} {uid0:08x}")

        md_file.new_line("***")
