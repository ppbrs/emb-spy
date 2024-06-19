"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_bdma(self: SoC):
    assert self.__class__.__name__ == "STM32H743"

    base = 0x58025400

    isr_bits = []
    for chnl in range(0, 8):
        isr_bits += [
            Bits(
                bits=(4 * chnl + 0), name=f"GIF{chnl}",
                descr=f"global interrupt flag for channel {chnl}",
                descr_vals={1: "a TE, HT or TC event occurred", }
            ),
            Bits(
                bits=(4 * chnl + 1), name=f"TCIF{chnl}",
                descr=f"transfer complete (TC) flag for channel {chnl}",
                descr_vals={1: "a TC event occurred", }
            ),
            Bits(
                bits=(4 * chnl + 2), name=f"HTIF{chnl}",
                descr=f"half transfer (HT) flag for channel {chnl}",
                descr_vals={1: "a HT event occurred", }
            ),
            Bits(
                bits=(4 * chnl + 3), name=f"TEIF{chnl}",
                descr=f"transfer error (TE) flag for channel {chnl}",
                descr_vals={1: "a TE event occurred", }
            ),
        ]

    self.append(MmapReg(
        name="BDMA_ISR", addr=(base + 0x00),
        descr="BDMA interrupt status", bits=isr_bits))
    for chnl in range(0, 8):
        self.append(MmapReg(
            name=f"BDMA_CCR{chnl}", addr=(base + 0x08 + 0x14 * chnl),
            descr=f"BDMA channel {chnl} configuration register",
            bits=[
                Bits(bits=0, name="EN", descr="channel enable"),
                Bits(bits=1, name="TCIE", descr="transfer complete interrupt enable"),
                Bits(bits=2, name="HTIE", descr="half transfer interrupt enable"),
                Bits(bits=3, name="TEIE", descr="transfer error interrupt enable"),
                Bits(bits=4, name="DIR", descr="data transfer direction",
                     descr_vals={0: "read from peripheral", 1: "read from memory"}),
                Bits(bits=5, name="CIRC", descr="circular mode"),
                Bits(bits=6, name="PINC", descr="peripheral increment mode"),
                Bits(bits=7, name="MINC", descr="memory increment mode"),
                Bits(bits=range(8, 10), name="PSIZE", descr="peripheral size",
                     descr_vals={0: "8 bits", 1: "16 bits", 2: "32 bits", 3: "reserved"}),
                Bits(bits=range(10, 12), name="MSIZE", descr="memory size",
                     descr_vals={0: "8 bits", 1: "16 bits", 2: "32 bits", 3: "reserved"}),
                Bits(bits=range(12, 14), name="PL", descr="priority level",
                     descr_vals={0: "low", 1: "medium", 2: "high", 3: "very high", }),
                Bits(bits=14, name="MEM2MEM", descr="memory-to-memory mode"),
                Bits(bits=15, name="DBM", descr="double-buffer mode"),
                Bits(
                    bits=16, name="CT",
                    descr="current target memory of DMA transfer in double-buffer mode",
                    descr_vals={
                        0: "memory 0 (addressed by the BDMA_CM0AR pointer)",
                        1: "memory 1 (addressed by the BDMA_CM1AR pointer)", }),
            ]))
        self.append(MmapReg(
            name=f"BDMA_CNDTR{chnl}", addr=(base + 0x0C + 0x14 * chnl),
            descr=f"BDMA channel {chnl} number of data to transfer register"))
        self.append(MmapReg(
            name=f"BDMA_CPAR{chnl}", addr=(base + 0x10 + 0x14 * chnl),
            descr=f"BDMA channel {chnl} peripheral address register"))
        self.append(MmapReg(
            name=f"BDMA_CM0AR{chnl}", addr=(base + 0x14 + 0x14 * chnl),
            descr=f"BDMA channel {chnl} memory 0 address register"))
        self.append(MmapReg(
            name=f"BDMA_CM1AR{chnl}", addr=(base + 0x18 + 0x14 * chnl),
            descr=f"BDMA channel {chnl} memory 1 address register"))
