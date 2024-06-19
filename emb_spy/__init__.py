"""
Expose emb_spy public classes.

All lines obviously show "imported but unused" error. It is easier to put :noqa
everywhere than copy-pasting particular disabling code.
"""
from .__about__ import __version__ as __version__

from .app_swo import AppSwo
# Backend
from .backend import Backend
# elf:
from .elf.demangle import demangle
from .elf.elf import Elf
from .elf.elf import ElfInstruction
from .elf.elf import ElfSymbol
from .elf.elf import ElfSymbolDisassembly
from .elf.elf import ElfSymbolName
from .elf.elf import ElfSymbolNameDemangled
#
from .pc_sampler import PCSampler
# reader:
from .reader._reader_core_reg import ReaderConfigCoreReg
from .reader._reader_core_reg import ReaderConfigCoreRegBits
from .reader._reader_memory import ReaderConfigMemory
from .reader._reader_mmap_reg import ReaderConfigMmapReg
from .reader._reader_mmap_reg import ReaderConfigMmapRegBits
from .reader._reader_symbol import ReaderConfigSymbol
from .reader.reader_static import ReaderStatic
from .reader.reader_static import ReaderStaticResult
from .reader._reader_common import ReaderConfig
from .reader._reader_common import SymbolName
# socs
from .socs.arm.armv6_m.stm32f0.stm32f051 import STM32F051
from .socs.arm.armv7e_m.stm32f7.stm32f745 import STM32F745
from .socs.arm.armv7e_m.stm32h7.stm32h743 import STM32H743
from .socs.soc import SoC
# analyzer
# Analyzers use Backend so they should be imported after the Backend is imported.
from .analyzer.analyzer_stm32f051 import AnalyzerSTM32F051  # isort:skip
from .analyzer.analyzer_stm32h743 import AnalyzerSTM32H743  # isort:skip
from .analyzer.analyzer_stm32f745 import AnalyzerSTM32F745  # isort:skip


_ = AnalyzerSTM32F051
_ = AnalyzerSTM32F745
_ = AnalyzerSTM32H743
_ = AppSwo
_ = Backend
_ = demangle
assert type(Elf).__name__ == "type"  # useless check to silence mypy
assert type(ElfInstruction).__name__ == "type"  # useless check to silence mypy
assert type(ElfSymbol).__name__ == "type"  # useless check to silence mypy
assert type(ElfSymbolDisassembly).__name__ == "type"  # useless check to silence mypy
assert type(ElfSymbolName).__name__ == "type"  # useless check to silence mypy
assert type(ElfSymbolNameDemangled).__name__ == "type"  # useless check to silence mypy
_ = PCSampler
_ = ReaderConfigCoreReg
_ = ReaderConfigCoreRegBits
_ = ReaderConfigMemory
_ = ReaderConfigMmapReg
_ = ReaderConfigMmapRegBits
_ = ReaderConfigSymbol
_ = ReaderStatic
_ = STM32F051
_ = STM32F745
_ = STM32H743
