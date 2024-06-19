"""Part of AnalyzerSTM32H743 class."""

from emb_spy import ReaderStaticResult


def report_adc(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file,
) -> None:
    """Add "ADC" chapter to the report."""
    # Circular import error does not allow importin AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    md_file.new_header(level=1, title="ADC")

    # Analog switches:
    md_file.new_line("* Analog switches")
    pa0so = bits_data["SYSCFG_PMCR.PA0SO"].val
    pa1so = bits_data["SYSCFG_PMCR.PA1SO"].val
    pc2so = bits_data["SYSCFG_PMCR.PC2SO"].val
    pc3so = bits_data["SYSCFG_PMCR.PC3SO"].val
    boost_ena = bits_data["SYSCFG_PMCR.BOOSTE"].val

    switch = {
        True: " --x-- ",  # open
        False: " <---> ",
    }  # closed
    md_file.new_line("\t* PA0 (ADC1_INP16)" + switch[pa0so] + "PA0_C (ADC12_INN1, ADC12_INP0)")
    md_file.new_line("\t* PA1 (ADC1_INN16, ADC1_INP17)" + switch[pa1so] + "PA1_C (ADC12_INP1)")
    md_file.new_line(
        "\t* PC2 (ADC123_INN11, ADC123_INP12)" + switch[pc2so] + "PC2_C (ADC3_INN1, ADC3_INP0)"
    )
    md_file.new_line("\t* PC3 (ADC12_INN12, ADC12_INP13)" + switch[pc3so] + "PC3_C (ADC3_INP1)")
    if boost_ena:
        # boost_vdd = bits_data["SYSCFG_PMCR.BOOSTVDDSEL"].val
        md_file.new_line("\t* Supply voltage booster enabled.")
    else:
        md_file.new_line("\t* Supply voltage booster disabled.")

    ker_clk_src = bits_data["RCC_D3CCIPR.ADCSEL"].val
    if ker_clk_src == 0:
        # pll2_p_ck clock selected as kernel peripheral clock
        if self.state.pll2_p_freq is not None:
            self.state.adc_ker_input_freq = self.state.pll2_p_freq
            md_file.new_line(
                "* ADC kernel input clock is from PLL2.P: "
                f"{self.state.adc_ker_input_freq / 1e6} MHz."
            )
        else:
            md_file.new_line("* ADC kernel clock is from PLL2.P which is OFF.")
            return
    elif ker_clk_src == 1:
        # pll3_r_ck clock selected as kernel peripheral clock
        raise NotImplementedError
    elif ker_clk_src == 2:
        # per_ck clock selected as kernel peripheral clock
        self.state.adc_ker_input_freq = self.state.per_freq
        md_file.new_line(
            "* ADC kernel input clock is from PER_CK: "
            f"{self.state.adc_ker_input_freq / 1e6} MHz."
        )
    else:
        md_file.new_line("* ADC kernel clock is disabled.")
        return

    md_file.new_line("***")

    _report_adc_common(self, bits_data=bits_data, md_file=md_file, idx=12)
    _report_adc_common(self, bits_data=bits_data, md_file=md_file, idx=3)

    _report_adc_individual(self, bits_data=bits_data, md_file=md_file, idx=1)
    _report_adc_individual(self, bits_data=bits_data, md_file=md_file, idx=2)
    _report_adc_individual(self, bits_data=bits_data, md_file=md_file, idx=3)


def _report_adc_common(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file,
    idx: int,  # 12, or 3.
) -> None:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"
    assert idx in (12, 3)
    adcc = f"ADC{idx}"
    is_rev_v = self.state.is_rev_v
    md_file.new_header(level=2, title=f"{adcc} (common)")

    adc_ker_freq_name = "adc12_ker_freq" if idx == 12 else "adc3_ker_freq"

    ckmode = bits_data[f"{adcc}_CCR.CKMODE"].val
    if ckmode == 0:
        ker_in_div = {
            0b0000: 1,
            0b0001: 2,
            0b0010: 4,
            0b0011: 6,
            0b0100: 8,
            0b0101: 10,
            0b0110: 12,
            0b0111: 16,
            0b1000: 32,
            0b1001: 64,
            0b1010: 128,
            0b1011: 256,
        }[bits_data[f"{adcc}_CCR.PRESC"].val]
        md_file.new_line(
            f"Asynchronous clock mode, divided by {ker_in_div} in prescaler, "
            f"then by {2 if is_rev_v else 1}."
        )

        setattr(
            self.state,
            adc_ker_freq_name,
            self.state.adc_ker_input_freq / ker_in_div / (2 if is_rev_v else 1),
        )

    else:
        md_file.new_line("Synchronous clock mode.")
        hclk_div = {
            0b01: 1,
            0b10: 2,
            0b11: 4,
        }[ckmode]
        if idx == 12:
            setattr(self.state, adc_ker_freq_name, self.state.ahb1_freq / hclk_div)
            md_file.new_line(
                f"ADC kernel clock is from AHB1: {self.state.ahb1_freq / 1e6} MHz / {hclk_div}."
            )
        else:
            setattr(self.state, adc_ker_freq_name, self.state.ahb4_freq / hclk_div)
            md_file.new_line(
                f"ADC kernel clock is from AHB4: {self.state.ahb1_freq / 1e6} MHz / {hclk_div}."
            )

    md_file.new_line(f"ADC kernel clock is : {getattr(self.state, adc_ker_freq_name) / 1e6} MHz.")

    md_file.new_line("***")


def _report_adc_individual(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file,
    idx: int,  # 1, 2, or 3.
) -> None:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"
    assert idx in (1, 2, 3)
    adci = f"ADC{idx}"
    enabled = bits_data[adci + "_CR.ADEN"].val
    if not enabled:
        md_file.new_header(level=2, title=f"{adci} (individual) - disabled")
        return

    is_rev_v = self.state.is_rev_v
    adc_ker_freq = self.state.adc12_ker_freq if idx in (1, 2) else self.state.adc3_ker_freq

    md_file.new_header(level=2, title=f"{adci} (individual)")

    def report_boost():
        boost = bits_data[f"{adci}_CR.BOOST"].val
        if is_rev_v:
            boost_descr = {
                0b00: "can be used when ADC clock ≤ 6.25 MHz",
                0b01: "can be used when 6.25 MHz < ADC clock frequency ≤ 12.5 MHz",
                0b10: "can be used when 12.5 MHz < ADC clock ≤ 25.0 MHz",
                0b11: "can be used when 25.0 MHz < ADC clock ≤ 50.0 MHz",
            }[boost]
        else:
            boost_descr = {
                0: "used when ADC clock < 20 MHz to save power at lower clock frequency",
                1: "used when ADC clock > 20 MHz",
            }[boost]
        md_file.new_line(f"* BOOST={boost} ({boost_descr}).")

    report_boost()

    def report_mode():
        disc_mode = bits_data[f"{adci}_CFGR.DISCEN"].val
        cont_mode = bits_data[f"{adci}_CFGR.CONT"].val
        if disc_mode:
            raise NotImplementedError
        if cont_mode:
            md_file.new_line("* Continuous conversion mode.")
        else:
            md_file.new_line("* Single conversion mode.")

    report_mode()

    def get_resolution() -> int:
        if is_rev_v:
            return {
                0b000: 16,
                0b101: 14,
                0b001: 14,
                0b110: 12,
                0b010: 12,
                0b011: 10,
                0b111: 8,
            }[bits_data[f"{adci}_CFGR.RES"].val]
        return {
            0b000: 16,
            0b001: 14,
            0b010: 12,
            0b011: 10,
            0b100: 8,
        }[bits_data[f"{adci}_CFGR.RES"].val]

    def report_resolution():
        resolution = get_resolution()
        md_file.new_line(f"* Resolution is {resolution} bits.")

    report_resolution()

    def report_data_mode():
        if (dmngt := bits_data[f"{adci}_CFGR.DMNGT"].val) == 0:
            md_file.new_line("* Data mode: DR only.")
        elif dmngt == 1:
            md_file.new_line("* Data mode: DMA One Shot Mode .")
        elif dmngt == 2:
            md_file.new_line("* Data mode: DFSDM.")
        elif dmngt == 3:
            md_file.new_line("* Data mode: DMA Circular Mode.")

    report_data_mode()

    def get_oversampling_ratio() -> int:
        """Find oversampling ratio."""
        os_enabled = bits_data[f"{adci}_CFGR2.ROVSE"].val
        os_ratio = bits_data[f"{adci}_CFGR2.OSVR"].val + 1
        return os_ratio if os_enabled else 1

    def report_oversampling():
        os_enabled = bits_data[f"{adci}_CFGR2.ROVSE"].val
        if os_enabled:
            ratio = bits_data[f"{adci}_CFGR2.OSVR"].val + 1
            lshift = bits_data[f"{adci}_CFGR2.LSHIFT"].val
            rshift = bits_data[f"{adci}_CFGR2.OVSS"].val
            md_file.new_line(
                f"* Oversampling: ON, ratio = {ratio}x, "
                f"left shift = {lshift}, right shift = {rshift}."
            )
        else:
            md_file.new_line("* Oversampling: OFF.")

    report_oversampling()

    if bits_data[f"{adci}_CFGR2.LSHIFT"].val:
        raise NotImplementedError

    # conv_cycles maps channel number to the number of cycles one conversion takes.
    conv_cycles: dict[int, float] = {}
    smp_cycles: dict[int, float] = {}
    sar_cycles: dict[int, float] = {}

    def report_enabled_channels():
        # Construct a table of enabled channels.
        legend, table = ["Channel", "Type", "Sampling time", "SAR time", "Conversion time"], []
        for ch in range(0, 20):
            if not bits_data[f"{adci}_PCSEL.PCSEL{ch}"].val:
                continue
            table.append(get_adc_channel_descr(adc_idx=idx, ch_idx=ch))

            # Type
            if (idx, ch) in [(1, 0), (2, 0), (1, 1), (2, 1), (3, 0), (3, 1)]:
                table.append("direct")
            elif ch <= 5:
                table.append("fast")
            else:
                table.append("slow")

            # Sampling time
            smp = bits_data[f"{adci}_SMPR1.SMP{ch}" if ch < 10 else f"{adci}_SMPR2.SMP{ch}"].val
            smp_cycles[ch] = {
                0b000: 1.5,
                0b001: 2.5,
                0b010: 8.5,
                0b011: 16.5,
                0b100: 32.5,
                0b101: 64.5,
                0b110: 387.5,
                0b111: 810.5,
            }[smp]
            smp_ns = smp_cycles[ch] / adc_ker_freq * 1e9
            table.append(f"{smp} = {smp_cycles[ch]} cycles = {round(smp_ns)} ns")

            # SAR time
            sar_cycles[ch] = {
                16: 8.5,
                14: 7.5,
                12: 6.5,
                10: 5.5,
                8: 4.5,
            }[get_resolution()]
            sar_ns = sar_cycles[ch] / adc_ker_freq * 1e9
            table.append(f"{sar_cycles[ch]} cycles = {round(sar_ns)} ns")

            # Conversion time
            conv_cycles[ch] = smp_cycles[ch] + sar_cycles[ch]
            conv_ns = conv_cycles[ch] / adc_ker_freq * 1e9
            conv_ksps = 1 / conv_ns * 1e6
            table.append(
                f"{conv_cycles[ch]} cycles = {round(conv_ns)} ns = {round(conv_ksps)} kSps"
            )

        md_file.new_line()
        md_file.new_table(
            columns=len(legend),
            rows=(1 + len(table) // len(legend)),
            text_align="left",
            text=(legend + table),
        )

    report_enabled_channels()

    def report_regular_sequence():
        seq_chs = []
        seq_len = bits_data[f"{adci}_SQR1.L"].val + 1
        conv_cycles_total = 0
        smp_cycles_total = 0
        sar_cycles_total = 0
        for seq_idx in range(1, seq_len + 1):
            if seq_idx <= 4:
                reg = f"{adci}_SQR1"
            elif seq_idx <= 9:
                reg = f"{adci}_SQR2"
            elif seq_idx <= 14:
                reg = f"{adci}_SQR3"
            elif seq_idx <= 16:
                reg = f"{adci}_SQR4"
            ch = bits_data[f"{reg}.SQ{seq_idx}"].val
            seq_chs.append(ch)
            conv_cycles_total += conv_cycles.get(ch, 0)
            sar_cycles_total += sar_cycles.get(ch, 0)
            smp_cycles_total += smp_cycles.get(ch, 0)
        md_file.new_line(f"* Regular sequence = {seq_len} conversions (max = 16 conversions): ")
        md_file.new_line(
            "\t* "
            + " ⇨ ".join(get_adc_channel_descr(adc_idx=idx, ch_idx=ch) for ch in seq_chs)
            + "."
        )
        os_ratio = get_oversampling_ratio()
        smp_ns_total = smp_cycles_total * os_ratio / adc_ker_freq * 1e9
        sar_ns_total = sar_cycles_total * os_ratio / adc_ker_freq * 1e9
        conv_ns_total = conv_cycles_total * os_ratio / adc_ker_freq * 1e9
        md_file.new_line(
            f"\t* Conversion: {conv_cycles_total} cycles × {os_ratio} = {round(conv_ns_total)} ns."
        )
        md_file.new_line(
            f"\t\t* Sampling: {smp_cycles_total} cycles × {os_ratio} = {round(smp_ns_total)} ns."
        )
        md_file.new_line(
            f"\t\t* SAR: {sar_cycles_total} cycles × {os_ratio} = {round(sar_ns_total)} ns."
        )

    report_regular_sequence()

    # External trigger (regular channels)
    def report_external_trigger():
        if (ext_enabled := bits_data[f"{adci}_CFGR.EXTEN"].val) == 0:
            md_file.new_line("* Hardware trigger: disabled.")
        else:
            edge_str = {
                0b01: "rising edge",
                0b10: "falling edge",
                0b11: "both rising and falling edges",
            }[ext_enabled]
            event_idx = bits_data[f"{adci}_CFGR.EXTSEL"].val
            assert event_idx < 32
            event_str = [
                "tim1_oc1",
                "tim1_oc2",
                "tim1_oc3",
                "tim2_oc2",
                "tim3_trgo",
                "tim4_oc4",
                "exti11",
                "tim8_trgo",
                "tim8_trgo2",
                "tim1_trgo",
                "tim1_trgo2",
                "tim2_trgo",
                "tim4_trgo",
                "tim6_trgo",
                "tim15_trgo",
                "tim3_oc4",
                "hrtim1_adctrg1",
                "hrtim1_adctrg3",
                "lptim1_out",
                "lptim2_out",
                "lptim3_out",
            ][event_idx]  # adc_ext_trg21..31 are Reserved.
            md_file.new_line(
                f"* Hardware trigger: enabled, {edge_str}, event {event_idx} = {event_str}."
            )

    report_external_trigger()

    def report_status():
        md_file.new_line("* Status:")
        ardy = bits_data[f"{adci}_ISR.ADRDY"].val
        eosmp = bits_data[f"{adci}_ISR.EOSMP"].val
        eoc = bits_data[f"{adci}_ISR.EOC"].val
        eos = bits_data[f"{adci}_ISR.EOS"].val
        ldordy = bits_data[f"{adci}_ISR.LDORDY"].val
        md_file.new_line(f"\t* ARDY: {ardy}")
        md_file.new_line(f"\t* EOSMP: {eosmp}")
        md_file.new_line(f"\t* EOC: {eoc}")
        md_file.new_line(f"\t* EOS: {eos}")
        md_file.new_line(f"\t* LDORDY: {ldordy}")

    report_status()

    md_file.new_line("***")


def get_adc_channel_descr(adc_idx: int, ch_idx: int) -> str:
    """
    Return a string of the form "XX (YYY)".

    PA0 = ADC1_INP16
    PA0_C = ADC12_INN1,ADC12_INP0
    PA1 = ADC1_INN16,ADC1_INP17
    PA1_C = ADC12_INP1
    PA2 = ADC12_INP14
    PA3 = ADC12_INP15
    PA4 = ADC12_INP18
    PA5 = ADC12_INN18,ADC12_INP19
    PA6 = ADC12_INP3
    PA7 = ADC12_INN3,ADC12_INP7

    PC0 = ADC123_INP10
    PC1 = ADC123_INN10, ADC123_INP11
    PC2 = ADC123_INN11,ADC123_INP12
    PC2_C = ADC3_INN1, ADC3_INP0
    PC3 = ADC12_INN12, ADC12_INP13
    PC3_C = ADC3_INP1
    """
    descr = str(ch_idx)
    match (adc_idx, ch_idx):
        case (1, 16):
            descr += " (PA0)"
        case (1, 0) | (2, 0):
            descr += " (PA0_C)"
        case (1, 17):
            descr += " (PA1)"
        case (1, 1) | (2, 1):
            descr += " (PA1_C)"
        case (1, 14) | (2, 14):
            descr += " (PA2)"
        case (1, 15) | (2, 15):
            descr += " (PA3)"
        case (1, 18) | (2, 18):
            descr += " (PA4)"
        case (1, 19) | (2, 19):
            descr += " (PA5)"
        case (1, 3) | (2, 3):
            descr += " (PA6)"
        case (1, 7) | (2, 7):
            descr += " (PA7)"

        case (1, 9) | (2, 9):
            descr += " (PB0)"  # PB0 = ADC12_INN5,ADC12_INP9
        case (1, 5) | (2, 5):
            descr += " (PB1)"  # PB1 = ADC12_INP5

        case (1, 10) | (2, 10) | (3, 10):
            descr += " (PC0)"
        case (1, 11) | (2, 11) | (3, 11):
            descr += " (PC1)"
        case (1, 12) | (2, 12) | (3, 12):
            descr += " (PC2)"
        case (3, 0):
            descr += " (PC2_C)"
        case (1, 13) | (2, 13):
            descr += " (PC3)"
        case (3, 1):
            descr += " (PC3_C)"

        case (1, 2):
            descr += " (PF11)"  # PF11 = ADC1_INP2
        case (2, 2):
            descr += " (PF13)"  # PF13 = ADC2_INP2

        case (2, 16):
            descr += " (DAC1_OUT)"
        case (2, 17):
            descr += " (DAC2_OUT)"

        case (3, 17):
            descr += " (VBAT/4)"
        case (3, 18):
            descr += " (SENSE)"
        case (3, 19):
            descr += " (VREFINT)"
    return descr
