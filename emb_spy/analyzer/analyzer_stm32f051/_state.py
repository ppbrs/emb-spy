"""Part of AnalyzerSTM32F051."""
import dataclasses

from emb_spy.analyzer.analyzer import State

Frequency = int | float | None


@dataclasses.dataclass
class StateSTM32F051(State):
    """
    If any value is None, this means it is not known yet.
    """

    hsi_freq: Frequency = None
    sys_freq: Frequency = None
    # ahb_freq: Frequency = None
    pclk_freq: Frequency = None
    cpu_freq: Frequency = None
