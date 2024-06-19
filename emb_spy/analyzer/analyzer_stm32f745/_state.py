"""Part of AnalyzerSTM32F745 class."""
import dataclasses

from emb_spy.analyzer.analyzer import State

Frequency = int | float | None
"""
Frequency type.
If the value is None, this means it is not known yet; otherwise, the value is in Hz.
"""


@dataclasses.dataclass
class StateSTM32F745(State):
    """An object of this class is populated with values while the Analyzer runs."""

    hse_freq: Frequency = None

    hsi_freq: Frequency = None

    pll_in_freq: Frequency = None
    pll_vco_freq: Frequency = None
    pll_p_freq: Frequency = None
    """Main PLL P output frequency that clocks the system."""
    pll_q_freq: Frequency = None
    """Main PLL Q output frequency that clocks USB OTG FS, SDMMC and random number generator."""

    sys_freq: Frequency = None

    mco1_freq: Frequency = None
    mco2_freq: Frequency = None
