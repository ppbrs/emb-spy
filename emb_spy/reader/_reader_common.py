

Name = str
"""
Name of
* a memory mapped register, e.g. GPIOA_MODER,
* or a subregister, e.g. GPIOA_MODER.MODER5,
* or a symbol, e.g. gCounter.
"""

MemAddr = int
"""
Address in memory.
"""

MemData = bytes
"""
The size of it indicates the number of bytes that are needed to read or have been read.
"""
