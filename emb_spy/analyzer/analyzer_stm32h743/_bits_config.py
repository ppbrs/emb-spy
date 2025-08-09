"""Part of AnalyzerSTM32H743 class."""
# from emb_spy import ReaderConfigMmapReg
from emb_spy import STM32H743
from emb_spy import ReaderConfigCoreReg
from emb_spy import ReaderConfigCoreRegBits
from emb_spy import ReaderConfigMmapRegBits
from emb_spy import ReaderStaticResult
from emb_spy.analyzer.analyzer import ConfigType


def get_bits_config(
    self,
) -> dict[str, ReaderStaticResult]:
    """Read all necessary register bits from the SoC."""
    # Circular import error does not allow importin AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    config: ConfigType = []
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
        "ADC12_CCR",
        "ADC3_CCR",
    ])
    mmap_reg_names.extend([
        "ADC1_ISR", "ADC1_CR", "ADC1_CFGR", "ADC1_CFGR2", "ADC1_PCSEL", "ADC1_SMPR1", "ADC1_SMPR2",
        "ADC1_SQR1", "ADC1_SQR2", "ADC1_SQR3", "ADC1_SQR4",
        "ADC2_ISR", "ADC2_CR", "ADC2_CFGR", "ADC2_CFGR2", "ADC2_PCSEL", "ADC2_SMPR1", "ADC2_SMPR2",
        "ADC2_SQR1", "ADC2_SQR2", "ADC2_SQR3", "ADC2_SQR4",
        "ADC3_ISR", "ADC3_CR", "ADC3_CFGR", "ADC3_CFGR2", "ADC3_PCSEL", "ADC3_SMPR1", "ADC3_SMPR2",
        "ADC3_SQR1", "ADC3_SQR2", "ADC3_SQR3", "ADC3_SQR4",
    ])
    mmap_reg_names.extend([
        "DAC_CR", "DAC_MCR",
    ])
    mmap_reg_names.extend([
        f"DMAMUX{dma_mux_idx}_C{ch_idx}CR"
        for dma_mux_idx in [1, 2]
        for ch_idx in range({1: 16, 2: 8, }[dma_mux_idx])
    ])
    mmap_reg_names.extend([
        "DBGMCU_IDC",
        "TIM1_CR1", "TIM1_ARR",
        "TIM8_CR1", "TIM8_ARR",
        "SYS_FLASH_SIZE",
        "SYS_UID0", "SYS_UID1", "SYS_UID2",
        "SYSCFG_PMCR", "SYSCFG_PKGR",
        "SYST_CSR", "SYST_RVR", "SYST_CVR", "SYST_CALIB",
    ])
    mmap_reg_names.extend([
        "HRTIM_MCR",
        "HRTIM_CNTAR", "HRTIM_PERAR", "HRTIM_TIMACR",
        "HRTIM_CNTBR", "HRTIM_PERBR", "HRTIM_TIMBCR",
        "HRTIM_CNTCR", "HRTIM_PERCR", "HRTIM_TIMCCR",
        "HRTIM_CNTDR", "HRTIM_PERDR", "HRTIM_TIMDCR",
        "HRTIM_CNTER", "HRTIM_PERER", "HRTIM_TIMECR",
    ])
    mmap_reg_names.extend([
        "QUADSPI_CR", "QUADSPI_DCR",
    ])
    mmap_reg_names.extend([
        "MPU_TYPE", "MPU_CTRL",
    ])
    mmap_reg_names.extend([
        "RCC_CFGR",
        "RCC_CR",
        "RCC_D1CFGR",
        "RCC_D2CFGR",
        "RCC_D3CCIPR",
        "RCC_D3CFGR",
        "RCC_PLL1DIVR",
        "RCC_PLL1FRACR",
        "RCC_PLL2DIVR",
        "RCC_PLL2FRACR",
        "RCC_PLL3DIVR",
        "RCC_PLL3FRACR",
        "RCC_PLLCFGR",
        "RCC_PLLCKSELR",

        "RCC_D1CCIPR",

        "RCC_AHB1ENR", "RCC_AHB1RSTR",
        "RCC_AHB2ENR", "RCC_AHB2RSTR",
        "RCC_AHB3ENR", "RCC_AHB3RSTR",
        "RCC_AHB4ENR", "RCC_AHB4RSTR",
        "RCC_APB1HENR", "RCC_APB1HRSTR",
        "RCC_APB1LENR", "RCC_APB1LRSTR",
        "RCC_APB2ENR", "RCC_APB2RSTR",
        "RCC_APB3ENR", "RCC_APB3RSTR",
        "RCC_APB4ENR", "RCC_APB4RSTR",
    ])
    mmap_reg_names.extend([
        "SCB_CCR",
        "CLIDR", "CTR", "CCSIDR", "CSSELR",
    ])

    mmap_reg_names.extend([
        "DWT_PCSR",
    ])

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

    for dma in [1, 2]:
        for stream in range(8):
            mmap_reg_names.append(f"DMA{dma}_S{stream}CR")
            mmap_reg_names.append(f"DMA{dma}_S{stream}NDTR")
            mmap_reg_names.append(f"DMA{dma}_S{stream}PAR")
            mmap_reg_names.append(f"DMA{dma}_S{stream}M0AR")
            mmap_reg_names.append(f"DMA{dma}_S{stream}M1AR")
            mmap_reg_names.append(f"DMA{dma}_S{stream}FCR")

    soc = STM32H743()
    map_name = soc.map_name()
    for mmap_reg_name in mmap_reg_names:
        mmap_reg = map_name[mmap_reg_name]
        for bits in mmap_reg.bits:
            name = mmap_reg.name + "." + bits.name
            config.append(ReaderConfigMmapRegBits(name=name))

    for core_reg_name in core_reg_names:
        core_reg = map_name[core_reg_name]
        for bits in core_reg.bits:
            name = core_reg.name + "." + bits.name
            config.append(ReaderConfigCoreRegBits(name=name))

    return config
