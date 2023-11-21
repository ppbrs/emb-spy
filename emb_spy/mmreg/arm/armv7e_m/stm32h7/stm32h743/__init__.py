""" Module for class MmregSTM32H743."""
# Disabling line-too-long because it's impossible to keep human-readable descriptions short.
# pylint: disable=line-too-long


from emb_spy.mmreg.registers_if import Register, Registers, RegisterBits  # pylint: disable=import-error
from emb_spy.mmreg.arm.armv7e_m import MmregARMV7EM  # pylint: disable=import-error
from emb_spy.mmreg.arm.stm32 import MmregSTM32  # pylint: disable=import-error

from ._pwr import _Pwr
from ._tim2_tim3_tim4_tim5 import _Tim2Tim3Tim4Tim5


class MmregSTM32H743(Registers):
    """
    Generates Register objects for all peripherals of STM32H743.
    """
    ADC12_BASE = 0x40022000
    ADC3_BASE = 0x58026000
    BDMA_BASE = 0x58025400
    DMAMUX1_BASE = 0x40020800
    DMAMUX2_BASE = 0x58025800
    FLASH_BASE = 0x52002000
    GPIOA_BASE = 0x58020000
    GPIOB_BASE = 0x58020400
    GPIOC_BASE = 0x58020800
    GPIOD_BASE = 0x58020C00
    GPIOE_BASE = 0x58021000
    GPIOF_BASE = 0x58021400
    GPIOG_BASE = 0x58021800
    GPIOH_BASE = 0x58021C00
    GPIOI_BASE = 0x58022000
    GPIOJ_BASE = 0x58022400
    GPIOK_BASE = 0x58022800
    I2C1_BASE = 0x40005400
    I2C2_BASE = 0x40005800
    I2C3_BASE = 0x40005C00
    I2C4_BASE = 0x58001C00
    RCC_BASE = 0x58024400
    TIM1_BASE = 0x40010000
    TIM8_BASE = 0x40010400

    def __init__(self):
        self.regs = []
        self.regs += MmregARMV7EM().get_list()
        self._init_adc()
        self._init_bdma()
        self._init_dmamux()
        self._init_flash()
        self._init_gpio()
        self._init_i2c()
        self.regs += MmregSTM32.init_tim1_tim8(prefix="TIM1", base=self.TIM1_BASE)
        self.regs += MmregSTM32.init_tim1_tim8(prefix="TIM8", base=self.TIM8_BASE)
        self.regs += _Pwr().get_list()
        self.regs += _Tim2Tim3Tim4Tim5().get_list()
        self._init_rcc()

        # TODO: check if there are no registers with same names.

        # self.regs += [
        #     Register(name="TIM1_CR1", addr=(self.TIM1_BASE + 0x00), descr="todo"),
        #     Register(name="TIM1_CR2", addr=(self.TIM1_BASE + 0x04), descr="todo"),
        #     Register(name="TIM1_CNT", addr=(self.TIM1_BASE + 0x24), descr="todo"),
        # ]

    def _init_adc(self):

        adc1_master_base = self.ADC12_BASE + 0
        adc2_slave_base = self.ADC12_BASE + 0x100
        adc12_common_base = self.ADC12_BASE + 0x300
        adc3_master_base = self.ADC3_BASE + 0
        adc3_common_base = self.ADC3_BASE + 0x300

        register_bits_cr = [
            RegisterBits(bits=31, name="ADCAL", descr="ADC calibration"),
            RegisterBits(bits=30, name="ADCALDIF", descr="Differential mode for calibration"),
            RegisterBits(bits=29, name="DEEPPWD", descr="Deep-power-down enable"),
            RegisterBits(bits=28, name="ADVREGEN", descr="ADC voltage regulator enable"),
            RegisterBits(bits=16, name="ADCALLIN", descr="Linearity calibration"),
            RegisterBits(bits=8, name="BOOST", descr="Boost mode control"),
            RegisterBits(bits=5, name="JADSTP", descr="ADC stop of injected conversion command"),
            RegisterBits(bits=4, name="ADSTP", descr="ADC stop of regular conversion command"),
            RegisterBits(bits=3, name="JADSTART", descr="ADC start of injected conversion"),
            RegisterBits(bits=2, name="ADSTART", descr="ADC start of regular conversion"),
            RegisterBits(bits=1, name="ADDIS", descr="ADC disable command"),
            RegisterBits(bits=0, name="ADEN", descr="ADC enable control"),
        ]
        register_bits_smpr_values = {
            0b000: "1.5 ADC clock cycles",
            0b001: "2.5 ADC clock cycles",
            0b010: "8.5 ADC clock cycles",
            0b011: "16.5 ADC clock cycles",
            0b100: "32.5 ADC clock cycles",
            0b101: "64.5 ADC clock cycles",
            0b110: "387.5 ADC clock cycles",
            0b111: "810.5 ADC clock cycles", }
        register_bits_smpr1 = [
            RegisterBits(
                bits=range(3 * ch, 3 * ch + 3), name=f"SMP{ch}",
                descr=f"Channel {ch} sampling time selection",
                values=register_bits_smpr_values) for ch in range(0, 10)
        ]
        register_bits_smpr2 = [
            RegisterBits(
                bits=range(3 * (ch - 10), 3 * (ch - 10) + 3), name=f"SMP{ch}",
                descr=f"Channel {ch} sampling time selection",
                values=register_bits_smpr_values) for ch in range(10, 20)
        ]

        self.regs += [
            Register(
                name="ADC12_CCR", addr=(adc12_common_base + 0x08),
                descr="ADC12 common control register",
                register_bits=[
                    RegisterBits(
                        bits=23, name="PRESC", descr="ADC prescaler",
                        values={
                            0b0000: "input ADC clock not divided",
                            0b0001: "input ADC clock divided by 2",
                            0b0010: "input ADC clock divided by 4",
                            0b0011: "input ADC clock divided by 6",
                            0b0100: "input ADC clock divided by 8",
                            0b0101: "input ADC clock divided by 10",
                            0b0110: "input ADC clock divided by 12",
                            0b0111: "input ADC clock divided by 16",
                            0b1000: "input ADC clock divided by 32",
                            0b1001: "input ADC clock divided by 64",
                            0b1010: "input ADC clock divided by 128",
                            0b1011: "input ADC clock divided by 256", }),
                ],
            ),
            Register(
                name="ADC3_CCR", addr=(adc3_common_base + 0x08), descr="ADC3 common control register",
                register_bits=[
                    # Bit 24 VBATEN: VBAT enable
                    RegisterBits(bits=23, name="TSEN", descr="Temperature sensor voltage enable"),
                    # Bit 22 VREFEN: VREFINT enable
                    # Bits 21:18 PRESC[3:0]: ADC prescaler
                    # Bits 17:16 CKMODE[1:0]: ADC clock mode
                    # Bits 15:14 DAMDF[1:0]: Dual ADC Mode Data Format
                    # Bits 11:8 DELAY[3:0]: Delay between 2 sampling phases
                    # Bits 4:0 DUAL[4:0]: Dual ADC mode selection
                ],
            ),
            Register(
                name="ADC1_CR", addr=(adc1_master_base + 0x08),
                descr="ADC1 control register", register_bits=register_bits_cr,
            ),
            Register(
                name="ADC2_CR", addr=(adc2_slave_base + 0x08),
                descr="ADC2 control register", register_bits=register_bits_cr,
            ),
            Register(
                name="ADC3_CR", addr=(adc3_master_base + 0x08),
                descr="ADC3 control register", register_bits=register_bits_cr,
            ),
            Register(
                name="ADC1_SMPR1", addr=(adc1_master_base + 0x14),
                descr="ADC1 sample time register 1",
                register_bits=register_bits_smpr1,
            ),
            Register(
                name="ADC1_SMPR2", addr=(adc1_master_base + 0x18),
                descr="ADC1 sample time register 2",
                register_bits=register_bits_smpr2,
            ),
            Register(
                name="ADC1_SQR1", addr=(adc1_master_base + 0x30),
                descr="ADC1 regular sequence register 1",
                register_bits=[
                    RegisterBits(
                        bits=range(0, 4), name="L", descr="Regular channel sequence length",
                        values={val: f"{(val + 1)} conversions" for val in range(0, 16)}),
                    RegisterBits(bits=range(6, 11), name="SQ1", descr="1st conversion in regular sequence"),
                    RegisterBits(bits=range(12, 17), name="SQ2", descr="2nd conversion in regular sequence"),
                    RegisterBits(bits=range(18, 23), name="SQ3", descr="3rd conversion in regular sequence"),
                    RegisterBits(bits=range(24, 29), name="SQ4", descr="4th conversion in regular sequence"),
                ],
            ),
            Register(
                name="ADC1_SQR2", addr=(adc1_master_base + 0x34), descr="ADC1 regular sequence register 2",
                register_bits=[
                    RegisterBits(bits=range(0, 4 + 1), name="SQ5", descr="5th conversion in regular sequence"),
                    RegisterBits(bits=range(6, 10 + 1), name="SQ6", descr="6th conversion in regular sequence"),
                    RegisterBits(bits=range(12, 16 + 1), name="SQ7", descr="7th conversion in regular sequence"),
                    RegisterBits(bits=range(18, 22 + 1), name="SQ8", descr="8th conversion in regular sequence"),
                    RegisterBits(bits=range(24, 28 + 1), name="SQ9", descr="9th conversion in regular sequence"),

                ],
            ),
            Register(
                name="ADC1_SQR3", addr=(adc1_master_base + 0x38), descr="ADC1 regular sequence register 3",
                register_bits=[
# Bits 4:0 SQ10[4:0]: 10th conversion in regular sequence
# Bits 10:6 SQ11[4:0]: 11th conversion in regular sequence
# Bits 16:12 SQ12[4:0]: 12th conversion in regular sequence
# Bits 22:18 SQ13[4:0]: 13th conversion in regular sequence
# Bits 28:24 SQ14[4:0]: 14th conversion in regular sequence
                ],
            ),
            Register(
                name="ADC1_SQR4", addr=(adc1_master_base + 0x3C), descr="ADC1 regular sequence register 4",
                register_bits=[
# Bits 4:0 SQ15[4:0]: 15th conversion in regular sequence
# Bits 10:6 SQ16[4:0]: 16th conversion in regular sequence
                ],
            ),
        ]

    def _init_bdma(self):
        isr_bits = []
        for chnl in range(0, 8):
            isr_bits += [
                RegisterBits(
                    bits=(4 * chnl + 0), name=f"GIF{chnl}", descr=f"global interrupt flag for channel {chnl}",
                    values={1: "a TE, HT or TC event occurred", }
                ),
                RegisterBits(
                    bits=(4 * chnl + 1), name=f"TCIF{chnl}", descr=f"transfer complete (TC) flag for channel {chnl}",
                    values={1: "a TC event occurred", }
                ),
                RegisterBits(
                    bits=(4 * chnl + 2), name=f"HTIF{chnl}", descr=f"half transfer (HT) flag for channel {chnl}",
                    values={1: "a HT event occurred", }
                ),
                RegisterBits(
                    bits=(4 * chnl + 3), name=f"TEIF{chnl}", descr=f"transfer error (TE) flag for channel {chnl}",
                    values={1: "a TE event occurred", }
                ),
            ]

        self.regs += [
            Register(name="BDMA_ISR", addr=(self.BDMA_BASE + 0x00), descr="BDMA interrupt status", register_bits=isr_bits),
        ]

        for chnl in range(0, 8):
            self.regs += [
                Register(
                    name=f"BDMA_CCR{chnl}", addr=(self.BDMA_BASE + 0x08 + 0x14 * chnl), descr=f"BDMA channel {chnl} configuration register",
                    register_bits=[
                        RegisterBits(bits=0, name="EN", descr="channel enable", values={}),
                        RegisterBits(bits=1, name="TCIE", descr="transfer complete interrupt enable", values={}),
                        RegisterBits(bits=2, name="HTIE", descr="half transfer interrupt enable", values={}),
                        RegisterBits(bits=3, name="TEIE", descr="transfer error interrupt enable", values={}),
                        RegisterBits(bits=4, name="DIR", descr="data transfer direction",
                                     values={0: "read from peripheral", 1: "read from memory"}),
                        RegisterBits(bits=5, name="CIRC", descr="circular mode", values={}),
                        RegisterBits(bits=6, name="PINC", descr="peripheral increment mode", values={}),
                        RegisterBits(bits=7, name="MINC", descr="memory increment mode", values={}),
                        RegisterBits(bits=range(8, 10), name="PSIZE", descr="peripheral size",
                                     values={0: "8 bits", 1: "16 bits", 2: "32 bits", 3: "reserved"}),
                        RegisterBits(bits=range(10, 12), name="MSIZE", descr="memory size",
                                     values={0: "8 bits", 1: "16 bits", 2: "32 bits", 3: "reserved"}),
                        RegisterBits(bits=range(12, 14), name="PL", descr="priority level",
                                     values={0: "low", 1: "medium", 2: "high", 3: "very high", }),
                        RegisterBits(bits=14, name="MEM2MEM", descr="memory-to-memory mode", values={}),
                        RegisterBits(bits=15, name="DBM", descr="double-buffer mode", values={}),
                        RegisterBits(bits=16, name="CT", descr="current target memory of DMA transfer in double-buffer mode",
                                     values={0: "memory 0 (addressed by the BDMA_CM0AR pointer)", 1: "memory 1 (addressed by the BDMA_CM1AR pointer)", }),
                    ]),
                Register(name=f"BDMA_CNDTR{chnl}", addr=(self.BDMA_BASE + 0x0C + 0x14 * chnl), descr=f"BDMA channel {chnl} number of data to transfer register"),
                Register(name=f"BDMA_CPAR{chnl}", addr=(self.BDMA_BASE + 0x10 + 0x14 * chnl), descr=f"BDMA channel {chnl} peripheral address register"),
                Register(name=f"BDMA_CM0AR{chnl}", addr=(self.BDMA_BASE + 0x14 + 0x14 * chnl), descr=f"BDMA channel {chnl} memory 0 address register"),
                Register(name=f"BDMA_CM1AR{chnl}", addr=(self.BDMA_BASE + 0x18 + 0x14 * chnl), descr=f"BDMA channel {chnl} memory 1 address register"),
            ]

    def _init_dmamux(self):

        for per in [1, 2]:
            chnl_count = 16 if per == 1 else 8
            dmamux_base = self.DMAMUX1_BASE if per == 1 else self.DMAMUX2_BASE
            for chnl in range(0, chnl_count):
                self.regs += [
                    Register(
                        name=f"DMAMUX{per}_C{chnl}CR", addr=(dmamux_base + 0x04 * chnl),
                        descr=f"DMAMUX{per} request line multiplexer channel {chnl} configuration register",
                        register_bits=[
                              RegisterBits(bits=range(0, 7), name="DMAREQ_ID", descr="DMA request identification"),
                            # Bit 9 EGE: Event generation enable
                            # Bit 8 SOIE: Synchronization overrun interrupt enable
                            # Bit 16 SE: Synchronization enable
                            # Bits 18:17 SPOL[1:0]: Synchronization polarity
                            # Bits 23:19 NBREQ[4:0]: Number of DMA requests minus 1 to forward
                            # Bits 26:24 SYNC_ID[2:0]: Synchronization identification
                        ]),
                ]

        self.regs += [
            Register(
                name="DMAMUX1_CSR", addr=(self.DMAMUX1_BASE + 0x080),
                descr="DMAMUX1 request line multiplexer interrupt channel status register",
                register_bits=[]),
            Register(
                name="DMAMUX2_CSR", addr=(self.DMAMUX2_BASE + 0x080),
                descr="DMAMUX2 request line multiplexer interrupt channel status register",
                register_bits=[]),
        ]

    def _init_flash(self):
        self.regs += [
            Register(
                name="FLASH_OPTSR_CUR", addr=(self.FLASH_BASE + 0x01C),
                descr="Reflects the current values of corresponding option bits",
                comment="These bits reflects the power level that generates a system reset",
                register_bits=[
                    RegisterBits(
                        bits=range(2, 4), name="BOR_LEV", descr="Brownout level option status bit",
                        values={
                            0b00: "VBOR0, brownout reset threshold 0 (1.67..1.62 V)",
                            0b01: "VBOR1, brownout reset threshold 1 (2.10..2.00 V)",
                            0b10: "VBOR2, brownout reset threshold 2 (2.41..2.31 V)",
                            0b11: "VBOR3, brownout reset threshold 3 (2.70..2.61 V)",
                        }),
                ]),
        ]

    def _init_gpio(self):
        self.regs += MmregSTM32.init_gpio(prefix="GPIOA", base=self.GPIOA_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOB", base=self.GPIOB_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOC", base=self.GPIOC_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOD", base=self.GPIOD_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOE", base=self.GPIOE_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOF", base=self.GPIOF_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOG", base=self.GPIOG_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOH", base=self.GPIOH_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOI", base=self.GPIOI_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOJ", base=self.GPIOJ_BASE)
        self.regs += MmregSTM32.init_gpio(prefix="GPIOK", base=self.GPIOK_BASE)

    def _init_i2c(self):

        for x, i2cx_base in enumerate([self.I2C1_BASE, self.I2C2_BASE, self.I2C3_BASE, self.I2C4_BASE], start=1):
            self.regs += [
                Register(
                    name=f"I2C{x}_CR1", addr=(i2cx_base + 0x00), descr=f"I2C{x} control register 1",
                    register_bits=[

                        # Bit 23 PECEN: PEC enable
                        # Bit 22 ALERTEN: SMBus alert enable
                        # Bit 21 SMBDEN: SMBus Device Default Address enable
                        # Bit 20 SMBHEN: SMBus Host Address enable
                        # Bit 19 GCEN: General call enable
                        # Bit 18 WUPEN: Wakeup from Stop mode enable
                        # Bit 17 NOSTRETCH: Clock stretching disable
                        # Bit 16 SBC: Slave byte control
                        RegisterBits(bits=15, name="RXDMAEN", descr="DMA reception requests enable"),
                        RegisterBits(bits=14, name="TXDMAEN", descr="DMA transmission requests enable"),
                        # Bit 12 ANFOFF: Analog noise filter OFF
                        # Bits 11:8 DNF[3:0]: Digital noise filter
                        # Bit 7 ERRIE: Error interrupts enable
                        # Bit 6 TCIE: Transfer Complete interrupt enable
                        # Bit 5 STOPIE: Stop detection Interrupt enable
                        # Bit 4 NACKIE: Not acknowledge received Interrupt enable
                        # Bit 3 ADDRIE: Address match Interrupt enable (slave only)
                        # Bit 2 RXIE: RX Interrupt enable
                        # Bit 1 TXIE: TX Interrupt enable
                        RegisterBits(bits=0, name="PE", descr="Peripheral enable"),
                    ],
                ),
                Register(
                    name=f"I2C{x}_CR2", addr=(i2cx_base + 0x04), descr=f"I2C{x} control register 2",
                    register_bits=[
                        RegisterBits(bits=range(0, 10), name="SADD", descr="Slave address (master mode)"),
                        RegisterBits(bits=10, name="RD_WRN", descr="Transfer direction (master mode)",
                                     values={
                                         0: "Master requests a write transfer.",
                                         1: "Master requests a read transfer.", }),
                        RegisterBits(bits=11, name="ADD10", descr="10-bit addressing mode"),
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
                ),
                Register(
                    name=f"I2C{x}_OAR1", addr=(i2cx_base + 0x08), descr=f"I2C{x} own address 1 register",
                    register_bits=[],
                ),
                Register(
                    name=f"I2C{x}_OAR2", addr=(i2cx_base + 0x0C), descr=f"I2C{x} own address 2 register",
                    register_bits=[],
                ),
                Register(
                    name=f"I2C{x}_TIMINGR", addr=(i2cx_base + 0x10), descr=f"I2C{x} timing register",
                    register_bits=[
                        RegisterBits(bits=range(0, 8), name="SCLL", descr="SCL low period (master mode)"),
                        RegisterBits(bits=range(8, 16), name="SCLH", descr="SCL high period (master mode)"),
                        RegisterBits(bits=range(16, 20), name="SDADEL", descr="Data hold time"),
                        RegisterBits(bits=range(20, 24), name="SCLDEL", descr="Data setup time"),
                        RegisterBits(bits=range(28, 32), name="PRESC", descr="Timing prescaler"),
                    ],
                ),
                Register(
                    name=f"I2C{x}_TIMEOUTR", addr=(i2cx_base + 0x14), descr=f"I2C{x} timeout register",
                    register_bits=[],
                ),
                Register(
                    name=f"I2C{x}_ISR", addr=(i2cx_base + 0x18), descr=f"I2C{x} interrupt and status register",
                    register_bits=[
                        RegisterBits(bits=0, name="TXE", descr="Transmit data register empty (transmitters)"),
                        RegisterBits(bits=1, name="TXIS", descr="Transmit interrupt status (transmitters)"),
                        RegisterBits(bits=2, name="RXNE", descr="Receive data register not empty (receivers)"),
                        RegisterBits(bits=3, name="ADDR", descr="Address matched (slave mode)"),
                        RegisterBits(bits=4, name="NACKF", descr="Not Acknowledge received flag"),
                        RegisterBits(bits=5, name="STOPF", descr="Stop detection flag"),
                        RegisterBits(bits=6, name="TC", descr="Transfer Complete (master mode)"),
                        RegisterBits(bits=7, name="TCR", descr="Transfer Complete Reload"),
                        RegisterBits(bits=8, name="BERR", descr="Bus error"),
                        RegisterBits(bits=9, name="ARLO", descr="Arbitration lost"),
                        RegisterBits(bits=10, name="OVR", descr="Overrun/Underrun (slave mode)"),
                        RegisterBits(bits=11, name="PECERR", descr="PEC Error in reception"),
                        RegisterBits(bits=12, name="TIMEOUT", descr="Timeout or tLOW detection flag"),
                        RegisterBits(bits=13, name="ALERT", descr="SMBus alert"),
                        RegisterBits(bits=15, name="BUSY", descr="Bus busy"),
                        RegisterBits(bits=16, name="DIR", descr="Transfer direction (Slave mode)"),
                        RegisterBits(bits=range(17, 24), name="ADDCODE", descr="Address match code (Slave mode)"),
                    ],
                ),
            ]

    def _init_rcc(self):
        self.regs += [
            Register(
                name="RCC_D3CFGR", addr=(self.RCC_BASE + 0x020),
                descr="RCC Domain 3 Clock Configuration Register",
                register_bits=[
                    RegisterBits(
                        bits=range(4, 7), name="D3PPRE", descr="D3 domain APB4 prescaler",
                        values={})
                ]
            ),

            Register(
                name="RCC_D1CCIPR", addr=(self.RCC_BASE + 0x04C),
                descr="RCC Domain 1 Kernel Clock Configuration Register",
                register_bits=[
                ]
            ),
            Register(
                name="RCC_D2CCIP1R", addr=(self.RCC_BASE + 0x050),
                descr="RCC Domain 2 Kernel Clock Configuration Register",
                register_bits=[
                ]
            ),
            Register(
                name="RCC_D2CCIP2R", addr=(self.RCC_BASE + 0x054),
                descr="RCC Domain 2 Kernel Clock Configuration Register",
                register_bits=[
                    RegisterBits(
                        bits=[12, 13], name="I2C123SEL", descr="I2C1,2,3 kernel clock source selection",
                        values={
                            0: "rcc_pclk1 clock is selected as kernel clock (default after reset)",
                            1: "pll3_r_ck clock is selected as kernel clock",
                            2: "hsi_ker_ck clock is selected as kernel clock",
                            3: "csi_ker_ck clock is selected as kernel clock", })
                ]
            ),
            Register(
                name="RCC_D3CCIPR", addr=(self.RCC_BASE + 0x058),
                descr="RCC Domain 3 Kernel Clock Configuration Register",
                register_bits=[
                    RegisterBits(
                        bits=[8, 9], name="I2C4SEL", descr="I2C4 kernel clock source selection",
                        values={
                            0: "rcc_pclk4 clock selected as kernel peripheral clock (default after reset)",
                            1: "pll3_r_ck clock selected as kernel peripheral clock",
                            2: "hsi_ker_ck clock selected as kernel peripheral clock,",
                            3: "csi_ker_ck clock selected as kernel peripheral clock", }),
                ]
            ),
            Register(
                name="RCC_APB1LENR", addr=(self.RCC_BASE + 0x0E8), descr="RCC APB1 Clock Register",
                register_bits=[
                    RegisterBits(bits=31, name="UART8EN", descr="UART8 Peripheral Clocks Enable"),
                    RegisterBits(bits=30, name="UART7EN", descr="UART7 Peripheral Clocks Enable"),
                    RegisterBits(bits=29, name="DAC12EN", descr="DAC1 and 2 peripheral clock enable"),
                    RegisterBits(bits=27, name="CECEN", descr="HDMI-CEC peripheral clock enable"),
                    RegisterBits(bits=23, name="I2C3EN", descr="I2C3 Peripheral Clocks Enable"),
                    RegisterBits(bits=22, name="I2C2EN", descr="I2C2 Peripheral Clocks Enable"),
                    RegisterBits(bits=21, name="I2C1EN", descr="I2C1 Peripheral Clocks Enable"),
                    RegisterBits(bits=20, name="UART5EN", descr="UART5 Peripheral Clocks Enable"),
                    RegisterBits(bits=19, name="UART4EN", descr="UART4 Peripheral Clocks Enable"),
                    RegisterBits(bits=18, name="USART3EN", descr="USART3 Peripheral Clocks Enable"),
                    RegisterBits(bits=17, name="USART2EN", descr="USART2 Peripheral Clocks Enable"),
                    RegisterBits(bits=16, name="SPDIFRXEN", descr="SPDIFRX Peripheral Clocks Enable"),
                    RegisterBits(bits=15, name="SPI3EN", descr="SPI3 Peripheral Clocks Enable"),
                    RegisterBits(bits=14, name="SPI2EN", descr="SPI2 Peripheral Clocks Enable"),
                    RegisterBits(bits=9, name="LPTIM1EN", descr="LPTIM1 Peripheral Clocks Enable"),
                    RegisterBits(bits=8, name="TIM14EN", descr="TIM14 peripheral clock enable"),
                    RegisterBits(bits=7, name="TIM13EN", descr="TIM13 peripheral clock enable"),
                    RegisterBits(bits=6, name="TIM12EN", descr="TIM12 peripheral clock enable"),
                    RegisterBits(bits=5, name="TIM7EN", descr="TIM7 peripheral clock enable"),
                    RegisterBits(bits=4, name="TIM6EN", descr="TIM6 peripheral clock enable"),
                    RegisterBits(bits=3, name="TIM5EN", descr="TIM5 peripheral clock enable"),
                    RegisterBits(bits=2, name="TIM4EN", descr="TIM4 peripheral clock enable"),
                    RegisterBits(bits=1, name="TIM3EN", descr="TIM3 peripheral clock enable"),
                    RegisterBits(bits=0, name="TIM2EN", descr="TIM2 peripheral clock enable"),
                ]
            ),
            Register(
                name="RCC_APB1HENR", addr=(self.RCC_BASE + 0x0EC), descr="RCC APB1 Clock Register",
                register_bits=[
                    RegisterBits(bits=8, name="FDCANEN", descr="FDCAN Peripheral Clocks Enable"),
                    RegisterBits(bits=5, name="MDIOSEN", descr="MDIOS peripheral clock enable"),
                    RegisterBits(bits=4, name="OPAMPEN", descr="OPAMP peripheral clock enable"),
                    RegisterBits(bits=2, name="SWPEN", descr="SWPMI Peripheral Clocks Enable"),
                    RegisterBits(bits=1, name="CRSEN", descr="Clock Recovery System peripheral clock enable"),
                ]
            ),
            Register(
                name="RCC_APB2ENR", addr=(self.RCC_BASE + 0x0F0), descr="RCC APB2 Clock Register",
                register_bits=[
                    RegisterBits(bits=29, name="HRTIMEN", descr="HRTIM peripheral clock enable"),
                    RegisterBits(bits=28, name="DFSDM1EN", descr="DFSDM1 Peripheral Clocks Enable"),
                    RegisterBits(bits=24, name="SAI3EN", descr="SAI3 Peripheral Clocks Enable"),
                    RegisterBits(bits=23, name="SAI2EN", descr="SAI2 Peripheral Clocks Enable"),
                    RegisterBits(bits=22, name="SAI1EN", descr="SAI1 Peripheral Clocks Enable"),
                    RegisterBits(bits=20, name="SPI5EN", descr="SPI5 Peripheral Clocks Enable"),
                    RegisterBits(bits=18, name="TIM17EN", descr="TIM17 peripheral clock enable"),
                    RegisterBits(bits=17, name="TIM16EN", descr="TIM16 peripheral clock enable"),
                    RegisterBits(bits=16, name="TIM15EN", descr="TIM15 peripheral clock enable"),
                    RegisterBits(bits=13, name="SPI4EN", descr="SPI4 Peripheral Clocks Enable"),
                    RegisterBits(bits=12, name="SPI1EN", descr="SPI1 Peripheral Clocks Enable"),
                    RegisterBits(bits=5, name="USART6EN", descr="USART6 Peripheral Clocks Enable"),
                    RegisterBits(bits=4, name="USART1EN", descr="USART1 Peripheral Clocks Enable"),
                    RegisterBits(bits=1, name="TIM8EN", descr="TIM8 peripheral clock enable"),
                    RegisterBits(bits=0, name="TIM1EN", descr="TIM1 peripheral clock enable"),
                ]
            ),
            Register(
                name="RCC_APB3ENR", addr=(self.RCC_BASE + 0x0E4), descr="RCC APB3 Clock Register",
                register_bits=[
                    RegisterBits(bits=6, name="WWDG1EN", descr="WWDG1 Clock Enable"),
                    RegisterBits(bits=3, name="LTDCEN", descr="LTDC peripheral clock enable"),
                ]
            ),
            Register(
                name="RCC_APB4ENR", addr=(self.RCC_BASE + 0x0F4), descr="RCC APB4 Clock Register",
                register_bits=[
                    RegisterBits(bits=21, name="SAI4EN", descr="SAI4 Peripheral Clocks Enable"),
                    RegisterBits(bits=16, name="RTCAPBEN", descr="RTC APB Clock Enable"),
                    RegisterBits(bits=15, name="VREFEN", descr="VREF peripheral clock enable"),
                    RegisterBits(bits=14, name="COMP12EN", descr="COMP1/2 peripheral clock enable"),
                    RegisterBits(bits=12, name="LPTIM5EN", descr="LPTIM5 Peripheral Clocks Enable"),
                    RegisterBits(bits=11, name="LPTIM4EN", descr="LPTIM4 Peripheral Clocks Enable"),
                    RegisterBits(bits=10, name="LPTIM3EN", descr="LPTIM3 Peripheral Clocks Enable"),
                    RegisterBits(bits=9, name="LPTIM2EN", descr="LPTIM2 Peripheral Clocks Enable"),
                    RegisterBits(bits=7, name="I2C4EN", descr="I2C4 Peripheral Clocks Enable"),
                    RegisterBits(bits=5, name="SPI6EN", descr="SPI6 Peripheral Clocks Enable"),
                    RegisterBits(bits=3, name="LPUART1EN", descr="LPUART1 Peripheral Clocks Enable"),
                    RegisterBits(bits=1, name="SYSCFGEN", descr="SYSCFG peripheral clock enable"),
                ]
            ),
            Register(
                name="RCC_AHB1ENR", addr=(self.RCC_BASE + 0x0D8), descr="RCC AHB1 Clock Register",
                register_bits=[
                ]
            ),
            Register(
                name="RCC_AHB2ENR", addr=(self.RCC_BASE + 0x0DC), descr="RCC AHB2 Clock Register",
                register_bits=[
                ]
            ),
            Register(
                name="RCC_AHB3ENR", addr=(self.RCC_BASE + 0x0D4), descr="RCC AHB3 Clock Register",
                register_bits=[
                ]
            ),
            Register(
                name="RCC_AHB4ENR", addr=(self.RCC_BASE + 0x0E0), descr="RCC AHB4 Clock Register",
                register_bits=[
                    RegisterBits(bits=28, name="BKPRAMEN", descr="Backup RAM Clock Enable"),
                    RegisterBits(bits=25, name="HSEMEN", descr="HSEM peripheral clock enable"),
                    RegisterBits(bits=24, name="ADC3EN", descr="ADC3 Peripheral Clocks Enable"),
                    RegisterBits(bits=21, name="BDMAEN", descr="BDMA and DMAMUX2 Clock Enable"),
                    RegisterBits(bits=19, name="CRCEN", descr="CRC peripheral clock enable"),
                    RegisterBits(bits=10, name="GPIOKEN", descr="GPIOK peripheral clock enable"),
                    RegisterBits(bits=9, name="GPIOJEN", descr="GPIOJ peripheral clock enable"),
                    RegisterBits(bits=8, name="GPIOIEN", descr="GPIOI peripheral clock enable"),
                    RegisterBits(bits=7, name="GPIOHEN", descr="GPIOH peripheral clock enable"),
                    RegisterBits(bits=6, name="GPIOGEN", descr="GPIOG peripheral clock enable"),
                    RegisterBits(bits=5, name="GPIOFEN", descr="GPIOF peripheral clock enable"),
                    RegisterBits(bits=4, name="GPIOEEN", descr="GPIOE peripheral clock enable"),
                    RegisterBits(bits=3, name="GPIODEN", descr="GPIOD peripheral clock enable"),
                    RegisterBits(bits=2, name="GPIOCEN", descr="GPIOC peripheral clock enable"),
                    RegisterBits(bits=1, name="GPIOBEN", descr="GPIOB peripheral clock enable"),
                    RegisterBits(bits=0, name="GPIOAEN", descr="GPIOA peripheral clock enable"),
                ]
            ),
        ]
