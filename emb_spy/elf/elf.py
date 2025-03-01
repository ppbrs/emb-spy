"""
Library of functions for extacting symbols information from object files.
"""

import dataclasses
import logging
import pathlib
import re
import subprocess as sp
from collections import Counter

import elftools.elf.elffile

from .demangle import demangle

ElfSymbolName = str
ElfSymbolNameDemangled = str

Addr = int
Code = list[str]  # 1 or 2 16-bit values for ARM, e.g. ['e92d', '4ff0']
Decoded = str


@dataclasses.dataclass
class ElfSection:
    """Structure that holds information about one section."""

    name: str
    """Name of the section."""
    idx: int
    addr: Addr
    size: int
    type: str
    """
    Section type.

    See specification:
    https://refspecs.linuxfoundation.org/LSB_2.1.0/LSB-Core-generic/LSB-Core-generic/elftypes.html

    Most notable are:
    SHT_PROGBITS = The section holds information defined by the program, whose format and meaning
        are determined solely by the program.
    SHT_NOBITS = A section of this type occupies no space in the file but otherwise
        resembles SHT_PROGBITS.
    SHT_SYMTAB = This section holds a symbol table.
    """


@dataclasses.dataclass
class ElfSymbol:
    """Structure that holds information about one symbol."""

    name: str
    """Name of the symbol as it is stored in the object file."""
    name_demangled: str
    """Demangled name of the symbol."""
    addr: int
    size: int
    type: str  # STT_FUNC, STT_OBJECT, STT_NOTYPE, STT_SECTION, STT_FILE
    bind: str  # STB_LOCAL, STB_GLOBAL, STB_WEAK
    section: ElfSection

    def __str__(self) -> str:
        """Convert to a short human-readable string."""
        addr_top = self.addr + self.size
        return (
            f"'{self.name}' "
            f"("
            f"'{self.name_demangled}'"
            f", {self.size} B"
            f", [0x{self.addr:08x}, 0x{addr_top:08x})"
            f", {self.type}, {self.bind}"
            ")"
        )


@dataclasses.dataclass
class ElfSymbolDisassembly:
    """Structure that holds information about a symbol's disassembly."""

    symbol_name: ElfSymbolName
    symbol_name_demangled: ElfSymbolNameDemangled
    lines: list[str]
    """
    Disassembly lines for the symbol.
    """


@dataclasses.dataclass
class ElfInstruction:
    """Structure that holds information about a disassembly line."""

    addr: Addr
    """
    Instruction address
    """
    code: list[str]
    """
    Instruction code, e.g. ['e92d', '4ff0'].
    """
    decoded: Decoded
    """
    Decoded instruction, e.g. 'stmdb sp!, {r4, r5, r6, r7, r8, r9, sl, fp, lr}'.
    """
    symbol_name: ElfSymbolName
    symbol_name_demangled: ElfSymbolNameDemangled
    symbol_addr: Addr

    def __repr__(self) -> str:
        """Convert to a short human-readable string."""
        return (
            "ElfInstruction("
            f"addr=0x{self.addr:08x},"
            f" '{self.decoded}',"
            f" '{self.code}',"
            f" in '{self.symbol_name}' (0x{self.symbol_addr:08x}),"
            ")"
        )


class Elf:
    """Get all info from an ELF file."""

    def __init__(
        self,
        elf_path: pathlib.PosixPath,
        objdump: str = "objdump",
    ) -> None:
        """Lazily construct Elf."""
        self._logger = logging.getLogger(self.__class__.__name__)
        self.elf_path = elf_path
        self.objdump = objdump
        self.symbols: list[ElfSymbol] | None = None
        self.instructions: list[ElfInstruction] | None = None
        self.symbols_disassembly: list[ElfSymbolDisassembly] | None = None

    def _get_symbols(
        self,
        elf_path: pathlib.PosixPath,
    ) -> list[ElfSymbol]:
        """
        Return a list of all symbols found in the ELF file.

        Zero-size symbols will be ignored.
        """
        assert elf_path.exists() and elf_path.is_file()

        symbols_list: list[ElfSymbol] = []
        sections_map: dict[int, ElfSection] = {}

        self._logger.info("Analyzing '%s'", elf_path)
        with open(elf_path, "rb") as file:
            elf = elftools.elf.elffile.ELFFile(file)

            self._logger.debug("%d sections", elf.num_sections())
            for section_idx in range(elf.num_sections()):
                section = elf.get_section(section_idx)
                sections_map[section_idx] = ElfSection(
                    name=section.name,
                    idx=section_idx,
                    addr=section["sh_addr"],
                    size=section["sh_size"],
                    type=section["sh_type"],
                )

            for section_idx in sections_map:
                section = elf.get_section(section_idx)
                if section["sh_type"] == "SHT_SYMTAB":
                    assert hasattr(section, "num_symbols")
                    assert hasattr(section, "iter_symbols")
                    self._logger.info("%d symbols total", section.num_symbols())  # pyright: ignore
                    for symbol in section.iter_symbols():  # pyright: ignore
                        if symbol["st_size"]:
                            st_value = symbol["st_value"]
                            st_info = symbol["st_info"]
                            symbols_list.append(
                                ElfSymbol(
                                    name=symbol.name,
                                    name_demangled=demangle(symbol.name),
                                    addr=st_value,
                                    size=symbol["st_size"],
                                    type=st_info["type"],
                                    bind=st_info["bind"],
                                    section=sections_map[symbol["st_shndx"]],
                                )
                            )
        self._logger.info("%d symbols will be returned", len(symbols_list))

        type_counter: Counter = Counter()
        for symbol in symbols_list:
            type_counter.update([symbol.type])
        self._logger.info("object types: %s", type_counter)

        bind_counter: Counter = Counter()
        for symbol in symbols_list:
            bind_counter.update([symbol.bind])
        self._logger.info("object binds: %s", bind_counter)

        return symbols_list

    def get_symbols(
        self,
    ) -> list[ElfSymbol]:
        """
        Return a list of all non-zero-size symbols found in the ELF file.
        """
        if self.symbols is None:
            self.symbols = self._get_symbols(elf_path=self.elf_path)
        return self.symbols

    def _get_disassembly(
        self,
        elf_path: pathlib.PosixPath,
        objdump: str = "objdump",
    ) -> tuple[list[ElfInstruction], list[ElfSymbolDisassembly]]:
        self._logger.info("Disassembling '%s' with '%s'", elf_path, objdump)
        instructions = []
        symbols_disassembly = []

        def disassemble() -> list[str]:
            with sp.Popen(
                args=[objdump, "--disassemble", "--wide", str(elf_path)],
                stdout=sp.PIPE,
                stderr=sp.PIPE,
            ) as proc:
                out, _ = proc.communicate()
                assert proc.wait() == 0
            self._logger.info("'%s' ok", objdump)
            return out.decode(encoding="ascii").splitlines()

        # Example of a line:
        #   '40a: <__aeabi_dcmpge>'
        #   ' 40a:\t4684       \tmov ip, r0'
        #   ' 40c:\tf023 0307 \tbic.w   r3, r3, #7'
        instr_pattern: re.Pattern = re.compile(r"^\s([A-Fa-f0-9]+)?:\t([A-Fa-f0-9\s]+)\t(.*)$")
        symbol_pattern: re.Pattern = re.compile(r"^([A-Fa-f0-9]+)\s<(.*)>:$")

        symbol_name: str | None = None
        symbol_disassembly: ElfSymbolDisassembly | None = None
        symbol_name_demangled: str | None = None
        symbol_addr: str | None = None

        def process_line(line: str) -> None:
            nonlocal symbol_name
            nonlocal symbol_disassembly
            nonlocal symbol_name_demangled
            nonlocal symbol_addr

            if mtch := symbol_pattern.fullmatch(line):
                assert len(mtch.groups()) == 2
                symbol_addr, symbol_name = mtch.groups()
                assert symbol_name is not None
                symbol_name_demangled = demangle(symbol_name)
                assert symbol_disassembly is None
                symbol_disassembly = ElfSymbolDisassembly(
                    symbol_name=symbol_name,
                    symbol_name_demangled=symbol_name_demangled,
                    lines=[],
                )
            elif mtch := instr_pattern.fullmatch(line):
                assert symbol_name is not None
                assert symbol_name_demangled is not None
                assert symbol_addr is not None
                assert len(mtch.groups()) == 3
                addr, code, decoded = mtch.groups()
                addr = int(addr, 16)
                code = code.strip().split()
                instructions.append(
                    ElfInstruction(
                        addr=addr,
                        code=code,
                        decoded=decoded,
                        symbol_name=symbol_name,
                        symbol_name_demangled=symbol_name_demangled,
                        symbol_addr=int(symbol_addr, 16),
                    )
                )
                assert symbol_disassembly is not None
                symbol_disassembly.lines.append(line)
            elif line == "":
                if symbol_disassembly is not None:
                    symbols_disassembly.append(symbol_disassembly)
                    symbol_disassembly = None

        for line in disassemble():
            process_line(line=line)

        self._logger.info("%d instructions total", len(instructions))

        return instructions, symbols_disassembly

    def get_instructions(
        self,
    ) -> list[ElfInstruction]:
        """Return a list of all disassembly lines."""
        if self.instructions is None:
            self.instructions, self.symbols_disassembly = self._get_disassembly(
                elf_path=self.elf_path, objdump=self.objdump
            )
        return self.instructions

    def get_symbols_disassembly(
        self,
    ) -> list[ElfSymbolDisassembly]:
        """Return a list of all symbols' disassembly."""
        if self.symbols_disassembly is None:
            self.instructions, self.symbols_disassembly = self._get_disassembly(
                elf_path=self.elf_path, objdump=self.objdump
            )
        return self.symbols_disassembly

    def get_instruction_for_pc_sample(
        self,
        get_true: bool,
        pc_sample,
    ) -> ElfInstruction:
        """
        Return a disassembly line for a given PC value.

        The PC points one instruction forward due to Pipeline (prefetch).
        """
        assert self.instructions is not None
        for i, instr in enumerate(self.instructions):
            if instr.addr == pc_sample:
                if get_true:
                    assert i > 0
                    return self.instructions[i - 1]
                return self.instructions[i]
        raise ValueError(f"{pc_sample=}")
