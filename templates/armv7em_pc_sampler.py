"""An example of PCSampler usage."""

import logging
import pathlib
import time
from collections import Counter

# from emb_spy import STM32F745 as SOC
from emb_spy import STM32H743 as SOC
from emb_spy import PCSampler
from emb_spy.elf import Elf
from emb_spy.elf import ElfSymbol


def main(
    blocking: bool,
    duration: float,
    soc,
    jtag_target_name: str,
    elf_path: pathlib.PosixPath,
) -> None:
    """Sample processor PC and report in what ELF symbols PC was found."""
    logger = logging.getLogger(__name__)

    pc_sampler = PCSampler(
        soc=soc,
        host="localhost",
        port=4444,
        jtag_target_name=jtag_target_name,
    )

    if blocking:
        pc_samples = pc_sampler.collect(duration)
    else:
        pc_sampler.start_collecting()
        time.sleep(duration)
        pc_samples = pc_sampler.stop_collecting()

    logger.info("%d PC samples collected.", len(pc_samples))

    # print("PC samples:")
    # for pc_sample in pc_samples:
    #     print(f"\t0x{pc_sample:08x}")

    elf = Elf(
        elf_path=elf_path,
        objdump="armv7m-none-eabihf-objdump",
    )
    symbols: list[ElfSymbol] = elf.get_symbols()
    logger.info("%d symbols", len(symbols))

    # print("Symbols:")
    # for symbol in symbols_map.values():
    #     print(f"\t{symbol}")

    pc_samples_ext = []
    symbol_counter = Counter()
    for pc_sample in pc_samples:
        for symbol in symbols:
            if symbol.addr <= pc_sample < (symbol.addr + symbol.size):
                pc_samples_ext.append((pc_sample, symbol.name_demangled))
                symbol_counter.update([symbol.name_demangled])
                break
        else:
            logger.warning("Symbol not found for 0x%.08x", pc_sample)

    # Optional sorting:
    symbol_counter = dict(sorted(symbol_counter.items(), reverse=True, key=lambda kv: kv[1]))

    print("\nSymbols numbers of samples when PC was inside a symbol:")
    for name, cnt in symbol_counter.items():
        print(f"\t{name}: {cnt}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # JTAG_TARGET_NAME = "solo.cpu"
    JTAG_TARGET_NAME = "master.cpu0"
    # JTAG_TARGET_NAME = "axis.cpu"

    bin_dir_path = pathlib.PosixPath("~/projects/fw7.wt3/bin").expanduser()

    # ELF_PATH = bin_dir_path / "vegaf7_application.elf"
    # ELF_PATH = bin_dir_path / "orion_master_application.elf"
    ELF_PATH = bin_dir_path / "orion_master_stage2_upgrade.elf"
    # ELF_PATH = bin_dir_path / "stm32h743_stage1.elf"

    main(
        blocking=True,
        duration=0.5,
        jtag_target_name=JTAG_TARGET_NAME,
        elf_path=ELF_PATH,
        soc=SOC(),
    )
