"""
Utilities to prepare reports on analyzed ELF files.
"""

import logging
import pathlib

from .elf import ElfSymbol
from mdutils import MdUtils  # type: ignore


def report_elf_symbols(
    symbols: list[ElfSymbol],
    file_name: pathlib.PosixPath,
    types=("STT_FUNC", "STT_OBJECT", "STT_NOTYPE", "STT_SECTION", "STT_FILE"),
) -> None:
    """
    """
    logger = logging.getLogger(__name__)
    logger.info("")
    md_file = MdUtils(file_name=str(file_name), title="Symbols Report")

    # Sort by demangled name:
    symbols_sorted = sorted(symbols, key=lambda sym: sym.name_demangled)

    table_legend = ["name", "size", "type"]
    table_values = []

    for symbol in symbols_sorted:
        if symbol.type in types:
            table_values += [f"`{symbol.name_demangled}`", symbol.size, str(symbol.type)]

    num_columns = len(table_legend)
    num_rows = 1 + len(table_values) // len(table_legend)
    md_file.new_line(f"{len(table_values) // len(table_legend)} symbols in this report")

    # name_demangled     # addr     # size      # type     # bind     # section

    md_file.new_table(
        columns=num_columns, rows=num_rows, text_align="left", text=(table_legend + table_values)
    )

    md_file.new_line("***")

    md_file.create_md_file()
