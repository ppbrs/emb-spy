"""
Everything related to reading firmware symbol values from a SoC running that firmware.

ReaderConfigSymbol class that configures the readers for getting a symbol value.
_ReaderSymbol class that includes functions for that.
"""
import ctypes
import dataclasses
from typing import Any

# import elftools.elf.elffile  # type: ignore

# from emb_spy.demangle import Demangle
from emb_spy.elf import Elf, ElfSymbol
from emb_spy.reader._reader_common import MemAddr
from emb_spy.reader._reader_common import MemData
from emb_spy.reader._reader_common import ReaderConfig
from emb_spy.reader._reader_common import SymbolName


@dataclasses.dataclass
class ReaderConfigSymbol(ReaderConfig):
    """
    The structure that defines how the value of a symbol should be returned or printed.
    """
    name: SymbolName
    ctype: Any = ctypes.c_uint32
    # verbose: bool = False


class _ReaderSymbol:
    """"""
 
    @dataclasses.dataclass
    class _SymbolConfigExt(ReaderConfigSymbol):
        """
        Fields that are filled by _Reader.
        """
        found_in_elf: bool = False
        mem_addr: int | MemAddr = None

    def parse_config(
        self,
        config,
        mem_map,
        core_map,
    ) -> None:
        """
        Find and preprocess symbols configurations from the list of all configurations.
        """

        for cfg in config:
            if isinstance(cfg, ReaderConfigSymbol):
                # "casting" SymbolConfig to _SymbolConfigExt:
                cfg_ext = self._SymbolConfigExt(name=cfg.name)
                for field in dataclasses.fields(cfg):
                    setattr(cfg_ext, field.name, getattr(cfg, field.name))
                self.config_symbol.append(cfg_ext)

        if len(self.config_symbol):
            if self.elf_path is None:
                raise ValueError(
                    "Once reading symbols is requested, the path to the elf file (elf_path) "
                    "must be provided.")
            self.elf_path = self.elf_path.expanduser()

            elf_symbols: list[ElfSymbol] = Elf(elf_path=self.elf_path).get_symbols()
            for idx, cfg in enumerate(self.config_symbol):
                for elf_symbol in elf_symbols:
                    if cfg.name == elf_symbol.name or cfg.name == elf_symbol.name_demangled:
                        self.config_symbol[idx].found_in_elf = True
                        self.logger.debug("Found `%s` in ELF, address %s, size %d.", cfg.name, hex(elf_symbol.addr), elf_symbol.size)
                        mem_data_size = elf_symbol.size  # Number of bytes occupied.
                        if ctypes.sizeof(cfg.ctype) != mem_data_size:
                            raise ValueError(
                                f"`{cfg.name}`: own size is {mem_data_size}B, "
                                f"requested {ctypes.sizeof(cfg.ctype)}B ({cfg.ctype}).")
                        mem_addr = elf_symbol.addr
                        self.config_symbol[idx].mem_addr = mem_addr
                        mem_data_size = ((mem_data_size + 3) // 4) * 4
                        if (mem_data := mem_map.get(mem_addr)) is None or len(mem_data) < mem_data_size:
                            mem_data = bytes(mem_data_size)
                            mem_map[mem_addr] = mem_data
                        break
                else:
                    raise ValueError("Symbol not found.")

            # if not self.elf_path.exists() or not self.elf_path.is_file():
            #     raise ValueError(f"Path \"{self.elf_path}\" does not exist or is not a file.")

            # self.logger.info("Analyzing \'%s\'.", self.elf_path.name)
            # assert self.elf_path.exists() and self.elf_path.is_file()
            # with open(self.elf_path, "rb") as file:
            #     elf = elftools.elf.elffile.ELFFile(file)
            #     for section_idx in range(elf.num_sections()):
            #         section = elf.get_section(section_idx)
            #         if isinstance(section, elftools.elf.sections.SymbolTableSection):
            #             self.logger.info(
            #                 "Found %d symbols in \'%s\'.",
            #                 section.num_symbols(), self.elf_path.name)
            #             for symbol in section.iter_symbols():
            #                 demangled_name = demangle(symbol.name)
            #                 for idx, cfg in enumerate(self.config_symbol):
            #                     if cfg.name == demangled_name or cfg.name == symbol.name:
            #                         self.config_symbol[idx].found_in_elf = True
            #                         self.logger.debug("Found `%s` in ELF.", cfg.name)
            #                         mem_data_size = symbol["st_size"]  # Number of bytes occupied.
            #                         if ctypes.sizeof(cfg.ctype) != mem_data_size:
            #                             raise ValueError(
            #                                 f"`{cfg.name}`: own size is {mem_data_size}B, "
            #                                 f"requested {ctypes.sizeof(cfg.ctype)}B ({cfg.ctype}).")
            #                         mem_addr = symbol["st_value"]
            #                         self.config_symbol[idx].mem_addr = mem_addr
            #                         mem_data_size = ((mem_data_size + 3) // 4) * 4
            #                         if (mem_data := mem_map.get(mem_addr)) is None or len(mem_data) < mem_data_size:
            #                             mem_data = bytes(mem_data_size)
            #                             mem_map[mem_addr] = mem_data
            #                         break
            # TODO: check that all symbols were found.
