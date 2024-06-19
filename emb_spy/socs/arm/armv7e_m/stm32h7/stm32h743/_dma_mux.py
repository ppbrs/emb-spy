"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_dma_mux(self: SoC):
    assert self.__class__.__name__ == "STM32H743"

    base_1 = 0x40020800
    base_2 = 0x58025800

    for dma_mux_idx in [1, 2]:
        dmamux = f"DMAMUX{dma_mux_idx}"
        chnl_count = 16 if dma_mux_idx == 1 else 8
        base = base_1 if dma_mux_idx == 1 else base_2
        for chnl in range(0, chnl_count):
            self.append(MmapReg(
                name=f"{dmamux}_C{chnl}CR", addr=(base + 0x04 * chnl),
                descr=f"{dmamux} request line multiplexer channel {chnl} configuration register",
                bits=[
                      Bits(bits=range(0, 7), name="DMAREQ_ID", descr="DMA request identification"),
                    # Bit 9 EGE: Event generation enable
                    # Bit 8 SOIE: Synchronization overrun interrupt enable
                    # Bit 16 SE: Synchronization enable
                    # Bits 18:17 SPOL[1:0]: Synchronization polarity
                    # Bits 23:19 NBREQ[4:0]: Number of DMA requests minus 1 to forward
                      Bits(
                        bits=range(24, 27), name="SYNC_ID", descr="Synchronization identification"),
                ]))

        self.append(MmapReg(
            name=f"{dmamux}_CSR", addr=(base + 0x080),
            descr=f"{dmamux} request line multiplexer interrupt channel status register",
            bits=[])
        )
