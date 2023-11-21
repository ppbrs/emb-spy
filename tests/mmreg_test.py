"""
Tests of collections of memory-mapped registers.
"""
# Standard library imports
import logging
# Third party imports
# Local application/library imports
from emb_spy.mmreg.arm.armv6_m.stm32f0.stm32f051 import MmregSTM32F051
from emb_spy.mmreg.arm.armv7e_m.stm32f7.stm32f745 import MmregSTM32F745
from emb_spy.mmreg.arm.armv7e_m.stm32h7.stm32h743 import MmregSTM32H743
from emb_spy.mmreg.registers_if import Register  # pylint: disable=import-error


def test_mmreg_all_sanity() -> None:
    """
    Sanity checking all collections of memory-mapped registers.
    """
    for soc in [MmregSTM32H743(), MmregSTM32F051()]:

        regs_list: list[Register] = soc.get_list()
        assert isinstance(regs_list, list)
        assert regs_list, "The list of registers is empty."
        for reg in regs_list:
            assert isinstance(reg, Register)
            assert reg.__class__.__name__ == "Register"
            assert "." not in reg.name, f"`.` found in the name of a register ({reg.name})"

        regs_dict_name: dict[str, Register] = soc.get_dict_name()
        assert regs_dict_name, "The dictionary of registers is empty."
        assert isinstance(regs_dict_name, dict)
        for name, reg in regs_dict_name.items():
            assert isinstance(name, str)
            assert reg.__class__.__name__ == "Register"

        regs_dict_address: dict[int | str, Register] = soc.get_dict_address()
        assert regs_dict_address, "The dictionary of registers is empty."
        assert isinstance(regs_dict_address, dict)
        for addr, reg in regs_dict_address.items():
            if not isinstance(addr, int):
                logging.warning("`%s` is not an mmreg, so it should be moved somewhere.", addr)
            assert isinstance(addr, (int | str)), \
                f"Type of address {addr} ({type(addr)}) is incompatible."
            assert reg.__class__.__name__ == "Register"

        assert set(reg.name for reg in regs_list) == set(name for name in regs_dict_name)


def test_mmreg_stm32h743() -> None:
    """
    Make sure the specific information is in MmregSTM32H743.
    """

    # mmreg names that are expected in the collection:
    names = [
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

        # Advanced-control timers
        "TIM1_CNT", "TIM8_CNT",

        # General-purpose timers
        "TIM2_CNT", "TIM3_CNT", "TIM4_CNT", "TIM5_CNT",

        # Debug system registers
        "DHCSR", "DCRSR", "DCRDR", "DEMCR",
    ]

    soc = MmregSTM32H743()
    mmreg_names = soc.get_dict_name().keys()
    for name in names:
        assert name in mmreg_names, f"`{name}` not found."


def test_mmreg_stm32f051() -> None:
    """
    Make sure the specific information is in MmregSTM32F051.
    """

    # mmreg names that are expected in the collection:
    names = [
        # GPIO
        "GPIOA_MODER",

        # Advanced-control timers
        "TIM1_CNT",
    ]

    soc = MmregSTM32F051()
    mmreg_names = soc.get_dict_name().keys()
    for name in names:
        assert name in mmreg_names, f"`{name}` not found."


def test_mmreg_stm32f745() -> None:
    """
    Make sure the specific information is in MmregSTM32F745.
    """
    soc = MmregSTM32F745()

    # mmreg names that are expected in the collection:
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

    mmreg_names = soc.get_dict_name().keys()
    for name in names:
        assert name in mmreg_names, f"`{name}` not found."
