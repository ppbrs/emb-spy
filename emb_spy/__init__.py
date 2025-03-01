"""
Expose emb_spy public classes.
"""

from .elf.demangle import demangle
from .elf.elf import Elf
from .elf.elf import ElfInstruction
from .elf.elf import ElfSymbol
from .elf.elf import ElfSymbolDisassembly
from .elf.elf import ElfSymbolName
from .elf.elf import ElfSymbolNameDemangled

_ = demangle
assert type(Elf).__name__ == "type"  # useless check to silence mypy
assert type(ElfInstruction).__name__ == "type"  # useless check to silence mypy
assert type(ElfSymbol).__name__ == "type"  # useless check to silence mypy
assert type(ElfSymbolDisassembly).__name__ == "type"  # useless check to silence mypy
assert type(ElfSymbolName).__name__ == "type"  # useless check to silence mypy
assert type(ElfSymbolNameDemangled).__name__ == "type"  # useless check to silence mypy
