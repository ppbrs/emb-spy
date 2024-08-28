"""Contains the base class for all analyzers."""
from __future__ import annotations

import abc
import dataclasses
import logging
import pathlib
from datetime import datetime

from emb_spy import Backend
from emb_spy.analyzer.analyzer._read_bits import ConfigType
from emb_spy.analyzer.analyzer._read_bits import read_bits
from emb_spy.analyzer.analyzer._report_clock_enable_stm32 import ClockResetEnableItemStm32
from emb_spy.analyzer.analyzer._report_clock_enable_stm32 import report_clock_enable_stm32
from emb_spy.analyzer.analyzer._report_core_arm import report_core_armv6_m
from emb_spy.analyzer.analyzer._report_core_arm import report_core_armv7e_m
from emb_spy.analyzer.analyzer._report_gpio_stm32 import report_gpio_stm32
from emb_spy.analyzer.analyzer._report_mpu_arm import report_mpu_armv7e_m
from emb_spy.analyzer.analyzer._report_nvic_stm32 import report_nvic_stm32
from emb_spy.analyzer.analyzer._report_systick_stm32 import report_systick_stm32

# Public types:
_ = ClockResetEnableItemStm32
_ = ConfigType


@dataclasses.dataclass
class State:
    """Common parent for all State{SoC} classes."""

    target_name: str | None = None
    target_state: str | None = None
    """debug-running, halted, reset, running, unknown"""


# pylint: disable-next=too-few-public-methods
class Analyzer(abc.ABC):
    """Common functions to all analyzers."""

    __slots__ = ('state', 'report_file_path', 'board_cfg')

    state: State
    report_file_path: pathlib.PosixPath
    board_cfg: Analyzer.BoardConfig

    def __init__(
        self,
        board_cfg: Analyzer.BoardConfig,
        report_file_path: pathlib.PosixPath,
        server: tuple[str, int] | None = None,
    ) -> None:
        """Prepare the analyzer."""
        if report_file_path.exists():
            logging.warning("`%s` report file already exists", report_file_path)
        self.report_file_path = report_file_path
        self.board_cfg = board_cfg
        self.server = ("localhost", Backend.find_openocd_telnet_port()) if server is None else server

    @dataclasses.dataclass
    class BoardConfig:
        """Information about the environment around the SoC of interest."""

        jtag_target_name: str | None = None
        """
        This can be left unassigned (None) if there is only one SoC in the JTAG chain; however,
        if there is more than one, a specific name should be chosen, otherwise the default
        target will be used.
        """
        resonator_freq: int | float | None = None
        """External crystal/resonator frequency in Hz."""
        external_freq: int | float | None = None
        """External clock frequency in Hz."""

    def report_environment(self, md_file) -> None:
        """Add information when the report was created."""
        now = datetime.today().strftime("on %a %Y-%m-%d at %H:%M:%S.%f")
        md_file.new_line(f"Created {now}.")
        # target_name = self.board_cfg.jtag_target_name
        # if target_name is not None:
        md_file.new_line(f"Target: {self.state.target_name}, {self.state.target_state}.")
        md_file.new_line("***")

    def read_bits(self, *arg, **kwarg):
        """Connect to the target and read all the required registers."""
        return read_bits(self, *arg, **kwarg)

    def report_gpio_stm32(self, *arg, **kwarg):
        """Add a GPIO chapter to the report."""
        return report_gpio_stm32(self, *arg, **kwarg)

    def report_systick_stm32(self, *arg, **kwarg):
        """Add a System Timer chapter to the report."""
        return report_systick_stm32(self, *arg, **kwarg)

    def report_clock_enable_stm32(self, *arg, **kwarg):
        """Add a table to the report showing which peripherals are being clocked or held reset."""
        return report_clock_enable_stm32(self, *arg, **kwarg)

    def report_core_armv7e_m(self, *arg, **kwarg):
        """Add a System Timer chapter to the report."""
        return report_core_armv7e_m(self, *arg, **kwarg)

    def report_core_armv6_m(self, *arg, **kwarg):
        """Add "Core" chapter to the report."""
        return report_core_armv6_m(self, *arg, **kwarg)

    def report_nvic_stm32(self, *arg, **kwarg):
        """Add "System Timer" chapter to the report."""
        return report_nvic_stm32(self, *arg, **kwarg)

    def report_mpu_armv7e_m(self, *arg, **kwarg):
        """Add a "MPU" chapter to the report."""
        return report_mpu_armv7e_m(self, *arg, **kwarg)
