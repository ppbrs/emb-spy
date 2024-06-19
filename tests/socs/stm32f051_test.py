"""Tests for STM32F051 SoC."""
from soc_test import check_soc  # type: ignore

from emb_spy.socs.arm.armv6_m.stm32f0.stm32f051 import STM32F051


def test_stm32f051() -> None:
    """Check the sanity of STM32F051 SoC."""
    soc = STM32F051()
    check_soc(soc)


def test_stm32f051_core() -> None:
    """Check that STM32F051 SoC contains specific core registers."""
    names = [
        "R0", "R12",
        "SP",
        "LR",
        "PC",
        "PSR",
        "PRIMASK",
        "CONTROL",
        "PSP",
        "MSP",
    ]
    soc = STM32F051()
    mmreg_names = soc.map_name().keys()
    for name in names:
        assert name in mmreg_names, f"`{name}` not found."


def test_stm32f051_mmap() -> None:
    """Check that STM32F051 SoC contains specific memory-mapped registers."""
    names = [
        # GPIO
        "GPIOA_MODER",
        # Advanced-control timers
        "TIM1_CNT",
        # RCC
        "RCC_CR", "RCC_CFGR",
        "RCC_AHBENR", "RCC_APB2ENR", "RCC_APB1ENR",
        "RCC_APB2RSTR", "RCC_APB1RSTR",
        "RCC_AHBRSTR", "RCC_CFGR2", "RCC_CFGR3", "RCC_CR2",
        # USART
        "USART1_CR1", "USART2_CR1",
    ]
    # ----------------------------------------------------------------------------------------------
    # Debug
    names.extend(["DWT_PCSR", ])
    # ----------------------------------------------------------------------------------------------
    # SYSTICK:
    names.extend(["SYST_CSR", "SYST_RVR", "SYST_CVR", "SYST_CALIB", ])
    # ----------------------------------------------------------------------------------------------
    # NVIC
    names.extend(["NVIC_ISER0", "NVIC_ICER0", "NVIC_ISPR0", "NVIC_ICPR0", ])
    names.extend([f"NVIC_IPR{i}" for i in range(8)])
    # ----------------------------------------------------------------------------------------------
    soc = STM32F051()
    mmreg_names = soc.map_name().keys()
    for name in names:
        assert name in mmreg_names, f"`{name}` not found."
