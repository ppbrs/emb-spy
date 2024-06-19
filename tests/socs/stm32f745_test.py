"""Tests for STM32F745 SoC."""
from soc_test import check_soc  # type: ignore

from emb_spy.socs.arm.armv7e_m.stm32f7.stm32f745 import STM32F745


def test_stm32f745() -> None:
    """Check the sanity of STM32F745 SoC."""
    soc = STM32F745()
    check_soc(soc)


def test_stm32f745_mmap() -> None:
    """Check that STM32F745 SoC contains specific memory-mapped registers."""
    names = [
        # Advanced-control timers
        "TIM1_CNT",
        "TIM8_CNT",
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
    ]
    # ----------------------------------------------------------------------------------------------
    # MPU
    names.extend(["MPU_TYPE", "MPU_CTRL", ])
    # ----------------------------------------------------------------------------------------------
    # RCC:
    names.extend(["RCC_CR", "RCC_PLLCFGR", "RCC_CFGR"])
    # ----------------------------------------------------------------------------------------------
    # SYSTICK:
    names.extend(["SYST_CSR", "SYST_RVR", "SYST_CVR", "SYST_CALIB", ])
    # ----------------------------------------------------------------------------------------------
    soc = STM32F745()
    mmreg_names = soc.map_name().keys()
    for name in names:
        assert name in mmreg_names, \
            f"Memory-mapped register `{name}` was not found in `{soc.__class__.__name__}` SoC."
