"""Example of Elf usage."""

import logging
import pathlib

from emb_spy import Elf, ElfSymbol, report_elf_symbols


def run_elf_example():
    """Extract information from an Elf."""
    logger = logging.getLogger(__name__)
    elf_path = pathlib.PosixPath("~/projects/fw7.wt0/bin/prometheus_application.elf").expanduser()
    elf = Elf(
        elf_path=elf_path,
        objdump="armv7m-none-eabihf-objdump",
    )
    logger.info("Elf object created")

    # instructions = elf.get_instructions()
    # logger.info("%d instructions", len(instructions))

    symbols: list[ElfSymbol] = elf.get_symbols()
    logger.info("%d symbols", len(symbols))

    report_elf_symbols(
        symbols=symbols,
        file_name=pathlib.PosixPath(__file__).with_suffix(".symbols.md"),
        types=("STT_FUNC"),
    )

    # for pc_sample in [
    #     (0x08044DCE + 4),
    #     (0x08045F2A + 4),
    #     (0x0806A69A + 4),
    #     (0x0804FF0A + 4),
    #     (0x08045F2A + 4),
    #     (0x0804FF0A + 4),
    #     (0x08117764 + 4),
    #     (0x08040FFE + 4),
    # ]:
    #     print(f"pc_sample=0x{pc_sample:08x}")
    #     inst = elf.get_instruction_for_pc_sample(pc_sample=pc_sample)
    #     print(f"\t{inst}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-1s %(name)s:%(funcName)s:%(lineno)d: %(message)s",
        datefmt="%H:%M:%S",
    )
    run_elf_example()
