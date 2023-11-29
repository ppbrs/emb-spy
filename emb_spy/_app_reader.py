from __future__ import annotations

# Standard library imports
import ctypes
import dataclasses
import logging
import pathlib
# Third party imports
import cpp_demangle  # https://github.com/benfred/py-cpp-demangle
import elftools.elf.elffile
# Local application/library imports
from .mmreg.registers_if import Register, Registers, RegisterBits


class _AppReader:

    @dataclasses.dataclass
    class Config:
        # descr: bool = True
        # comment: bool = False
        # bits: bool = True
        # bits_descr: bool = True
        # bits_val_descr: bool = False
        ctype: int = ctypes.c_uint32  # todo
        verbose: bool = False

    @dataclasses.dataclass
    class _SymbolData:
        name: str
        addr: int
        ctype: int
        val: int | None = None
        vals: list[tuple[float, int]] = dataclasses.field(default_factory=lambda: [])

    @dataclasses.dataclass
    class _RegisterData:
        register: Register
        sub_register: RegisterBits
        verbose: bool = False
        val: int | None = None
        vals: list[tuple[float, int]] = dataclasses.field(default_factory=lambda: [])

    def __init__(self,
                 config: dict[str, Config],
                 host: str = "localhost",
                 port: int | None = None,
                 target_name: str | None = None,
                 logger_suffix: str | None = None,
                 registers: Registers | None = None,
                 elf_path: pathlib.PosixPath | None = None,
                 start_if_reset: bool = False
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
        self.start_if_reset = start_if_reset

        self.regs_data: list[self._RegisterData] = []
        self._prepare_registers_data()
        self.syms_data: list[self._SymbolData] = []
        self._prepare_symbols_data()

        if not self.regs_data and not self.syms_data:
            raise ValueError("There is nothing to read.")

    def _prepare_registers_data(self):
        if self.registers is not None:
            for name_in_config, config in self.config.items():
                # Examples of name_in_config: TIM1_CNT as a register), TIM1_CNT.CNT as a
                # subregister, g_counter0 as a memory object.
                assert len(name_in_config.split(".")) <= 2, \
                    f"There cannot be more than one period in the name. ({name_in_config})"
                reg_name_in_config = name_in_config.split(".")[0]

                for name, register in self.registers.get_dict_name().items():
                    if reg_name_in_config == name:
                        if len(name_in_config.split(".")) == 2:
                            sub_reg_name = name_in_config.split(".")[1]
                            for sub_register in register.register_bits:
                                if sub_reg_name == sub_register.name:
                                    self.regs_data.append(self._RegisterData(register=register, sub_register=sub_register, verbose=config.verbose, val=None))
                                    break
                            else:
                                raise ValueError(f"{reg_name_in_config}.{sub_reg_name} not found.")
                        else:
                            self.regs_data.append(self._RegisterData(register=register, sub_register=None, verbose=config.verbose, val=None))
                            break
        if not self.regs_data:
            self.logger.info("There are no registers to read.")
        else:
            self.logger.info(f"{len(self.regs_data)} registers will be read.")
            # self.logger.info(f"{self.regs_data}")

    def _prepare_symbols_data(self):
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
                                self.logger.debug("Symbol `%s` found: st_value=0x%x, st_size=%d, sizeof(ctype)=%d.", sname, st_value, st_size, ctypes.sizeof(ctype))
                                assert ctypes.sizeof(ctype) == st_size, "Symbol size is wrong."
                                self.syms_data.append(self._SymbolData(name=sname, addr=st_value, ctype=ctype))
        if not self.syms_data:
            self.logger.info("There are no symbols to read.")
        else:
            self.logger.info(f"{len(self.syms_data)} symbols will be read.")
