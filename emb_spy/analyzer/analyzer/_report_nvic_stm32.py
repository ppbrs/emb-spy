"""Part of Analyzer class."""
import inspect
import math

from emb_spy import ReaderStaticResult


def report_nvic_stm32(
    self,
    bits_data: dict[str, ReaderStaticResult],
    md_file,
    irq_num: int,
    irq_descr: dict[int, str],
) -> None:
    """Add a System Timer chapter to the report."""
    assert "Analyzer" in [cls.__name__ for cls in inspect.getmro(self.__class__)]
    # which is basically the same as issublass(self.__class__, Analyzer).

    md_file.new_header(level=1, title="NVIC")

    legend: list[str] = ["IRQn", "Enabled", "Pending", "Priority", "Legend",]
    table: list[list[str]] = [[] for _ in range(irq_num)]

    reg_num = int(math.ceil(irq_num / 32))
    enabled = [bits_data[f"NVIC_ISER{reg}"].val for reg in range(reg_num)]
    pending = [bits_data[f"NVIC_ISPR{reg}"].val for reg in range(reg_num)]

    reg_num = int(math.ceil(irq_num / 4))
    priority = [bits_data[f"NVIC_IPR{reg}"].val for reg in range(reg_num)]

    for irqn in range(irq_num):
        table[irqn].append(str(irqn))

        reg_idx = irqn // 32
        bit_idx = (irqn % 32) * 1
        enabled_val = bool(enabled[reg_idx] & (1 << bit_idx))
        pending_val = bool(pending[reg_idx] & (1 << bit_idx))
        table[irqn].append("Enabled" if enabled_val else "-")
        table[irqn].append("Pending" if pending_val else "-")

        reg_idx = irqn // 4
        bit_idx = (irqn % 4) * 8
        priority_val = (priority[reg_idx] >> bit_idx) & 255
        table[irqn].append(str(priority_val))

        table[irqn].append(irq_descr[irqn])

    md_file.new_table(
        columns=len(legend), rows=(1 + len(table)), text_align="left",
        text=(legend + [cell for row in table for cell in row]),
    )

    md_file.new_line("***")
