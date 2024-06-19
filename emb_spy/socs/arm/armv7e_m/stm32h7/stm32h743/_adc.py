"""Part of STM32H743 SoC."""

from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC

ADC12_BASE = 0x40022000
ADC3_BASE = 0x58026000


def init_adc(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"

    _init_common(self)

    adc1_master_base = ADC12_BASE + 0
    adc2_slave_base = ADC12_BASE + 0x100
    adc3_master_base = ADC3_BASE + 0
    _init_individual(self, idx=1, base=adc1_master_base)
    _init_individual(self, idx=2, base=adc2_slave_base)
    _init_individual(self, idx=3, base=adc3_master_base)


def _init_individual(self: SoC, idx: int, base: int) -> None:
    assert self.__class__.__name__ == "STM32H743"
    adc = f"ADC{idx}"
    # ----------------------------------------------------------------------------------------------
    bits_cr = [
        Bits(bits=31, name="ADCAL", descr="ADC calibration"),
        Bits(bits=30, name="ADCALDIF", descr="Differential mode for calibration"),
        Bits(bits=29, name="DEEPPWD", descr="Deep-power-down enable"),
        Bits(bits=28, name="ADVREGEN", descr="ADC voltage regulator enable"),
        Bits(bits=16, name="ADCALLIN", descr="Linearity calibration"),
        Bits(
            bits=range(8, 10),
            name="BOOST",
            descr="Boost mode control",
        ),
        # 00: used when ADC clock ≤ 6.25 MHz
        # 01: used when 6.25 MHz < ADC clock frequency ≤ 12.5 MHz
        # 10: used when 12.5 MHz < ADC clock ≤ 25.0 MHz
        # 11: used when 25.0 MHz < ADC clock ≤ 50.0 MHz
        Bits(bits=5, name="JADSTP", descr="ADC stop of injected conversion command"),
        Bits(bits=4, name="ADSTP", descr="ADC stop of regular conversion command"),
        Bits(bits=3, name="JADSTART", descr="ADC start of injected conversion"),
        Bits(bits=2, name="ADSTART", descr="ADC start of regular conversion"),
        Bits(bits=1, name="ADDIS", descr="ADC disable command"),
        Bits(bits=0, name="ADEN", descr="ADC enable control"),
    ]
    self.append(
        MmapReg(
            name=f"{adc}_CR",
            addr=(base + 0x08),
            descr="ADC1 control register",
            bits=bits_cr,
        )
    )
    # ----------------------------------------------------------------------------------------------
    self.append(
        MmapReg(
            name=f"{adc}_ISR",
            addr=(base + 0x00),
            descr="ADC interrupt and status register",
            bits=[
                Bits(bits=12, name="LDORDY", descr="ADC LDO output voltage ready bit."),
                Bits(bits=10, name="JQOVF", descr="Injected context queue overflow."),
                Bits(bits=9, name="AWD3", descr="Analog watchdog 3 flag."),
                Bits(bits=8, name="AWD2", descr="Analog watchdog 2 flag."),
                Bits(bits=7, name="AWD1", descr="Analog watchdog 1 flag."),
                Bits(bits=6, name="JEOS", descr="Injected channel end of sequence flag."),
                Bits(bits=5, name="JEOC", descr="Injected channel end of conversion flag."),
                Bits(bits=4, name="OVR", descr="ADC overrun."),
                Bits(bits=3, name="EOS", descr="End of regular sequence flag."),
                Bits(bits=2, name="EOC", descr="End of conversion flag."),
                Bits(bits=1, name="EOSMP", descr="End of sampling flag."),
                Bits(bits=0, name="ADRDY", descr="ADC ready."),
            ],
        )
    )
    # ----------------------------------------------------------------------------------------------
    self.append(
        MmapReg(
            name=f"{adc}_CFGR",
            addr=(base + 0x0C),
            descr="ADC configuration register",
            bits=[
                Bits(bits=[0, 1], name="DMNGT", descr="Data Management configuration."),
                # 00: Regular conversion data stored in DR only
                # 01: DMA One Shot Mode selected
                # 10: DFSDM mode selected
                # 11: DMA Circular Mode selected
                Bits(bits=[2, 3, 4], name="RES", descr="Data resolution."),
                # 000: 16 bits
                # 001: 14 bits (for devices revision Y)
                # 101: 14 bits (for devices revision V)
                # 010: 12 bits (for devices revision Y)
                # 110: 12 bits (for devices revision V)
                # 011: 10 bits
                # 100: 8 bits (for devices revision Y)
                # 111: 8 bits (for devices revision V)
                Bits(
                    bits=range(5, 10),
                    name="EXTSEL",
                    descr="External trigger selection for regular group.",
                ),
                Bits(
                    bits=range(10, 12),
                    name="EXTEN",
                    descr="External trigger enable and polarity selection for regular channel.",
                ),
                Bits(
                    bits=13,
                    name="CONT",
                    descr="Single / continuous conversion mode for regular conversions.",
                ),
                Bits(bits=16, name="DISCEN", descr="Discontinuous mode for regular channels."),
                Bits(bits=31, name="JQDIS", descr="Injected Queue disable."),
            ],
        )
    )
    # ----------------------------------------------------------------------------------------------
    self.append(
        MmapReg(
            name=f"{adc}_CFGR2",
            addr=(base + 0x10),
            descr="ADC configuration register 2",
            bits=[
                Bits(bits=range(28, 32), name="LSHIFT", descr="Left shift factor."),
                Bits(bits=range(16, 26), name="OSVR", descr="Oversampling ratio."),
                Bits(bits=14, name="RSHIFT4", descr="Right-shift data after Offset 4 correction."),
                Bits(bits=13, name="RSHIFT3", descr="Right-shift data after Offset 3 correction."),
                Bits(bits=12, name="RSHIFT2", descr="Right-shift data after Offset 2 correction."),
                Bits(bits=11, name="RSHIFT1", descr="Right-shift data after Offset 1 correction."),
                Bits(bits=10, name="ROVSM", descr="Regular Oversampling mode."),
                Bits(bits=9, name="TROVS", descr="Triggered Regular Oversampling."),
                Bits(bits=range(5, 9), name="OVSS", descr="Oversampling right shift."),
                Bits(bits=1, name="JOVSE", descr="Injected Oversampling Enable."),
                Bits(bits=0, name="ROVSE", descr="Regular Oversampling Enable."),
            ],
        )
    )
    # ----------------------------------------------------------------------------------------------
    bits_smpr_values = {
        0b000: "1.5 ADC clock cycles",
        0b001: "2.5 ADC clock cycles",
        0b010: "8.5 ADC clock cycles",
        0b011: "16.5 ADC clock cycles",
        0b100: "32.5 ADC clock cycles",
        0b101: "64.5 ADC clock cycles",
        0b110: "387.5 ADC clock cycles",
        0b111: "810.5 ADC clock cycles",
    }
    bits_smpr1 = [
        Bits(
            bits=range(3 * ch, 3 * ch + 3),
            name=f"SMP{ch}",
            descr=f"Channel {ch} sampling time selection",
            descr_vals=bits_smpr_values,
        )
        for ch in range(0, 10)
    ]
    self.append(
        MmapReg(
            name=f"{adc}_SMPR1",
            addr=(base + 0x14),
            descr="ADC1 sample time register 1",
            bits=bits_smpr1,
        )
    )
    bits_smpr2 = [
        Bits(
            bits=range(3 * (ch - 10), 3 * (ch - 10) + 3),
            name=f"SMP{ch}",
            descr=f"Channel {ch} sampling time selection",
            descr_vals=bits_smpr_values,
        )
        for ch in range(10, 20)
    ]
    self.append(
        MmapReg(
            name=f"{adc}_SMPR2",
            addr=(base + 0x18),
            descr="ADC1 sample time register 2",
            bits=bits_smpr2,
        )
    )
    # ----------------------------------------------------------------------------------------------
    self.append(
        MmapReg(
            name=f"{adc}_PCSEL",
            addr=(base + 0x1C),
            descr="ADC channel preselection register",
            bits=[
                Bits(bits=i, name=f"PCSEL{i}", descr=f"Channel VINP[{i}]) pre selection")
                for i in range(0, 20)
            ],
        )
    )
    # ----------------------------------------------------------------------------------------------
    self.append(
        MmapReg(
            name=f"{adc}_SQR1",
            addr=(base + 0x30),
            descr="ADC1 regular sequence register 1",
            bits=[
                Bits(
                    bits=range(0, 4),
                    name="L",
                    descr="Regular channel sequence length",
                    descr_vals={val: f"{(val + 1)} conversions" for val in range(0, 16)},
                ),
                Bits(bits=range(6, 11), name="SQ1", descr="1st conversion in regular sequence"),
                Bits(bits=range(12, 17), name="SQ2", descr="2nd conversion in regular sequence"),
                Bits(bits=range(18, 23), name="SQ3", descr="3rd conversion in regular sequence"),
                Bits(bits=range(24, 29), name="SQ4", descr="4th conversion in regular sequence"),
            ],
        )
    )
    self.append(
        MmapReg(
            name=f"{adc}_SQR2",
            addr=(base + 0x34),
            descr="ADC1 regular sequence register 2",
            bits=[
                Bits(bits=range(0, 4 + 1), name="SQ5", descr="5th conversion in regular sequence"),
                Bits(bits=range(6, 10 + 1), name="SQ6", descr="6th conversion in regular sequence"),
                Bits(
                    bits=range(12, 16 + 1), name="SQ7", descr="7th conversion in regular sequence"
                ),
                Bits(
                    bits=range(18, 22 + 1), name="SQ8", descr="8th conversion in regular sequence"
                ),
                Bits(
                    bits=range(24, 28 + 1), name="SQ9", descr="9th conversion in regular sequence"
                ),
            ],
        )
    )
    self.append(
        MmapReg(
            name=f"{adc}_SQR3",
            addr=(base + 0x38),
            descr="ADC1 regular sequence register 3",
            bits=[
                Bits(
                    bits=range(0, 4 + 1), name="SQ10", descr="10th conversion in regular sequence"
                ),
                Bits(
                    bits=range(6, 10 + 1), name="SQ11", descr="11th conversion in regular sequence"
                ),
                Bits(
                    bits=range(12, 16 + 1), name="SQ12", descr="12th conversion in regular sequence"
                ),
                Bits(
                    bits=range(18, 22 + 1), name="SQ13", descr="13th conversion in regular sequence"
                ),
                Bits(
                    bits=range(24, 28 + 1), name="SQ14", descr="14th conversion in regular sequence"
                ),
            ],
        )
    )
    self.append(
        MmapReg(
            name=f"{adc}_SQR4",
            addr=(base + 0x3C),
            descr="ADC1 regular sequence register 4",
            bits=[
                Bits(
                    bits=range(0, 4 + 1), name="SQ15", descr="15th conversion in regular sequence"
                ),
                Bits(
                    bits=range(6, 10 + 1), name="SQ16", descr="16th conversion in regular sequence"
                ),
            ],
        )
    )
    # ----------------------------------------------------------------------------------------------


def _init_common(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"
    # These registers define the control and status registers common to master and slave ADCs
    adc12_common_base = ADC12_BASE + 0x300
    adc3_common_base = ADC3_BASE + 0x300
    self.append(
        MmapReg(
            name="ADC12_CSR", addr=(adc12_common_base + 0x00), descr="ADC 12 common status register"
        )
    )
    self.append(
        MmapReg(
            name="ADC3_CSR", addr=(adc3_common_base + 0x00), descr="ADC 3 common status register"
        )
    )

    ccr_bits = [
        # Bit 24 VBATEN: VBAT enable
        Bits(bits=23, name="TSEN", descr="Temperature sensor voltage enable"),
        # Bit 22 VREFEN: VREFINT enable
        Bits(
            bits=range(18, 22),
            name="PRESC",
            descr="ADC prescaler",
            descr_vals={
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
                0b1011: "input ADC clock divided by 256",
            },
        ),
        Bits(
            bits=range(16, 18),
            name="CKMODE",
            descr="ADC clock mode",
            descr_vals={
                0b00: "Asynchronous clock mode, generated at product level.",
                0b01: "Synchronous clock mode, adc_sclk/1. Note additional /2 for rev.V.",
                0b10: "Synchronous clock mode, adc_sclk/2. Note additional /2 for rev.V.",
                0b11: "Synchronous clock mode, adc_sclk/4. Note additional /2 for rev.V.",
            },
        ),
        # Bits 15:14 DAMDF[1:0]: Dual ADC Mode Data Format
        # Bits 11:8 DELAY[3:0]: Delay between 2 sampling phases
        # Bits 4:0 DUAL[4:0]: Dual ADC mode selection
    ]
    self.append(
        MmapReg(
            name="ADC12_CCR",
            addr=(adc12_common_base + 0x08),
            descr="ADC12 common control register",
            bits=ccr_bits,
        )
    )
    self.append(
        MmapReg(
            name="ADC3_CCR",
            addr=(adc3_common_base + 0x08),
            descr="ADC3 common control register",
            bits=ccr_bits,
        )
    )

    self.append(
        MmapReg(
            name="ADC12_CDR",
            addr=(adc12_common_base + 0x0C),
            descr="ADC 12 common regular data register for dual mode",
        )
    )
    self.append(
        MmapReg(
            name="ADC3_CDR",
            addr=(adc3_common_base + 0x0C),
            descr="ADC 3 common regular data register for dual mode",
        )
    )

    self.append(
        MmapReg(
            name="ADC12_CDR2",
            addr=(adc12_common_base + 0x10),
            descr="ADC 12 common egular data register for 32-bit dual mode",
        )
    )
    self.append(
        MmapReg(
            name="ADC3_CDR2",
            addr=(adc3_common_base + 0x10),
            descr="ADC 3 common egular data register for 32-bit dual mode",
        )
    )
