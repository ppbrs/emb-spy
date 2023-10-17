"""
Application that can read and print the contents of multiple registers and/or symbols
from a single MCU connected via OpenOCD.
"""

# Standard library imports
import dataclasses
import ctypes
import logging
import pathlib
# Third party imports
import cpp_demangle  # https://github.com/benfred/py-cpp-demangle
import elftools.elf.elffile
# Local application/library imports
from .backend import Backend
from .mmreg.registers_if import Register, Registers


class AppStatic:
    """A class that contains methods of the application."""

    @dataclasses.dataclass
    class Config:
        descr: bool = False
        comment: bool = False
        bits: bool = True
        bits_descr: bool = False
        bits_val_descr: bool = False
        ctype: int = ctypes.c_uint32  # todo

    def __init__(self,
                 config: dict[str, Config],
                 host: str, port: int,
                 target_name: str | None = None,
                 logger_suffix: str | None = None,
                 registers: Registers | None = None,
                 elf_path: pathlib.PosixPath | None = None
                 ):
        """
        :param logger_suffix: Optional suffix for the logger name.
        """
        self.logger = logging.getLogger(
            self.__class__.__name__ + ("" if logger_suffix is None else logger_suffix))
        self.config = config
        self.host = host
        self.port = port
        self.target_name = target_name
        self.logger_suffix = logger_suffix
        self.registers = registers
        self.elf_path = elf_path

    def __call__(self) -> list:

        self.logger.debug("App called.")

        @dataclasses.dataclass
        class RegisterData:
            register: Register
            config: AppStatic.Config
            val: int | None = None

        @dataclasses.dataclass
        class SymbolData:
            name: str
            addr: int
            ctype: int
            val: int | None = None

        regs_data: list[RegisterData] = []
        if self.registers is not None:
            for name, register in self.registers.get_dict_name().items():
                if name in self.config.keys():
                    regs_data.append(RegisterData(register=register, config=self.config[name], val=None))
        if not regs_data:
            self.logger.info("There are no registers to read.")

        symbols: list[SymbolData] = []
        if self.elf_path is not None:
            self.logger.info("Analyzing %s", self.elf_path)
            assert self.elf_path.exists() and self.elf_path.is_file()
            with open(self.elf_path, "rb") as file:
                elf = elftools.elf.elffile.ELFFile(file)
                for section_idx in range(elf.num_sections()):
                    section = elf.get_section(section_idx)
                    if type(section) == elftools.elf.sections.SymbolTableSection:
                        logging.info("%d symbols total.", section.num_symbols())
                        # self.logger.debug("Looking for (%s)", self.config.keys())
                        for symbol in section.iter_symbols():
                            try:
                                sname = cpp_demangle.demangle(symbol.name)
                            except ValueError:
                                sname = symbol.name
                            if sname in self.config.keys():
                                st_value = symbol["st_value"]
                                st_size = symbol["st_size"]
                                ctype = self.config[sname].ctype
                                self.logger.debug("Symbol `%s` found: 0x%x, %d, %d", sname, st_value, st_size, ctypes.sizeof(ctype))
                                assert ctypes.sizeof(ctype) == st_size, "Symbol size is wrong."
                                symbols.append(SymbolData(name=sname, addr=st_value, ctype=ctype))
        if not symbols:
            self.logger.info("There are no symbols to read.")

        with Backend(host=self.host, port=self.port, target_name=self.target_name,
                     logger_suffix=self.logger_suffix) as backend:
            for reg_data in regs_data:
                reg_data.val = backend.read_register(addr=reg_data.register.addr)
            for s_data in symbols:
                s_data.val = backend.read_memory(addr=s_data.addr, ctype=s_data.ctype)

        res = {}
        print()
        for reg_data in regs_data:
            reg_str = reg_data.register.get_str(
                value=reg_data.val,
                descr=reg_data.config.descr,
                comment=reg_data.config.comment,
                bits=reg_data.config.bits,
                bits_descr=reg_data.config.bits_descr,
                bits_val_descr=reg_data.config.bits_val_descr,
            )
            print(reg_str, "\n")

        print()
        for s_data in symbols:
            print(f"{s_data.name} = {s_data.val} / 0x{s_data.val:x} ({s_data.ctype})")
            res[s_data.name] = s_data.val

        return res
