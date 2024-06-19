import logging
import pathlib
from pprint import pp

from emb_spy import Elf
from emb_spy import ElfSymbol


def main():
    logging.basicConfig(level=logging.INFO)
    elf_path = pathlib.PosixPath("~/projects/fw7.wt3/bin/saturn2_application.elf").expanduser()

    elf = Elf(
        elf_path=elf_path,
        objdump="armv7m-none-eabihf-objdump",
    )

    instructions = elf.get_instructions()
    print(f"{len(instructions)} instructions")
    # pp(disasm_lines)

    symbols: list[ElfSymbol] = elf.get_symbols()
    print(f"{len(symbols)} symbols")
    # pp(symbols)

    # 0x08044dce
    # 0x08045f2a

    for pc_sample in [
        (0x08044dce + 4),
        (0x08045f2a + 4),
        (0x0806a69a + 4),
        (0x0804ff0a + 4),
        (0x08045f2a + 4),
        (0x0804ff0a + 4),
        (0x08117764 + 4),
        (0x08040ffe + 4),
    ]:
        print(f"pc_sample=0x{pc_sample:08x}")
        inst = elf.get_instruction_for_pc_sample(pc_sample=pc_sample)
        print(f"\t{inst}")


if __name__ == "__main__":
    main()
