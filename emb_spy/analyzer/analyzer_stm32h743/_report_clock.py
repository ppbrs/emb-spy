"""Part of AnalyzerSTM32H743 class."""
from emb_spy import ReaderStaticResult


def report_clock(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    """Add "Clock" chapter to the report."""
    # Circular import error does not allow importin AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    md_file.new_header(level=1, title="Clock")

    hsi_rdy = bits_data["RCC_CR.HSIRDY"].val
    hsi_on = bits_data["RCC_CR.HSION"].val
    if hsi_on and hsi_rdy:
        hsi_div = {0b00: 1, 0b01: 2, 0b10: 4, 0b11: 8, }[bits_data["RCC_CR.HSIDIV"].val]
        self.state.hsi_freq = 64e6 / hsi_div
        md_file.new_line(
            f"* HSI is ON and ready, 64Mhz / {hsi_div} = {self.state.hsi_freq / 1e6} MHz.")
    else:
        self.state.hsi_freq = 0
        md_file.new_line("* HSI is OFF or not ready")

    hse_rdy = bits_data["RCC_CR.HSERDY"].val
    hse_on = bits_data["RCC_CR.HSEON"].val
    if hse_on and hse_rdy:
        hse_cs_on = bits_data["RCC_CR.HSECSSON"].val
        hse_bypass = bits_data["RCC_CR.HSEBYP"].val
        if hse_bypass:
            if not isinstance(hse_freq := self.board_cfg.external_freq, int | float):
                raise ValueError("Valid `external_freq` is required.")
            md_file.new_line(f"* HSE is ON and ready, external clock source, {hse_freq / 1e6}MHz.")
        else:
            if not isinstance(hse_freq := self.board_cfg.resonator_freq, int | float):
                raise ValueError("Valid `resonator_freq` is required.")
            md_file.new_line(
                f"* HSE is ON and ready, crystal/ceramic resonator, {hse_freq / 1e6} MHz.")
        self.state.hse_freq = hse_freq
        if hse_cs_on:
            md_file.new_line(
                "\t* Clock Security System (CSS) is " + ("ON" if hse_cs_on else "OFF") + " on HSE.")
    else:
        md_file.new_line("* HSE is OFF or not ready")

    if (pll_src := bits_data["RCC_PLLCKSELR.PLLSRC"].val) == 0:
        # HSI is sent to PLLs.
        assert self.state.hsi_freq is not None
        ref123_before_divm = self.state.hsi_freq
    elif pll_src == 1:
        # CSI is sent to PLLs.
        raise NotImplementedError
    elif pll_src == 2:
        # HSE is sent to PLLs.
        assert self.state.hse_freq is not None
        ref123_before_divm = self.state.hse_freq
    elif pll_src == 3:
        # No clock is sent to PLLs.
        raise NotImplementedError
    self.state.ref1_freq = ref123_before_divm / bits_data["RCC_PLLCKSELR.DIVM1"].val
    self.state.ref2_freq = ref123_before_divm / bits_data["RCC_PLLCKSELR.DIVM2"].val
    self.state.ref3_freq = ref123_before_divm / bits_data["RCC_PLLCKSELR.DIVM3"].val

    for i in [1, 2, 3]:  # i is PLL index
        pll_on = bits_data[f"RCC_CR.PLL{i}ON"].val
        pll_rdy = bits_data[f"RCC_CR.PLL{i}RDY"].val
        pll_frac_en = bits_data[f"RCC_PLLCFGR.PLL{i}FRACEN"].val
        if pll_on and pll_rdy:
            md_file.new_line(f"* PLL{i} is ON and ready.")
            if not pll_frac_en:
                vco_sel = bits_data[f"RCC_PLLCFGR.PLL{i}VCOSEL"].val

                div_n = bits_data[f"RCC_PLL{i}DIVR.DIVN{i}"].val + 1
                assert 4 <= div_n <= 514, f"PLL{i} invalid divn"
                ref_freq = {1: self.state.ref1_freq, 2: self.state.ref2_freq, 3: self.state.ref3_freq, }[i]
                vco_freq = ref_freq * div_n
                setattr(self.state, f"pll{i}_vco_freq", vco_freq)
                md_file.new_line(f"\t* VCO{i} = {ref_freq} * {div_n} = {vco_freq / 1e6} MHz.")
                if vco_sel:
                    md_file.new_line(f"\t* VCO{i} is set to medium range: 150 to 420 MHz.")
                else:
                    md_file.new_line(f"\t* VCO{i} is set to wide range: 192 to 960 MHz.")
                div_p_en = bits_data[f"RCC_PLLCFGR.DIVP{i}EN"].val
                if div_p_en:
                    div_p = bits_data[f"RCC_PLL{i}DIVR.DIVP{i}"].val + 1
                    p_freq = vco_freq / div_p
                    setattr(self.state, f"pll{i}_p_freq", p_freq)
                    md_file.new_line(f"\t* PLL{i}-P is enabled, {p_freq / 1e6} MHz.")
                div_q_en = bits_data[f"RCC_PLLCFGR.DIVQ{i}EN"].val
                if div_q_en:
                    div_q = bits_data[f"RCC_PLL{i}DIVR.DIVQ{i}"].val + 1
                    q_freq = vco_freq / div_q
                    setattr(self.state, f"pll{i}_q_freq", q_freq)
                    md_file.new_line(f"\t* PLL{i}-Q is enabled, {q_freq / 1e6} MHz.")
                div_r_en = bits_data[f"RCC_PLLCFGR.DIVR{i}EN"].val
                if div_r_en:
                    div_r = bits_data[f"RCC_PLL{i}DIVR.DIVR{i}"].val + 1
                    r_freq = vco_freq / div_r
                    setattr(self.state, f"pll{i}_r_freq", r_freq)
                    md_file.new_line(f"\t* PLL{i}-R is enabled, {r_freq / 1e6} MHz.")
            else:
                raise NotImplementedError
        elif pll_on:
            md_file.new_line(f"* PLL{i} is ON but not ready.")
        elif not pll_on:
            md_file.new_line(f"* PLL{i} is OFF.")

    #
    # System clock
    #
    assert bits_data["RCC_CFGR.SWS"].val == bits_data["RCC_CFGR.SW"].val
    sws = bits_data["RCC_CFGR.SWS"].val
    if sws == 0b000:
        self.state.sys_freq = self.state.hsi_freq
        md_file.new_line(f"* System clock is from HSI: {self.state.sys_freq / 1e6} MHz.")
    elif sws == 0b010:
        self.state.sys_freq = self.state.hse_freq
        md_file.new_line(f"* System clock is from HSE: {self.state.sys_freq / 1e6} MHz.")
    elif sws == 0b011:
        self.state.sys_freq = self.state.pll1_p_freq
        md_file.new_line(f"* System clock is from PLL1-P: {self.state.sys_freq / 1e6} MHz.")
    else:
        raise NotImplementedError

    self.state.systick_freq = self.state.sys_freq / 8
    md_file.new_line(f"* SysTick: {self.state.systick_freq / 1e6} MHz.")

    #
    # Bus clock
    #
    assert bits_data["RCC_D1CFGR.D1CPRE"].val == 0
    self.state.cpu_freq = self.state.sys_freq
    md_file.new_line(f"* CPU clock (D1) == system clock: {self.state.cpu_freq / 1e6} MHz.")

    axi_div = {
        0b0000: 1,
        0b1000: 2,
        0b1001: 4,
        0b1010: 8,
        0b1011: 16,
        0b1100: 64,
        0b1101: 128,
        0b1110: 256,
        0b1111: 512, }[bits_data["RCC_D1CFGR.HPRE"].val]
    self.state.axi_freq = self.state.cpu_freq / axi_div
    md_file.new_line(f"* AXI clock (D1): {self.state.axi_freq / 1e6} MHz.")
    self.state.ahb1_freq = self.state.axi_freq
    md_file.new_line(f"* AHB1 clock (D2): {self.state.ahb1_freq / 1e6} MHz.")
    self.state.ahb2_freq = self.state.axi_freq
    md_file.new_line(f"* AHB2 clock (D2): {self.state.ahb2_freq / 1e6} MHz.")
    self.state.ahb3_freq = self.state.axi_freq
    md_file.new_line(f"* AHB3 clock (D1): {self.state.ahb3_freq / 1e6} MHz.")
    self.state.ahb4_freq = self.state.axi_freq
    md_file.new_line(f"* AHB4 clock (D3): {self.state.ahb4_freq / 1e6} MHz.")

    #
    # Peripheral clock
    #
    apb1_div = {
        0b000: 1,
        0b100: 2,
        0b101: 4,
        0b110: 8,
        0b111: 16, }[bits_data["RCC_D2CFGR.D2PPRE1"].val]
    self.state.apb1_freq = self.state.axi_freq / apb1_div
    md_file.new_line(f"* APB1 clock (D2): {self.state.apb1_freq / 1e6} MHz.")
    apb2_div = {
        0b000: 1,
        0b100: 2,
        0b101: 4,
        0b110: 8,
        0b111: 16, }[bits_data["RCC_D2CFGR.D2PPRE2"].val]
    self.state.apb2_freq = self.state.axi_freq / apb2_div
    md_file.new_line(f"* APB2 clock (D2): {self.state.apb2_freq / 1e6} MHz.")
    apb3_div = {
        0b000: 1,
        0b100: 2,
        0b101: 4,
        0b110: 8,
        0b111: 16, }[bits_data["RCC_D1CFGR.D1PPRE"].val]
    self.state.apb3_freq = self.state.axi_freq / apb3_div
    md_file.new_line(f"* APB3 clock (D1): {self.state.apb3_freq / 1e6} MHz.")
    apb4_div = {
        0b000: 1,
        0b100: 2,
        0b101: 4,
        0b110: 8,
        0b111: 16, }[bits_data["RCC_D3CFGR.D3PPRE"].val]
    self.state.apb4_freq = self.state.axi_freq / apb4_div
    md_file.new_line(f"* APB4 clock (D3): {self.state.apb4_freq / 1e6} MHz.")

    #
    # Peripheral timers clock
    #
    timpre = bits_data["RCC_CFGR.TIMPRE"].val
    d2ppre1 = bits_data["RCC_D2CFGR.D2PPRE1"].val
    if d2ppre1 == 0:
        timx_apb1_factor = 1
    elif timpre == 0:
        timx_apb1_factor = 2
    elif timpre == 1:
        if d2ppre1 == 0b100:
            timx_apb1_factor = 2
        else:
            timx_apb1_factor = 4
    self.state.timx_freq = self.state.apb1_freq * timx_apb1_factor
    md_file.new_line(
        f"* TIMx clock (D2, advanced-control timers, TIM1/TIM8): {self.state.timx_freq / 1e6} MHz.")

    d2ppre2 = bits_data["RCC_D2CFGR.D2PPRE2"].val
    if d2ppre2 == 0:
        timy_apb1_factor = 1
    elif timpre == 0:
        timy_apb1_factor = 2
    elif timpre == 1:
        if d2ppre2 == 0b100:
            timy_apb1_factor = 2
        else:
            timy_apb1_factor = 4
    self.state.timy_freq = self.state.apb1_freq * timy_apb1_factor
    md_file.new_line(
        "* TIMy clock (D2, general-purpose timers, other than TIM1/TIM8): "
        f"{self.state.timy_freq / 1e6} MHz.")

    hrtimsel = bits_data["RCC_CFGR.HRTIMSEL"].val
    if hrtimsel == 0:
        self.state.hrtim_freq = self.state.timy_freq
    else:
        self.state.hrtim_freq = self.state.cpu_freq
    md_file.new_line(f"* HRTIM clock (D2): {self.state.hrtim_freq / 1e6} MHz.")

    _report_clock_mco(self, bits_data, md_file)

    #
    # PER_CK
    #
    percksel = bits_data["RCC_D1CCIPR.CKPERSEL"].val
    match percksel:
        case 0:
            # 0: hsi_ker_ck clock selected as per_ck clock (default after reset)
            self.state.per_freq = self.state.hsi_freq
        case 1:
            # 1: csi_ker_ck clock selected as per_ck clock
            raise NotImplementedError
        case 2:
            # 2: hse_ck clock selected as per_ck clock
            self.state.per_freq = self.state.hse_freq
        case _:
            # 3: reserved, the per_ck clock is disabled
            self.state.per_freq = 0
    md_file.new_line(f"* PER clock: {self.state.per_freq / 1e6} MHz.")

    md_file.new_line("***")


def _report_clock_mco(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"
    mco1_enabled = bits_data["RCC_CFGR.MCO1PRE"].val > 0
    if mco1_enabled:
        mco1_src = bits_data["RCC_CFGR.MCO1"].val
        mco1_div = bits_data["RCC_CFGR.MCO1PRE"].val
        if mco1_src == 0b010:  # hse_ck
            self.state.mco1_freq = self.state.hse_freq / mco1_div
            md_file.new_line(
                "* MCO1 is from HSE: "
                f"{self.state.hse_freq / 1e6} / {mco1_div} = {self.state.mco1_freq / 1e6} MHz.")
        else:
            raise NotImplementedError
    else:
        md_file.new_line("* MCO1 is OFF.")
    mco2_enabled = bits_data["RCC_CFGR.MCO2PRE"].val > 0
    if mco2_enabled:
        raise NotImplementedError
    md_file.new_line("* MCO2 is OFF.")
