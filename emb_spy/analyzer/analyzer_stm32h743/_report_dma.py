"""Part of AnalyzerSTM32H743 class."""
import itertools

from emb_spy import ReaderStaticResult
from mdutils import MdUtils  # type: ignore


def report_dma(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file: MdUtils,
) -> None:
    """Add "DMA" chapter to the report."""
    # Circular import error does not allow importing AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    md_file.new_header(level=1, title="DMA")

    legend = [
        "DMA", "Str", "En", "Direction",
        "Circular", "Double", "Target", "Priority",
        "MSIZE", "PSIZE",
        "MINC", "PINC",
        "NDT",
        "PAR", "M0A", "M1A",
        "Mode",
        "Bufferable",
        "Interrupts",
    ]
    table = []
    for dma_idx, stream_idx in itertools.product([1, 2], range(8)):
        row = ["?"] * len(legend)
        #
        dma = f"DMA{dma_idx}"
        row[legend.index("DMA")] = str(dma)
        #
        stream = f"S{stream_idx}"
        row[legend.index("Str")] = str(stream)
        #
        enabled = bits_data[f"{dma}_{stream}CR.EN"].val
        row[legend.index("En")] = "EN" if enabled else "-"
        #
        direction = {
            0b00: "Per-to-Mem",
            0b01: "Mem-to-Per",
            0b10: "Mem-to-Mem", }[bits_data[f"{dma}_{stream}CR.DIR"].val]
        row[legend.index("Direction")] = str(direction)
        #
        circular = bits_data[f"{dma}_{stream}CR.CIRC"].val
        row[legend.index("Circular")] = "CIRC" if circular else "-"
        #
        double = bits_data[f"{dma}_{stream}CR.DBM"].val
        row[legend.index("Double")] = "DOUBLE" if double else "-"
        #
        target = bits_data[f"{dma}_{stream}CR.CT"].val
        row[legend.index("Target")] = str(target)
        #
        prio = bits_data[f"{dma}_{stream}CR.PL"].val
        prio_str = {
            0b00: "Low",
            0b01: "Medium",
            0b10: "High",
            0b11: "Very high", }[prio]
        row[legend.index("Priority")] = prio_str
        #
        msize = {
            0b00: "8-bit",
            0b01: "16-bit",
            0b10: "32-bit", }[bits_data[f"{dma}_{stream}CR.MSIZE"].val]
        row[legend.index("MSIZE")] = msize
        #
        psize = {
            0b00: "8-bit",
            0b01: "16-bit",
            0b10: "32-bit", }[bits_data[f"{dma}_{stream}CR.PSIZE"].val]
        row[legend.index("PSIZE")] = psize
        #
        minc = bits_data[f"{dma}_{stream}CR.MINC"].val
        row[legend.index("MINC")] = "MINC" if minc else "-"
        #
        pinc = bits_data[f"{dma}_{stream}CR.PINC"].val
        row[legend.index("PINC")] = "PINC" if pinc else "-"
        #
        ndt = bits_data[f"{dma}_{stream}NDTR.NDT"].val
        row[legend.index("NDT")] = str(ndt)
        # PAR
        par = bits_data[f"{dma}_{stream}PAR.PAR"].val
        row[legend.index("PAR")] = hex(par) if par else ""
        # M0A
        m0a = bits_data[f"{dma}_{stream}M0AR.M0A"].val
        row[legend.index("M0A")] = hex(m0a) if m0a else ""
        # M1A
        m1a = bits_data[f"{dma}_{stream}M1AR.M1A"].val
        row[legend.index("M1A")] = hex(m1a) if m1a else ""
        # FIFO
        dmdis = bits_data[f"{dma}_{stream}FCR.DMDIS"].val
        row[legend.index("Mode")] = "FIFO" if dmdis else "Direct"
        # Bufferable
        trbuff = bits_data[f"{dma}_{stream}CR.TRBUFF"].val
        row[legend.index("Bufferable")] = "Yes" if trbuff else "-"
        # Interrupts
        interrupts = []
        if bits_data[f"{dma}_{stream}CR.TCIE"].val:
            interrupts.append("TC")
        if bits_data[f"{dma}_{stream}CR.HTIE"].val:
            interrupts.append("HT")
        if bits_data[f"{dma}_{stream}CR.TEIE"].val:
            interrupts.append("TE")
        if bits_data[f"{dma}_{stream}CR.DMEIE"].val:
            interrupts.append("DME")
        row[legend.index("Interrupts")] = " ".join(interrupts) if interrupts else "-"

        table.extend(row)

    md_file.new_table(
        columns=len(legend), rows=(1 + len(table) // len(legend)), text_align="left",
        text=(legend + table),
    )

    md_file.new_line("***")
