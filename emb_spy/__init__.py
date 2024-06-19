"""
Expose emb_spy public classes.

All lines obviously show "imported but unused" error. It is easier to put :noqa
everywhere than copy-pasting particular disabling code.
"""
from .app_swo import AppSwo  # noqa
from .backend import Backend  # noqa
from .reader.dynamic_reader import DynamicReader  # noqa
from .reader.static_reader import StaticReader  # noqa
from .reader._reader_core_reg import ReaderConfigCoreReg, ReaderConfigCoreRegBits  # noqa
from .reader._reader_memory import ReaderConfigMemory  # noqa
from .reader._reader_mmap_reg import ReaderConfigMmapReg, ReaderConfigMmapRegBits  # noqa
from .reader._reader_symbol import ReaderConfigSymbol  # noqa


from .socs.arm.armv6_m.stm32f0.stm32f051 import STM32F051  # noqa
from .socs.arm.armv7e_m.stm32f7.stm32f745 import STM32F745  # noqa
from .socs.arm.armv7e_m.stm32h7.stm32h743 import STM32H743  # noqa

# Analyzers use Backend so it should be imported after it.
from .analyzer.analyzer_stm32f051 import AnalyzerSTM32F051  # noqa isort:skip
from .analyzer.analyzer_stm32h743 import AnalyzerSTM32H743  # noqa isort:skip
from .analyzer.analyzer_stm32f745 import AnalyzerSTM32F745  # noqa isort:skip
