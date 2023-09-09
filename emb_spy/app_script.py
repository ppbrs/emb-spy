
#!/usr/bin/python3
"""

"""
# Standard library imports
import ctypes
from dataclasses import dataclass, field
import logging
import pathlib
import os
import time
# Third party imports
import elftools.elf.elffile
import matplotlib.pyplot as plt
# Local application/library imports
from backend import Backend
from mmreg.arm.armv7e_m.stm32h7.stm32h743 import MmregSTM32H743
from mmreg.arm.armv6_m.stm32f0.stm32f051 import MmregSTM32F051
from mmreg.registers_if import Register, Registers, RegisterBits  # pylint: disable=import-error


@dataclass
class SymbolInfo:
    addr: int
    size: int


class AppScript:

    def __init__(self, elf_path: pathlib.PosixPath, mmregs: Registers, host, port):
        self.elf_path = elf_path
        self.mmregs = mmregs
        self.host = host
        self.port = port

        logging.basicConfig(level=logging.DEBUG)

        # Parse elf file to get all symbols from it.
        with open(self.elf_path, 'rb') as bin_file:
            self.symbols: dict[str, SymbolInfo] = {}
            elf_file = elftools.elf.elffile.ELFFile(bin_file)
            for section in elf_file.iter_sections(type="SHT_SYMTAB"):
                logging.debug("section %s", section.name)
                for symbol in section.iter_symbols():
                    symbol_info = SymbolInfo(addr=symbol["st_value"], size=symbol["st_size"])
                    self.symbols[symbol.name] = symbol_info
                    # logging.debug("symbol %s %s", symbol.name, symbol_info)

    def dump_symbols(self, fname: pathlib.PosixPath):
        """Write all symbols to a file."""
        with open(fname, 'w') as file:
            for name in sorted(self.symbols.keys()):
                file.write(f"{name}, 0x{self.symbols[name].addr}:08X, {self.symbols[name].size}\n")

    def read_symbol(self, name: str, ctype=ctypes.c_uint32, offset: int = 0) -> int:

        logging.debug(f"reading symbol `{name}` and offset {offset} as {ctype}")
        with Backend(host=self.host, port=self.port) as backend:
            # val = backend.read_register(addr=self.symbols[name].addr)
            val = backend.read_memory(addr=(self.symbols[name].addr + offset), ctype=ctype)
        logging.debug(f"read result: {val}, 0x{val:08X}")
        return val

    def write_symbol(self, name: str, val: int, offset=0, ctype=ctypes.c_uint32) -> None:

        logging.info(f"writing {val} to symbol `{name}` and offset {offset} as {ctype}")
        with Backend(host=self.host, port=self.port) as backend:
            # val = backend.write_register(addr=(self.symbols[name].addr + offset), val=val)
            val = backend.write_memory(addr=(self.symbols[name].addr + offset), val=val, ctype=ctype)
        logging.info("writing done")


HOST, PORT = "localhost", 4444

# ELF_PATH = pathlib.PosixPath("/home/boris/projects/emb1.wt0/bin/stm32f051_sbx.elf")
# ELF_PATH = pathlib.PosixPath("/home/boris/projects/emb1.wt0/bin/stm32h743_sbx.elf")
ELF_PATH = pathlib.PosixPath("/home/boris/projects/fw7.wt2/bin/serpens_application.elf")


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    app = AppScript(elf_path=ELF_PATH, mmregs=MmregSTM32H743(), host=HOST, port=PORT)
    app.dump_symbols(fname=(pathlib.PosixPath(__file__).with_suffix(".symbols")))

    app.read_symbol(name="_ZN6sensor12_GLOBAL__N_118systemTemperaturesE", offset=0, ctype=ctypes.c_int16)
    app.read_symbol(name="_ZN6sensor12_GLOBAL__N_118systemTemperaturesE", offset=2, ctype=ctypes.c_int16)

    app.read_symbol(name="_ZN6stm32h6sensor12_GLOBAL__N_125MCUTemperatureDebugOffsetE",
                    ctype=ctypes.c_int16)
    app.write_symbol(name="_ZN6stm32h6sensor12_GLOBAL__N_125MCUTemperatureDebugOffsetE", val=-543, ctype=ctypes.c_int16)
    app.read_symbol(name="_ZN6stm32h6sensor12_GLOBAL__N_125MCUTemperatureDebugOffsetE",
                    ctype=ctypes.c_int16)

    # app.read_symbol(name="_ZN6sensor12_GLOBAL__N_126systemTemperaturesCriticalE")
    # app.write_symbol(name="_ZN6sensor12_GLOBAL__N_126systemTemperaturesCriticalE", val=2)
    # app.read_symbol(name="_ZN6sensor12_GLOBAL__N_126systemTemperaturesCriticalE")
