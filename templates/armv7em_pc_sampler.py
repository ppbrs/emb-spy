import logging
import pathlib
import time
from collections import Counter

from emb_spy import PCSampler
from emb_spy import STM32F745
from emb_spy.elf import Elf, ElfSymbol


def main(
    blocking: bool,
    duration: float,
    soc,
    jtag_target_name: str,
    elf_path: pathlib.PosixPath,
) -> None:
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

    logger.info(f"{len(pc_samples)} PC samples collected.")

    # print("PC samples:")
    # for pc_sample in pc_samples:
    #     print(f"\t0x{pc_sample:08x}")

    symbols_map: dict[str, ElfSymbol] = Elf(elf_path=elf_path).get_symbols_map()
    # print("Symbols:")
    # for symbol in symbols_map.values():
    #     print(f"\t{symbol}")

    pc_samples_ext = []
    symbol_counter = Counter()
    for pc_sample in pc_samples:
        pc_sample = pc_sample - 4  # For v7m-e
        # pc_sample = (pc_sample & 0xFFFFFFFE) + 1
        for name, symbol in symbols_map.items():
            if pc_sample >= symbol.addr and pc_sample < (symbol.addr + symbol.size):
                pc_samples_ext.append((pc_sample, symbol.name))
                symbol_counter.update([symbol.name])
                break
        else:
            logger.warning(f"Symbol not found for 0x{pc_sample:08x}")

    # Optional sorting:
    symbol_counter = {k: v for k, v in sorted(symbol_counter.items(), reverse=True, key=lambda kv: kv[1])}

    print("Counters:")
    for name, cnt in symbol_counter.items():
        print(f"\t{name}: {cnt}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    SOC = STM32F745()

    jtag_target_name = "solo.cpu"
    # jtag_target_name = "master.cpu"
    # jtag_target_name = "axis.cpu"

    bin_dir_path = pathlib.PosixPath("~/projects/fw7.wt0/bin").expanduser()

    elf_path = bin_dir_path / "vegaf7_application.elf"

    main(
        blocking=False,
        duration=0.5,
        jtag_target_name=jtag_target_name,
        elf_path=elf_path,
        soc=SOC,
    )
