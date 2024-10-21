import dataclasses
import logging

import elftools.elf.elffile
from emb_spy.demangle import demangle


@dataclasses.dataclass
class ElfSymbol:
    name: str
    addr: str
    size: int
    type_: str  # STT_FUNC, STT_OBJECT, STT_NOTYPE, STT_SECTION, STT_FILE
    bind: str  # STB_LOCAL, STB_GLOBAL, STB_WEAK

    def __str__(self) -> str:
        addr_top = self.addr + self.size
        return f"'{self.name}' (0x{self.addr:08x}, 0x{addr_top:08x}, {self.size}, {self.type_}, {self.bind})"


class Elf:

    def __init__(
        self,
        elf_path,
    ):
        assert elf_path.exists() and elf_path.is_file()
        self.elf_path = elf_path

    def get_symbols_map(
        self,
    ) -> dict[str, ElfSymbol]:

        symbols_map: dict[str, ElfSymbol] = {}

        logging.info("Analyzing '%s'", self.elf_path)
        with open(self.elf_path, "rb") as file:
            elf = elftools.elf.elffile.ELFFile(file)

            sections: list[elftools.elf.sections.Section] = []
            logging.debug("%d sections", elf.num_sections())
            for section_idx in range(elf.num_sections()):
                sections.append(elf.get_section(section_idx))
                logging.debug("Section #%d: name=%s, type=%s, class=%s, address=[%x..%x]",
                              section_idx,
                              sections[-1].name,
                              sections[-1]["sh_type"],
                              sections[-1].__class__.__name__,
                              sections[-1]["sh_addr"],
                              sections[-1]["sh_addr"] + sections[-1]["sh_size"]
                              )

            if sections:
                for section in sections:
                    if isinstance(section, elftools.elf.sections.SymbolTableSection):
                        logging.info("%d symbols total", section.num_symbols())
                        for symbol in section.iter_symbols():
                            st_name = symbol.name
                            st_size = symbol["st_size"]
                            if st_size:
                                st_name = demangle(st_name)
                                st_value = symbol["st_value"]
                                if not st_name:  # empty name
                                    st_name = f"0x{st_value:08x}"
                                st_info = symbol["st_info"]
                                st_type = st_info["type"]
                                st_bind = st_info["bind"]
                                # assert symbols.get(st_name) is None
                                symbols_map[st_name] = ElfSymbol(
                                    name=st_name,
                                    addr=st_value,
                                    size=st_size,
                                    type_=st_type,
                                    bind=st_bind,
                                )
        logging.info("map of symbols created, %d symbols", len(symbols_map))
        return symbols_map
