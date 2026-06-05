"""
Utilities to prepare reports on analyzed ELF files.
"""

import dataclasses
import logging
import pathlib
from collections.abc import Iterable

from mdutils import MdUtils  # type: ignore

from .elf import Elf, ElfSymbol


def report_elf_symbols(
    elf: Elf,
    out_file_path: pathlib.PosixPath,
    types: Iterable[str] = ("STT_FUNC", "STT_OBJECT", "STT_NOTYPE", "STT_SECTION", "STT_FILE"),
) -> None:
    """
    Generate a Markdown-formatted report.
    """
    logger = logging.getLogger(__name__)

    md_file = MdUtils(file_name=str(out_file_path), title="Symbols Report")

    md_file.new_line(f"**ELF**: {elf.elf_path}")

    md_file.new_line("***")
    for s_type in types:
        symbols: list[ElfSymbol] = sorted(
            [s for s in elf.get_symbols() if s.type == s_type], key=lambda sym: sym.name_demangled
        )
        logger.info("%s: %d symbols", s_type, len(symbols))
        if not symbols:
            continue

        md_file.new_line(f"# {s_type}")

        table_legend = [
            "size",
            "bind",
            "name (demangled)",
        ]  # name goes last because it can be very long
        table_values = []

        for symbol in symbols:
            if symbol.type in types:
                table_values += [
                    str(symbol.size),
                    symbol.bind.removeprefix("STB_"),
                    f"`{symbol.name_demangled}`",
                ]

        num_cols = len(table_legend)
        num_rows = 1 + len(table_values) // len(table_legend)
        md_file.new_line(f"{len(table_values) // len(table_legend)} {s_type} symbols")

        md_file.new_line("")
        md_file.new_table(
            columns=num_cols,
            rows=num_rows,
            text_align="left",
            text=(table_legend + table_values),
        )

        md_file.new_line("***")
    md_file.create_md_file()


def report_elf_symbols_compare(
    elf_a: Elf,
    elf_b: Elf,
    out_file_path: pathlib.PosixPath,
) -> None:
    """
    Take 2 ELF files and generate a report on the difference.
    """

    @dataclasses.dataclass(frozen=True)
    class NameSize:
        """Structure that holds information about one symbol."""

        name: str
        name_demangled: str
        """Demangled name of the symbol."""
        size_a: int | None = None
        size_b: int | None = None

    md_file = MdUtils(file_name=str(out_file_path), title="Symbols compare report")

    md_file.new_line(f"**ELF A**: {elf_a.elf_path}")
    md_file.new_line(f"**ELF B**: {elf_b.elf_path}")
    md_file.new_line("***")

    for s_type in ("STT_FUNC", "STT_OBJECT", "STT_NOTYPE", "STT_SECTION", "STT_FILE"):
        ns_set: set[NameSize] = set()
        for s in elf_a.get_symbols():
            if s.type != s_type:
                continue
            ns_set.add(NameSize(name=s.name, name_demangled=s.name_demangled, size_a=s.size))

        for s in elf_b.get_symbols():
            if s.type != s_type:
                continue
            ns_found = next((ns for ns in ns_set if ns.name == s.name), None)
            if ns_found is None:
                ns_set.add(NameSize(name=s.name, name_demangled=s.name_demangled, size_b=s.size))
            else:
                assert isinstance(ns_found, NameSize)
                ns_set.remove(ns_found)
                ns_set.add(
                    NameSize(
                        name=ns_found.name,
                        name_demangled=s.name_demangled,
                        size_a=ns_found.size_a,
                        size_b=s.size,
                    )
                )

        ns_list = sorted([ns for ns in ns_set if ns.size_a != ns.size_b], key=lambda ns: ns.name)
        if not ns_list:
            continue

        md_file.new_line(f"# {s_type}")

        table_legend = ["A size", "B size", "Demangled name"]
        table_values = []

        for ns in ns_list:
            table_values += [str(ns.size_a), str(ns.size_b), f"`{ns.name_demangled}`"]

        num_cols = len(table_legend)
        num_rows = 1 + len(table_values) // len(table_legend)
        md_file.new_table(
            columns=num_cols, rows=num_rows, text_align="left", text=(table_legend + table_values)
        )

        md_file.new_line("***")

    md_file.create_md_file()
