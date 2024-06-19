"""
Application that can read multiple STM32F051's registers and print their content.
"""
import logging

from emb_spy import STM32F051
from emb_spy import ReaderConfigCoreReg
from emb_spy import ReaderConfigCoreRegBits
from emb_spy import ReaderConfigMemory
from emb_spy import ReaderConfigMmapRegBits
from emb_spy import ReaderStatic


def main() -> None:
    """Read and print registers."""
    logging.basicConfig(level=logging.DEBUG)
    config = [
        # ReaderConfigMmapReg("GPIOA_MODER"),

        ReaderConfigMmapRegBits("GPIOA_AFRH.AFR15"),

        # ReaderConfigMemory(0xE000E410),
        # ReaderConfigMemory(0xE000E414),
        # ReaderConfigMemory(0xE000E418),
        ReaderConfigMemory(0xE000E41C),

        # ReaderConfigCoreReg("R0"),
        # ReaderConfigCoreReg("SP"),
        # ReaderConfigCoreReg("LR"),
        # ReaderConfigCoreReg("PC"),
        # ReaderConfigCoreReg("PRIMASK"),
        # ReaderConfigCoreReg("CONTROL"),
        ReaderConfigCoreReg("PSP"),
        ReaderConfigCoreReg("MSP"),
        ReaderConfigCoreReg("PSR"),

        ReaderConfigCoreRegBits("PRIMASK.PRIMASK"),
        ReaderConfigCoreRegBits("CONTROL.SPSEL"),
        ReaderConfigCoreRegBits("PSR.ExceptionNumber"),

        # ReaderStatic.SymbolConfig("tick::sysTickCnt"),

    ]

    # elf_path = pathlib.PosixPath("project.elf").absolute()

    results = ReaderStatic(
        config=config,
        soc=STM32F051(),
        # elf_path=elf_path,
    ).read()
    for name, result in results.items():
        if isinstance(name, int):
            print(f"0x{name:08X}:")
        else:
            print(f"{name}:")
        print(f"val={result.val}")
        print(f"raw(LE)={result.raw[::-1].hex()}")
        print(f"{result.descr}")
        print()


if __name__ == "__main__":
    main()
