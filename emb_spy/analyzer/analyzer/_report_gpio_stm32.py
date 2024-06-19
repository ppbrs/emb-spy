"""Part of Analyzer class."""
import inspect
from collections.abc import Callable

from emb_spy import ReaderStaticResult


def report_gpio_stm32(
    self,
    bits_data: dict[str, ReaderStaticResult],
    md_file,
    port_list: list[str],
    af_descr_getter: Callable[[str, int, int], str] | None,
) -> None:
    """
    Add a GPIO chapter to the report.

    :param af_descr_getter: A SoC-specific function that returns a short description
        of the alternate function for given
            port (a string, e.g. "A"),
            pin_idx (an integer,e.g. 2),
            and af_idx (an integer, e.g. 3).
    """
    assert "Analyzer" in [cls.__name__ for cls in inspect.getmro(self.__class__)]
    # which is basically the same as issublass(self.__class__, Analyzer).

    md_file.new_header(level=1, title="GPIO")
    for port in port_list:
        md_file.new_header(level=2, title=f"GPIO{port}")
        legend: list[str] = []
        table: list[list[str]] = [[] for _ in range(0, 16)]
        #
        legend.append("Pin")
        for pin_idx in range(0, 16):
            table[pin_idx].append(str(f"P{port}{pin_idx}"))
        #
        legend.append("Mode")
        for pin_idx in range(0, 16):
            mode = bits_data[f"GPIO{port}_MODER.MODER{pin_idx}"].val
            table[pin_idx].append(f"{mode}: {_mode_to_str(mode)}")
        #
        legend.append("Pull up/down")
        for pin_idx in range(0, 16):
            pupd = bits_data[f"GPIO{port}_PUPDR.PUPDR{pin_idx}"].val
            table[pin_idx].append(f"{pupd}: {_pupd_to_str(pupd)}")
        #
        legend.append("Output type")
        for pin_idx in range(0, 16):
            otype = bits_data[f"GPIO{port}_OTYPER.OT{pin_idx}"].val
            ot_descr = "open-drain" if otype == 1 else ""
            table[pin_idx].append(f"{otype}: {ot_descr}")
        #
        legend.append("Alternate")
        for pin_idx in range(0, 16):
            is_alternate = bits_data[f"GPIO{port}_MODER.MODER{pin_idx}"].val == 2
            if is_alternate:
                if pin_idx < 8:
                    af_idx = bits_data[f"GPIO{port}_AFRL.AFR{pin_idx}"].val
                else:
                    af_idx = bits_data[f"GPIO{port}_AFRH.AFR{pin_idx}"].val
                if af_descr_getter is not None:
                    # todo: https://stackoverflow.com/questions/73449645
                    descr = af_descr_getter(port=port, pin_idx=pin_idx, af_idx=af_idx)  # noqa
                    table[pin_idx].append(f"{af_idx}: {descr}")
                else:
                    table[pin_idx].append(f"{af_idx}: ?")
            else:
                table[pin_idx].append("-")
        #
        legend.append("Output speed")
        for pin_idx in range(0, 16):
            ospeed = bits_data[f"GPIO{port}_OSPEEDR.OSPEEDR{pin_idx}"].val
            table[pin_idx].append(f"{ospeed}: {_ospeed_to_str(ospeed)}")
        #
        legend.append("Input")
        for pin_idx in range(0, 16):
            idr = bits_data[f"GPIO{port}_IDR.IDR{pin_idx}"].val
            table[pin_idx].append(f"{idr}")
        #
        legend.append("Output")
        for pin_idx in range(0, 16):
            odr = bits_data[f"GPIO{port}_ODR.ODR{pin_idx}"].val
            table[pin_idx].append(f"{odr}")
        #
        legend.append("Lock")
        for pin_idx in range(0, 16):
            lock = bits_data[f"GPIO{port}_LCKR.LCK{pin_idx}"].val
            table[pin_idx].append("Unlocked" if lock == 0 else str(lock))
        #
        md_file.new_table(
            columns=len(legend), rows=(1 + len(table)), text_align="left",
            text=(legend + [cell for row in table for cell in row]),
        )
        md_file.new_line("***")


def _mode_to_str(mode: int) -> str:
    """MODER value meaning."""
    return {
        0b00: "Input",
        0b01: "Output",
        0b10: "Alternate",
        0b11: "Analog", }[mode]


def _pupd_to_str(pupd: int) -> str:
    """PUPDR value meaning."""
    if pupd == 1:
        return "Pull-up"
    if pupd == 2:
        return "Pull-down"
    return ""


def _ospeed_to_str(ospeed: int) -> str:
    """OSPEEDR value meaning."""
    return {
        0b00: "Low",
        0b01: "Medium",
        0b10: "High",
        0b11: "Very high", }[ospeed]
