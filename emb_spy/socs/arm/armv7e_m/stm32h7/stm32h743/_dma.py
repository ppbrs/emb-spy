
"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_dma(self: SoC):
    assert self.__class__.__name__ == "STM32H743"

    for dma_idx in (1, 2):
        dma = f"DMA{dma_idx}"
        base = {
            1: 0x40020000,
            2: 0x40020400, }[dma_idx]

        for stream_idx in range(8):

            self.append(MmapReg(
                name=f"{dma}_S{stream_idx}CR", addr=(base + 0x010 + 0x18 * stream_idx),
                descr=f"DMA{dma_idx} stream {stream_idx} configuration register",
                bits=[

                    # Bits 24:23 MBURST[1:0]: Memory burst transfer configuration
                    # 00: Single transfer
                    # 01: INCR4 (incremental burst of 4 beats)
                    # 10: INCR8 (incremental burst of 8 beats)
                    # 11: INCR16 (incremental burst of 16 beats)

                    # Bits 22:21 PBURST[1:0]: Peripheral burst transfer configuration
                    # 00: Single transfer
                    # 01: INCR4 (incremental burst of 4 beats)
                    # 10: INCR8 (incremental burst of 8 beats)
                    # 11: INCR16 (incremental burst of 16 beats)

                    Bits(bits=20, name="TRBUFF", descr="Enable the DMA to handle bufferable transfers"),
                    # 0: Bufferable transfers not enabled
                    # 1: Bufferable transfers enabled

                    Bits(bits=19, name="CT", descr="Current target (only in double-buffer mode)"),
                    # 0: Current target memory is memory 0 (addressed by the DMA_SxM0AR pointer).
                    # 1: Current target memory is memory 1 (addressed by the DMA_SxM1AR pointer).

                    Bits(bits=18, name="DBM", descr="Double-buffer mode"),
                    # 0: No buffer switching at the end of transfer
                    # 1: Memory target switched at the end of the DMA transfer

                    Bits(bits=range(16, 17), name="PL", descr="priority level"),
                    # 00: Low
                    # 01: Medium
                    # 10: High
                    # 11: Very high

                    # Bit 15 PINCOS: Peripheral increment offset size
                    # 0: The offset size for the peripheral address calculation is
                    # linked to the PSIZE.
                    # 1: The offset size for the peripheral address calculation is
                    # fixed to 4 (32-bit alignment).

                    Bits(bits=range(13, 15), name="MSIZE", descr="Memory data size"),
                    # 00: Byte (8-bit)
                    # 01: Half-word (16-bit)
                    # 10: Word (32-bit)

                    Bits(bits=range(11, 13), name="PSIZE", descr="Peripheral data size"),
                    # 00: Byte (8-bit)
                    # 01: Half-word (16-bit)
                    # 10: Word (32-bit)

                    Bits(bits=10, name="MINC", descr="Memory increment mode"),
                    # 0: Memory address pointer fixed
                    # 1: Memory address pointer incremented after each data transfer
                    # (increment is done according to MSIZE)

                    Bits(bits=9, name="PINC", descr="Peripheral increment mode"),
                    # 0: Peripheral address pointer fixed
                    # 1: Peripheral address pointer incremented after each data transfer
                    # (increment done according to PSIZE)

                    Bits(bits=8, name="CIRC", descr="Circular mode"),
                    # 0: Circular mode disabled
                    # 1: Circular mode enabled

                    Bits(bits=range(6, 8), name="DIR", descr="Data transfer direction"),
                    # 00: Peripheral-to-memory
                    # 01: Memory-to-peripheral
                    # 10: Memory-to-memory

                    # Bit 5 PFCTRL: Peripheral flow controller
                    # 0: DMA is the flow controller.
                    # 1: The peripheral is the flow controller.

                    Bits(bits=4, name="TCIE", descr="Transfer complete interrupt enable"),
                    # 0: TC interrupt disabled
                    # 1: TC interrupt enabled

                    Bits(bits=3, name="HTIE", descr="Half transfer interrupt enable"),
                    # 0: HT interrupt disabled
                    # 1: HT interrupt enabled

                    Bits(bits=2, name="TEIE", descr="Transfer error interrupt enable"),
                    # 0: TE interrupt disabled
                    # 1: TE interrupt enabled

                    Bits(bits=1, name="DMEIE", descr="Direct mode error interrupt enable"),
                    # 0: DME interrupt disabled
                    # 1: DME interrupt enabled

                    Bits(bits=0, name="EN", descr="Stream enable/flag stream ready when read low"),
                ],
            ))
            self.append(MmapReg(
                name=f"{dma}_S{stream_idx}NDTR", addr=(base + 0x014 + 0x18 * stream_idx),
                descr=f"DMA{dma_idx} stream {stream_idx} number of data register",
                bits=[
                    Bits(
                        bits=range(16), name="NDT",
                        descr="Number of data items to transfer (0 up to 65535)"),
                ],
            ))
            self.append(MmapReg(
                name=f"{dma}_S{stream_idx}PAR", addr=(base + 0x018 + 0x18 * stream_idx),
                descr=f"DMA{dma_idx} stream {stream_idx} peripheral address register",
                bits=[
                    Bits(bits=range(32), name="PAR", descr="Peripheral address"),
                ],
            ))
            self.append(MmapReg(
                name=f"{dma}_S{stream_idx}M0AR", addr=(base + 0x01C + 0x18 * stream_idx),
                descr=f"DMA{dma_idx} stream {stream_idx} memory 0 address register",
                bits=[
                    Bits(bits=range(32), name="M0A", descr="Memory 0 address"),
                ],
            ))
            self.append(MmapReg(
                name=f"{dma}_S{stream_idx}M1AR", addr=(base + 0x020 + 0x18 * stream_idx),
                descr=f"DMA{dma_idx} stream {stream_idx} memory 1 address register",
                bits=[
                    Bits(
                        bits=range(32), name="M1A",
                        descr="Memory 1 address (used in case of double-buffer mode)"),
                ],
            ))
            self.append(MmapReg(
                name=f"{dma}_S{stream_idx}FCR", addr=(base + 0x024 + 0x18 * stream_idx),
                descr=f"DMA{dma_idx} stream {stream_idx} FIFO control register",
                bits=[
                    # Bit 7 FEIE: FIFO error interrupt enable
                    # 0: FE interrupt disabled
                    # 1: FE interrupt enabled
                    # Bits 5:3 FS[2:0]: FIFO status
                    # 000: 0 < fifo_level < 1/4
                    # 001: 1/4 ≤ fifo_level < 1/2
                    # 010: 1/2 ≤ fifo_level < 3/4
                    # 011: 3/4 ≤ fifo_level < full
                    # 100: FIFO is empty.
                    # 101: FIFO is full.
                    Bits(bits=2, name="DMDIS", descr="Direct mode disable"),
                    # 0: Direct mode enabled
                    # 1: Direct mode disabled
                    # Bits 1:0 FTH[1:0]: FIFO threshold selection
                ],
            ))
