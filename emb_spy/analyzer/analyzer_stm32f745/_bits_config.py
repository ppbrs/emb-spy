"""Part of AnalyzerSTM32F745 class."""
from emb_spy import STM32F745
from emb_spy import ReaderConfigCoreReg
from emb_spy import ReaderConfigCoreRegBits
from emb_spy import ReaderConfigMmapReg
from emb_spy import ReaderConfigMmapRegBits
from emb_spy import ReaderStaticResult


def _get_bits_config(
    self,
) -> dict[str, ReaderStaticResult]:
    """Read all necessary register bits from the SoC."""
    assert self.__class__.__name__ == "AnalyzerSTM32F745"
    # because I cannot import AnalyzerSTM32F745 from this module - circular import error.

    config: list[ReaderConfigMmapReg | ReaderConfigMmapRegBits | ReaderConfigCoreReg | ReaderConfigCoreRegBits] = []
    for gpio_idx in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", ]:
        config += [ReaderConfigMmapRegBits(
            name=f"GPIO{gpio_idx}_MODER.MODER{pin_idx}") for pin_idx in range(16)]
        config += [ReaderConfigMmapRegBits(
            name=f"GPIO{gpio_idx}_PUPDR.PUPDR{pin_idx}") for pin_idx in range(16)]
        config += [ReaderConfigMmapRegBits(
            name=f"GPIO{gpio_idx}_OTYPER.OT{pin_idx}") for pin_idx in range(16)]
        config += [ReaderConfigMmapRegBits(
            name=f"GPIO{gpio_idx}_AFRL.AFR{pin_idx}") for pin_idx in range(8)]
        config += [ReaderConfigMmapRegBits(
            name=f"GPIO{gpio_idx}_AFRH.AFR{pin_idx}") for pin_idx in range(8, 16)]
        config += [ReaderConfigMmapRegBits(
            name=f"GPIO{gpio_idx}_OSPEEDR.OSPEEDR{pin_idx}") for pin_idx in range(16)]
        config += [ReaderConfigMmapRegBits(
            name=f"GPIO{gpio_idx}_IDR.IDR{pin_idx}") for pin_idx in range(16)]
        config += [ReaderConfigMmapRegBits(
            name=f"GPIO{gpio_idx}_ODR.ODR{pin_idx}") for pin_idx in range(16)]
        config += [ReaderConfigMmapRegBits(
            name=f"GPIO{gpio_idx}_LCKR.LCK{pin_idx}") for pin_idx in range(16)]

    # All bits from these memory-mapped and core registers are required:
    mmap_reg_names, core_reg_names = [], []

    mmap_reg_names.extend([
        "MPU_TYPE", "MPU_CTRL",
    ])
    # NVIC
    config.extend([ReaderConfigMmapReg(f"NVIC_ISER{i}") for i in range(0, 8)])
    config.extend([ReaderConfigMmapReg(f"NVIC_ISPR{i}") for i in range(0, 8)])
    config.extend([ReaderConfigMmapReg(f"NVIC_IPR{i}") for i in range(0, 60)])
    # RCC
    mmap_reg_names.extend(["RCC_CR", "RCC_PLLCFGR", "RCC_CFGR"])
    # System timer
    mmap_reg_names.extend(["SYST_CSR", "SYST_RVR", "SYST_CVR", "SYST_CALIB", ])

    # Core
    config.extend([ReaderConfigCoreReg(f"R{i}") for i in range(13)])
    config.append(ReaderConfigCoreReg("SP"))
    config.append(ReaderConfigCoreReg("LR"))
    config.append(ReaderConfigCoreReg("PC"))
    config.append(ReaderConfigCoreRegBits("PRIMASK.PRIMASK"))
    config.append(ReaderConfigCoreRegBits("FAULTMASK.FAULTMASK"))
    config.append(ReaderConfigCoreRegBits("BASEPRI.BASEPRI"))
    config.append(ReaderConfigCoreReg("PSP"))
    config.append(ReaderConfigCoreReg("MSP"))
    core_reg_names.extend(["CONTROL", "PSR"])
    mmap_reg_names.extend([
        "SCB_CCR",
        # "CLIDR", "CTR", "CCSIDR", "CSSELR",
        "DWT_PCSR",
    ])

    soc = STM32F745()
    map_name = soc.map_name()

    for mmap_reg_name in mmap_reg_names:
        mmap_reg = map_name[mmap_reg_name]
        for bits in mmap_reg.bits:
            config.append(ReaderConfigMmapRegBits(name=(mmap_reg.name + "." + bits.name)))

    for core_reg_name in core_reg_names:
        core_reg = map_name[core_reg_name]
        for bits in core_reg.bits:
            config.append(ReaderConfigCoreRegBits(name=(core_reg.name + "." + bits.name)))

    return config
