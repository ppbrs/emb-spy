RegName = str
"""
The type of the name of
* a memory mapped register, e.g. "GPIOA_MODER",
* or a subregister, e.g. "GPIOA_MODER.MODER5",
* or a core register, e.g. "r2".
"""

SymbolName = str
"""
The type of the name of a symbol, e.g. "gCounter".
"""

MemAddr = int
"""
Address in memory.
"""

MemData = bytes
"""
The size of it indicates the number of bytes that are needed to read or have been read.
"""


class ReaderConfig:
    """Base class for all configuration objects."""
