"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_i2c(self: SoC):
    assert self.__class__.__name__ == "STM32H743"

    for x, i2cx_base in enumerate(
            [self.I2C1_BASE, self.I2C2_BASE, self.I2C3_BASE, self.I2C4_BASE],
            start=1):
        self.append(MmapReg(
            name=f"I2C{x}_CR1", addr=(i2cx_base + 0x00), descr=f"I2C{x} control register 1",
            bits=[

                # Bit 23 PECEN: PEC enable
                # Bit 22 ALERTEN: SMBus alert enable
                # Bit 21 SMBDEN: SMBus Device Default Address enable
                # Bit 20 SMBHEN: SMBus Host Address enable
                # Bit 19 GCEN: General call enable
                # Bit 18 WUPEN: Wakeup from Stop mode enable
                # Bit 17 NOSTRETCH: Clock stretching disable
                # Bit 16 SBC: Slave byte control
                Bits(bits=15, name="RXDMAEN", descr="DMA reception requests enable"),
                Bits(bits=14, name="TXDMAEN", descr="DMA transmission requests enable"),
                # Bit 12 ANFOFF: Analog noise filter OFF
                # Bits 11:8 DNF[3:0]: Digital noise filter
                # Bit 7 ERRIE: Error interrupts enable
                # Bit 6 TCIE: Transfer Complete interrupt enable
                # Bit 5 STOPIE: Stop detection Interrupt enable
                # Bit 4 NACKIE: Not acknowledge received Interrupt enable
                # Bit 3 ADDRIE: Address match Interrupt enable (slave only)
                # Bit 2 RXIE: RX Interrupt enable
                # Bit 1 TXIE: TX Interrupt enable
                Bits(bits=0, name="PE", descr="Peripheral enable"),
            ],
        ))
        self.append(MmapReg(
            name=f"I2C{x}_CR2", addr=(i2cx_base + 0x04), descr=f"I2C{x} control register 2",
            bits=[
                Bits(bits=range(0, 10), name="SADD", descr="Slave address (master mode)"),
                Bits(bits=10, name="RD_WRN", descr="Transfer direction (master mode)",
                     descr_vals={
                         0: "Master requests a write transfer.",
                         1: "Master requests a read transfer.", }),
                Bits(bits=11, name="ADD10", descr="10-bit addressing mode"),
                # Bit 11 ADD10: 10-bit addressing mode (master mode)
                # Bit 12 HEAD10R: 10-bit address header only read direction (master receiver mode)
                # Bit 13 START: Start generation
                # Bit 14 STOP: Stop generation (master mode)
                # Bit 15 NACK: NACK generation (slave mode)
                # Bits 23:16 NBYTES[7:0]: Number of bytes
                # Bit 24 RELOAD: NBYTES reload mode
                # Bit 25 AUTOEND: Automatic end mode (master mode)
                # Bit 26 PECBYTE: Packet error checking byte
            ]
        ))
        self.append(MmapReg(
            name=f"I2C{x}_OAR1", addr=(i2cx_base + 0x08), descr=f"I2C{x} own address 1 register",
            bits=[],
        ))
        self.append(MmapReg(
            name=f"I2C{x}_OAR2", addr=(i2cx_base + 0x0C), descr=f"I2C{x} own address 2 register",
            bits=[],
        ))
        self.append(MmapReg(
            name=f"I2C{x}_TIMINGR", addr=(i2cx_base + 0x10), descr=f"I2C{x} timing register",
            bits=[
                Bits(bits=range(0, 8), name="SCLL", descr="SCL low period (master mode)"),
                Bits(bits=range(8, 16), name="SCLH", descr="SCL high period (master mode)"),
                Bits(bits=range(16, 20), name="SDADEL", descr="Data hold time"),
                Bits(bits=range(20, 24), name="SCLDEL", descr="Data setup time"),
                Bits(bits=range(28, 32), name="PRESC", descr="Timing prescaler"),
            ],
        ))
        self.append(MmapReg(
            name=f"I2C{x}_TIMEOUTR", addr=(i2cx_base + 0x14), descr=f"I2C{x} timeout register",
            bits=[],
        ))
        self.append(MmapReg(
            name=f"I2C{x}_ISR", addr=(i2cx_base + 0x18),
            descr=f"I2C{x} interrupt and status register",
            bits=[
                Bits(bits=0, name="TXE", descr="Transmit data register empty (transmitters)"),
                Bits(bits=1, name="TXIS", descr="Transmit interrupt status (transmitters)"),
                Bits(bits=2, name="RXNE", descr="Receive data register not empty (receivers)"),
                Bits(bits=3, name="ADDR", descr="Address matched (slave mode)"),
                Bits(bits=4, name="NACKF", descr="Not Acknowledge received flag"),
                Bits(bits=5, name="STOPF", descr="Stop detection flag"),
                Bits(bits=6, name="TC", descr="Transfer Complete (master mode)"),
                Bits(bits=7, name="TCR", descr="Transfer Complete Reload"),
                Bits(bits=8, name="BERR", descr="Bus error"),
                Bits(bits=9, name="ARLO", descr="Arbitration lost"),
                Bits(bits=10, name="OVR", descr="Overrun/Underrun (slave mode)"),
                Bits(bits=11, name="PECERR", descr="PEC Error in reception"),
                Bits(bits=12, name="TIMEOUT", descr="Timeout or tLOW detection flag"),
                Bits(bits=13, name="ALERT", descr="SMBus alert"),
                Bits(bits=15, name="BUSY", descr="Bus busy"),
                Bits(bits=16, name="DIR", descr="Transfer direction (Slave mode)"),
                Bits(bits=range(17, 24), name="ADDCODE", descr="Address match code (Slave mode)"),
            ],
        ))
