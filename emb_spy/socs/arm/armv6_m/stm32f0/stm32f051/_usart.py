"""Part of STM32F051 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_usart(self: SoC) -> None:
    """Generate Register objects for USART peripheral."""
    assert self.__class__.__name__ == "STM32F051"

    usart1_base = 0x40013800
    usart2_base = 0x40004400
    # usart3_base = 0x40004800
    # usart4_base = 0x40004C00
    # usart5_base = 0x40005000
    # usart6_base = 0x40011400
    # usart7_base = 0x40011800
    # usart8_base = 0x40011C00

    _init_usart_x(self, idx=1, base=usart1_base)
    _init_usart_x(self, idx=2, base=usart2_base)


def _init_usart_x(self: SoC, idx: int, base: int) -> None:

    usart = f"USART{idx}"

    self.append(MmapReg(
        name=f"{usart}_CR1", addr=(base + 0x00), descr="USART control register 1",
        bits=[
            Bits(bits=28, name="M1", descr="Word length"),
            Bits(bits=27, name="EOBIE", descr="End of Block interrupt enable"),
            Bits(bits=26, name="RTOIE", descr="Receiver timeout interrupt enable"),
            Bits(bits=range(21, 26), name="DEAT", descr="Driver Enable assertion time"),
            Bits(bits=range(16, 21), name="DEDT", descr="Driver Enable de-assertion time"),
            Bits(bits=15, name="OVER8", descr="Oversampling mode"),
            # 0: Oversampling by 16
            # 1: Oversampling by 8
            Bits(bits=14, name="CMIE", descr="Character match interrupt enable"),
            Bits(bits=13, name="MME", descr="Mute mode enable"),
            Bits(bits=12, name="M0", descr="Word length"),
            Bits(bits=11, name="WAKE", descr="Receiver wake-up method"),
            Bits(bits=10, name="PCE", descr="Parity control enable"),
            Bits(bits=9, name="PS", descr="Parity selection"),
            Bits(bits=8, name="PEIE", descr="PE interrupt enable"),
            Bits(bits=7, name="TXEIE", descr="interrupt enable"),
            Bits(bits=6, name="TCIE", descr="Transmission complete interrupt enable"),
            Bits(bits=5, name="RXNEIE", descr="RXNE interrupt enable"),
            Bits(bits=4, name="IDLEIE", descr="IDLE interrupt enable"),
            Bits(bits=3, name="TE", descr="Transmitter enable"),
            Bits(bits=2, name="RE", descr="Receiver enable"),
            Bits(bits=1, name="UESM", descr="USART enable in Stop mode"),
            Bits(bits=0, name="UE", descr="USART enable"),
        ]
    ))

    self.append(MmapReg(
        name=f"{usart}_CR2", addr=(base + 0x04), descr="USART control register 2",
        bits=[
            # Bits 31:28 ADD[7:4]: Address of the USART node
            # Bits 27:24 ADD[3:0]: Address of the USART node
            # Bit 23 RTOEN: Receiver timeout enable
            # Bits 22:21 ABRMOD[1:0]: Auto baud rate mode
            # Bit 20 ABREN: Auto baud rate enable
            # Bit 19 MSBFIRST: Most significant bit first
            # Bit 18 DATAINV: Binary data inversion
            # Bit 17 TXINV: TX pin active level inversion
            # Bit 16 RXINV: RX pin active level inversion
            # Bit 15 SWAP: Swap TX/RX pins
            # Bit 14 LINEN: LIN mode enable
            # Bits 13:12 STOP[1:0]: STOP bits
            # Bit 11 CLKEN: Clock enable
            # Bit 10 CPOL: Clock polarity
            # Bit 9 CPHA: Clock phase
            # Bit 8 LBCL: Last bit clock pulse
            # Bit 6 LBDIE: LIN break detection interrupt enable
            # Bit 5 LBDL: LIN break detection length
            # Bit 4 ADDM7:7-bit Address Detection/4-bit Address Detection
        ]))

    self.append(MmapReg(
        name=f"{usart}_CR3", addr=(base + 0x08), descr="USART control register 3",
        bits=[
            # Bit 22 WUFIE: Wake-up from Stop mode interrupt enable
            # Bits 21:20 WUS[1:0]: Wake-up from Stop mode interrupt flag selection
            # Bits 19:17 SCARCNT[2:0]: Smartcard auto-retry count
            # Bit 15 DEP: Driver enable polarity selection
            # Bit 14 DEM: Driver enable mode
            # Bit 13 DDRE: DMA Disable on Reception Error
            # Bit 12 OVRDIS: Overrun Disable
            # Bit 11 ONEBIT: One sample bit method enable
            # Bit 10 CTSIE: CTS interrupt enable
            # Bit 9 CTSE: CTS enable
            # Bit 8 RTSE: RTS enable
            # Bit 7 DMAT: DMA enable transmitter
            # Bit 6 DMAR: DMA enable receiver
            # Bit 5 SCEN: Smartcard mode enable
            # Bit 4 NACK: Smartcard NACK enable
            # Bit 3 HDSEL: Half-duplex selection
            # Bit 2 IRLP: IrDA low-power
            # Bit 1 IREN: IrDA mode enable
            # Bit 0 EIE: Error interrupt enable
        ]))

    self.append(MmapReg(
        name=f"{usart}_BRR", addr=(base + 0x0C), descr="USART baud rate register",
        bits=[Bits(bits=range(0, 16), name="BRR")]))

    self.append(MmapReg(
        name=f"{usart}_GTPR", addr=(base + 0x10), descr="USART guard time and prescaler register",
        bits=[
            # Bits 15:8 GT[7:0]: Guard time value
            # Bits 7:0 PSC[7:0]: Prescaler value
        ]))

    self.append(MmapReg(
        name=f"{usart}_RTOR", addr=(base + 0x14), descr="USART receiver timeout register",
        bits=[
            # Bits 31:24 BLEN[7:0]: Block Length
            # Bits 23:0 RTO[23:0]: Receiver timeout value
        ]))

    self.append(MmapReg(
        name=f"{usart}_RQR", addr=(base + 0x18), descr="USART request register",
        bits=[
            # Bit 4 TXFRQ: Transmit data flush request
            # Bit 3 RXFRQ: Receive data flush request
            # Bit 2 MMRQ: Mute mode request
            # Bit 1 SBKRQ: Send break request
            # Bit 0 ABRRQ: Auto baud rate request
        ]))

    self.append(MmapReg(
        name=f"{usart}_ISR", addr=(base + 0x1C), descr="USART interrupt and status register",
        bits=[
            Bits(bits=22, name="REACK", descr="Receive enable acknowledge flag"),
            Bits(bits=21, name="TEACK", descr="Transmit enable acknowledge flag"),
            Bits(bits=20, name="WUF", descr="Wake-up from Stop mode flag"),
            Bits(bits=19, name="RWU", descr="Receiver wake-up from Mute mode"),
            Bits(bits=18, name="SBKF", descr="Send break flag"),
            Bits(bits=17, name="CMF", descr="Character match flag"),
            Bits(bits=16, name="BUSY", descr="Busy flag"),
            Bits(bits=15, name="ABRF", descr="Auto baud rate flag"),
            Bits(bits=14, name="ABRE", descr="Auto baud rate error"),
            Bits(bits=13, name="Reserved", descr="must be kept at reset value."),
            Bits(bits=12, name="EOBF", descr="End of block flag"),
            Bits(bits=11, name="RTOF", descr="Receiver timeout"),
            Bits(bits=10, name="CTS", descr="CTS flag"),
            Bits(bits=9, name="CTSIF", descr="CTS interrupt flag"),
            Bits(bits=8, name="LBDF", descr="LIN break detection flag"),
            Bits(bits=7, name="TXE", descr="Transmit data register empty"),
            Bits(bits=6, name="TC", descr="Transmission complete"),
            Bits(bits=5, name="RXNE", descr="Read data register not empty"),
            Bits(bits=4, name="IDLE", descr="Idle line detected"),
            Bits(bits=3, name="ORE", descr="Overrun error"),
            Bits(bits=2, name="NF", descr="START bit Noise detection flag"),
            Bits(bits=1, name="FE", descr="Framing error"),
            Bits(bits=0, name="PE", descr="Parity error"),
        ]))

    self.append(MmapReg(
        name=f"{usart}_ICR", addr=(base + 0x20), descr="USART interrupt flag clear register",
        bits=[
            # Bits 31:21 Reserved, must be kept at reset value.
            # Bit 20 WUCF: Wake-up from Stop mode clear flag
            # Bits 19:18 Reserved, must be kept at reset value.
            # Bit 17 CMCF: Character match clear flag
            # Bits 16:13 Reserved, must be kept at reset value.
            # Bit 12 EOBCF: End of block clear flag
            # Bit 11 RTOCF: Receiver timeout clear flag
            # Bit 10 Reserved, must be kept at reset value.
            # Bit 9 CTSCF: CTS clear flag
            # Bit 8 LBDCF: LIN break detection clear flag
            # Bit 7 Reserved, must be kept at reset value.
            # Bit 6 TCCF: Transmission complete clear flag
            # Bit 5 Reserved, must be kept at reset value.
            # Bit 4 IDLECF: Idle line detected clear flag
            # Bit 3 ORECF: Overrun error clear flag
            # Bit 2 NCF: Noise detected clear flag
            # Bit 1 FECF: Framing error clear flag
            # Bit 0 PECF: Parity error clear flag

        ]))

    self.append(MmapReg(
        name=f"{usart}_RDR", addr=(base + 0x24), descr="USART receive data register",
        bits=[
            # Bits 8:0 RDR[8:0]: Receive data value
        ]))

    self.append(MmapReg(
        name=f"{usart}_TDR", addr=(base + 0x28), descr="USART transmit data register",
        bits=[
            # Bits 8:0 TDR[8:0]: Transmit data value
        ]))
