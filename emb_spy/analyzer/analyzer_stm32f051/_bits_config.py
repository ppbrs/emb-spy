"""Part of AnalyzerSTM32F051."""
from emb_spy import STM32F051
from emb_spy import ReaderConfigCoreReg
from emb_spy import ReaderConfigCoreRegBits
from emb_spy import ReaderConfigMmapReg
from emb_spy import ReaderConfigMmapRegBits
from emb_spy import ReaderStaticResult


def _get_bits_config(
    self,
) -> dict[str, ReaderStaticResult]:
    """Read all necessary register bits from the SoC."""
    assert self.__class__.__name__ == "AnalyzerSTM32F051"
    # This is equivalent to assert isinstance(self, AnalyzerSTM32F051).
    # I do this to avoid the circular import error.

    config: list[ReaderConfigMmapReg | ReaderConfigMmapRegBits | ReaderConfigCoreReg | ReaderConfigCoreRegBits] = []

    # All bits from these memory-mapped and core registers are required:
    mmap_reg_names, core_reg_names = [], []

    mmap_reg_names.extend([
        "RCC_CFGR",
        "RCC_CR",
        "RCC_APB2RSTR",
        "RCC_APB1RSTR",
        "RCC_APB2ENR",
        "RCC_APB1ENR",
    ])

    for gpio_idx in ["A", "B", "C"]:
        mmap_reg_names.append(f"GPIO{gpio_idx}_MODER")
        mmap_reg_names.append(f"GPIO{gpio_idx}_PUPDR")
        mmap_reg_names.append(f"GPIO{gpio_idx}_OTYPER")
        mmap_reg_names.append(f"GPIO{gpio_idx}_AFRL")
        mmap_reg_names.append(f"GPIO{gpio_idx}_AFRH")
        mmap_reg_names.append(f"GPIO{gpio_idx}_OSPEEDR")
        mmap_reg_names.append(f"GPIO{gpio_idx}_IDR")
        mmap_reg_names.append(f"GPIO{gpio_idx}_ODR")
        mmap_reg_names.append(f"GPIO{gpio_idx}_LCKR")

    # SYSTICK
    mmap_reg_names.extend(["SYST_CSR", "SYST_RVR", "SYST_CVR", "SYST_CALIB", ])
    # NVIC
    config.extend([ReaderConfigMmapReg(f"NVIC_ISER{i}") for i in range(0, 1)])
    config.extend([ReaderConfigMmapReg(f"NVIC_ISPR{i}") for i in range(0, 1)])
    config.extend([ReaderConfigMmapReg(f"NVIC_IPR{i}") for i in range(0, 8)])
    # USART2
    mmap_reg_names.extend([
        "USART2_BRR",
        "USART2_CR1", "USART2_CR2", "USART2_CR3",
        "USART2_GTPR", "USART2_RTOR", "USART2_RQR", "USART2_ISR", ])
    # Core
    config.extend([ReaderConfigCoreReg(f"R{i}") for i in range(13)])
    config.append(ReaderConfigCoreReg("SP"))
    config.append(ReaderConfigCoreReg("LR"))
    config.append(ReaderConfigCoreReg("PC"))
    config.append(ReaderConfigCoreRegBits("PRIMASK.PRIMASK"))
    config.append(ReaderConfigCoreReg("PSP"))
    config.append(ReaderConfigCoreReg("MSP"))
    core_reg_names.extend(["CONTROL", "PSR"])
    # Debug
    mmap_reg_names.append("DWT_PCSR")

    soc = STM32F051()
    map_name = soc.map_name()

    for core_reg_name in core_reg_names:
        core_reg = map_name[core_reg_name]
        for bits in core_reg.bits:
            config.append(ReaderConfigCoreRegBits(name=(core_reg.name + "." + bits.name)))

    for mmap_reg_name in mmap_reg_names:
        mmap_reg = map_name[mmap_reg_name]
        for bits in mmap_reg.bits:
            config.append(ReaderConfigMmapRegBits(name=(mmap_reg.name + "." + bits.name)))

    return config
