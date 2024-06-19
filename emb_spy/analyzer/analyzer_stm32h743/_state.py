"""Part of AnalyzerSTM32H743 class."""
import dataclasses

from emb_spy.analyzer.analyzer import State

Frequency = int | float | None
"""
Frequency type.
If the value is None, this means it is not known yet; otherwise, the value is in Hz.
"""


@dataclasses.dataclass
class StateSTM32H743(State):
    """An object of this class is populated with values while the Analyzer runs."""

    is_rev_v: bool | None = None

    hse_freq: Frequency = None

    hsi_freq: Frequency = None

    per_freq: Frequency = None
    """per_ck frequency, in Hz."""

    ref1_freq: Frequency = None
    """PLL1 input in Hz; must be from 1 to 16 MHz."""
    ref2_freq: Frequency = None
    """PLL2 input in Hz; must be from 1 to 16 MHz."""
    ref3_freq: Frequency = None
    """PLL3 input in Hz; must be from 1 to 16 MHz."""

    pll1_p_freq: Frequency = None
    """PLL1-P output in Hz."""
    pll1_q_freq: Frequency = None
    """PLL1-Q output in Hz."""
    pll1_r_freq: Frequency = None
    """PLL1-R output in Hz."""

    pll2_p_freq: Frequency = None
    """PLL2-P output in Hz."""
    pll2_q_freq: Frequency = None
    """PLL2-Q output in Hz."""
    pll2_r_freq: Frequency = None
    """PLL2-R output in Hz."""

    pll3_p_freq: Frequency = None
    """PLL3-P output in Hz."""
    pll3_q_freq: Frequency = None
    """PLL3-Q output in Hz."""
    pll3_r_freq: Frequency = None
    """PLL1-R output in Hz."""

    pll1_vco_freq: Frequency = None
    """PLL1-VCO in Hz."""
    pll2_vco_freq: Frequency = None
    """PLL1-VCO in Hz."""
    pll3_vco_freq: Frequency = None
    """PLL1-VCO in Hz."""

    adc_ker_input_freq: Frequency = None
    """ADC kernel clock input, which is common for all ADCs."""
    adc12_ker_freq: Frequency = None
    adc3_ker_freq: Frequency = None

    sys_freq: Frequency = None
    systick_freq: Frequency = None

    mco1_freq: Frequency = None
    mco2_freq: Frequency = None

    cpu_freq: Frequency = None

    axi_freq: Frequency = None
    ahb1_freq: Frequency = None
    ahb2_freq: Frequency = None
    ahb3_freq: Frequency = None
    ahb4_freq: Frequency = None
    apb1_freq: Frequency = None
    apb2_freq: Frequency = None
    apb3_freq: Frequency = None
    apb4_freq: Frequency = None

    timx_freq: Frequency = None
    """Advanced-control timers (TIM1/TIM8) frequency."""
    timy_freq: Frequency = None
    """General-purpose timers (other than TIM1/TIM8) frequency."""
    hrtim_freq: Frequency = None
    """High-resolution timer frequency."""

    quadspi_ker_freq: Frequency = None
