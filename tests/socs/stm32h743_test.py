"""Tests for STM32H743 SoC."""

import math

from soc_test import check_soc  # type: ignore

from emb_spy.socs.arm.armv7e_m.stm32h7.stm32h743 import STM32H743


def test_stm32h743() -> None:
    """Check the sanity of STM32F051 SoC."""
    soc = STM32H743()
    check_soc(soc)


def test_stm32h743_core() -> None:
    """Check that STM32F051 SoC contains specific core registers."""
    names = [
        "R0",
        "R12",
        "SP",
        "PSP",
        "MSP",
        "LR",
        "PC",
        "PSR",
        "PRIMASK",
        "FAULTMASK",
        "BASEPRI",
        "CONTROL",
    ]
    soc = STM32H743()
    mmreg_names = soc.map_name().keys()
    for name in names:
        assert name in mmreg_names, f"`{name}` not found."


def test_stm32h743_mmap() -> None:
    """Check that STM32H743 SoC contains specific memory-mapped registers."""
    names = [
        # ------------------------------------------------------------------------------------------
        # Debug system registers
        "DBGMCU_IDC",
        "DBGMCU_CR",
        "DHCSR",
        "DCRSR",
        "DCRDR",
        "DEMCR",
        "DWT_PCSR",
        # ------------------------------------------------------------------------------------------
        # DMA
        "DMA1_S0CR",
        "DMA1_S7CR",
        "DMA2_S0CR",
        "DMA2_S7CR",
        # ------------------------------------------------------------------------------------------
        # GPIO
        "GPIOA_MODER",
        "GPIOB_MODER",
        "GPIOC_MODER",
        "GPIOD_MODER",
        "GPIOE_MODER",
        "GPIOF_MODER",
        "GPIOG_MODER",
        "GPIOH_MODER",
        "GPIOI_MODER",
        "GPIOJ_MODER",
        "GPIOK_MODER",
        # ------------------------------------------------------------------------------------------
        # PWR
        "PWR_CR1",
        "PWR_CR2",
        "PWR_CR3",
        # ------------------------------------------------------------------------------------------
        # PWR
        "QUADSPI_CR",
        "QUADSPI_DCR",
        # ------------------------------------------------------------------------------------------
        # RCC
        "RCC_CR",
        "RCC_CFGR",
        "RCC_AHB1ENR",
        "RCC_AHB1RSTR",
        "RCC_AHB2ENR",
        "RCC_AHB2RSTR",
        "RCC_AHB3ENR",
        "RCC_AHB3RSTR",
        "RCC_AHB4ENR",
        "RCC_AHB4RSTR",
        "RCC_APB1HENR",
        "RCC_APB1HRSTR",
        "RCC_APB1LENR",
        "RCC_APB1LRSTR",
        "RCC_APB2ENR",
        "RCC_APB2RSTR",
        "RCC_APB3ENR",
        "RCC_APB3RSTR",
        "RCC_APB4ENR",
        "RCC_APB4RSTR",
        "RCC_D1CCIPR",
        "RCC_D2CCIP1R",
        "RCC_D2CCIP2R",
        "RCC_D3CCIPR",
        "RCC_PLLCKSELR",
        "RCC_PLLCFGR",
        "RCC_PLL1DIVR",
        "RCC_PLL1FRACR",
        "RCC_PLL2DIVR",
        "RCC_PLL2FRACR",
        "RCC_PLL3DIVR",
        "RCC_PLL3FRACR",
        "RCC_D1CFGR",
        "RCC_D2CFGR",
        "RCC_D3CFGR",
        # ------------------------------------------------------------------------------------------
        # System flash
        "SYS_FLASH_SIZE",
        "SYS_UID0",
        "SYS_UID1",
        "SYS_UID2",
        # ------------------------------------------------------------------------------------------
        # SYSCFG
        "SYSCFG_PMCR",
        # ------------------------------------------------------------------------------------------
        # Timers
        #   Advanced-control timers
        "TIM1_CNT",
        "TIM8_CNT",
        #   General-purpose timers
        "TIM2_CNT",
        "TIM3_CNT",
        "TIM4_CNT",
        "TIM5_CNT",
        #   High-resolution timers
        "HRTIM_MCR",
        # ------------------------------------------------------------------------------------------
    ]
    # ----------------------------------------------------------------------------------------------
    # ADC
    #   individual
    for adc_i in ["ADC1", "ADC2", "ADC3"]:
        names.extend(
            [
                f"{adc_i}_ISR",
                f"{adc_i}_CR",
                f"{adc_i}_CFGR",
                f"{adc_i}_CFGR2",
                f"{adc_i}_PCSEL",
                f"{adc_i}_SMPR1",
                f"{adc_i}_SMPR2",
                f"{adc_i}_SQR1",
                f"{adc_i}_SQR2",
                f"{adc_i}_SQR3",
                f"{adc_i}_SQR4",
            ]
        )
    #   common
    for adc_c in ["ADC12", "ADC3"]:
        names.extend(
            [
                f"{adc_c}_CSR",
                f"{adc_c}_CCR",
                f"{adc_c}_CDR",
                f"{adc_c}_CDR2",
            ]
        )
    # ----------------------------------------------------------------------------------------------
    # BDMA
    names.extend(["BDMA_ISR", "BDMA_CCR0", "BDMA_CM1AR7"])
    # ----------------------------------------------------------------------------------------------
    # DMAMUX:
    names.extend(
        [
            f"DMAMUX{dma_mux_idx}_C{ch_idx}CR"
            for dma_mux_idx in [1, 2]
            for ch_idx in range(
                {
                    1: 16,
                    2: 8,
                }[dma_mux_idx]
            )
        ]
    )
    names.extend(
        [
            "DMAMUX1_CSR",
            "DMAMUX2_CSR",
        ]
    )
    # ----------------------------------------------------------------------------------------------
    # MPU
    names.extend(
        [
            "MPU_TYPE",
            "MPU_CTRL",
        ]
    )
    # ----------------------------------------------------------------------------------------------
    # NVIC
    for idx in range(math.ceil(240 / 32)):
        names.append(f"NVIC_ISER{idx}")
        names.append(f"NVIC_ICER{idx}")
        names.append(f"NVIC_ISPR{idx}")
        names.append(f"NVIC_ICPR{idx}")
        names.append(f"NVIC_IABR{idx}")
    for idx in range(math.ceil(240 / 32)):
        names.append(f"NVIC_IPR{idx}")
    names.append("STIR")
    # ----------------------------------------------------------------------------------------------
    # SYSTICK:
    names.extend(
        [
            "SYST_CSR",
            "SYST_RVR",
            "SYST_CVR",
            "SYST_CALIB",
        ]
    )
    # ----------------------------------------------------------------------------------------------
    soc = STM32H743()
    mmreg_names = soc.map_name().keys()
    for name in names:
        assert (
            name in mmreg_names
        ), f"Memory-mapped register `{name}` was not found in `{soc.__class__.__name__}` SoC."
