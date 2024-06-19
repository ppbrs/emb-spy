"""Part of Analyzer class."""
import dataclasses
import inspect

from emb_spy import ReaderStaticResult


@dataclasses.dataclass
class ClockResetEnableItemStm32:
    """Configuration necessary for reporting clock situation with a peripheral."""

    name: str
    """Name of a peripheral."""
    bits_rst: str | None
    bits_en: str | None


def report_clock_enable_stm32(
    self,
    bits_data: dict[str, ReaderStaticResult],
    md_file,
    items: list[ClockResetEnableItemStm32],
    title: str
) -> None:
    """
    Add "Clock reset/enabled" chapter to the report.

    """
    assert "Analyzer" in [cls.__name__ for cls in inspect.getmro(self.__class__)]
    # which is basically the same as issublass(self.__class__, Analyzer).

    # todo: check items type

    md_file.new_header(level=1, title=title)

    legend = ["Peripheral", "Bus", "RST", "EN"]
    table: list[list[str]] = [[] for _ in range(len(items))]

    for row_idx, item in enumerate(items):
        table[row_idx].append(item.name)

        if item.bits_en is not None:
            bus_name = item.bits_en.split(".")[0][4:8]
        elif item.bits_rst is not None:
            bus_name = item.bits_rst.split(".")[0][4:8]
        else:
            bus_name = "?"
        table[row_idx].append(bus_name)

        if item.bits_rst is not None:
            rst = "RST" if bits_data[item.bits_rst].val == 1 else "-"
        else:
            rst = "?"
        table[row_idx].append(rst)

        if item.bits_en is not None:
            rst = "EN" if bits_data[item.bits_en].val == 1 else "-"
        else:
            rst = "?"
        table[row_idx].append(rst)

    md_file.new_table(
        columns=len(legend), rows=(1 + len(table)), text_align="left",
        text=(legend + [cell for row in table for cell in row]),
    )
    md_file.new_line("***")
