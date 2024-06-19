"""Part of AnalyzerSTM32F745 class."""
from emb_spy import ReaderStaticResult


def _report_clock(
    self,  # : AnalyzerSTM32F745
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    # Circular import error does not allow importin AnalyzerSTM32F745 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32F745"

    md_file.new_header(level=1, title="Clock")

    hsi_rdy = bits_data["RCC_CR.HSIRDY"].val
    hsi_on = bits_data["RCC_CR.HSION"].val
    if hsi_on and hsi_rdy:
        raise NotImplementedError
        # hsi_div = {0b00: 1, 0b01: 2, 0b10: 4, 0b11: 8, }[bits_data["RCC_CR.HSIDIV"].val]
        # self.state.hsi_freq = 64e6 / hsi_div
        # md_file.new_line(
        #   f"* HSI is ON and ready, 64Mhz / {hsi_div} = {self.state.hsi_freq / 1e6} MHz.")
    md_file.new_line("* HSI is OFF or not ready")

    hse_rdy = bits_data["RCC_CR.HSERDY"].val
    hse_on = bits_data["RCC_CR.HSEON"].val
    if hse_on and hse_rdy:
        hse_cs_on = bits_data["RCC_CR.CSSON"].val
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

    pll_on = bits_data["RCC_CR.PLLON"].val
    pll_rdy = bits_data["RCC_CR.PLLRDY"].val
    if pll_on and pll_rdy:
        md_file.new_line("* Main PLL is ON and ready")
        pll_src = bits_data["RCC_PLLCFGR.PLLSRC"].val
        if pll_src == 0:
            raise NotImplementedError
            # 0: HSI clock selected as PLL and PLLI2S clock entry
        else:
            # 1: HSE oscillator clock selected as PLL and PLLI2S clock entry
            self.state.pll_in_freq = self.state.hse_freq
            md_file.new_line(f"\t* PLL input is HSE: {self.state.pll_in_freq / 1e6} MHz")
            m_div = bits_data["RCC_PLLCFGR.PLLM"].val
            n_fact = bits_data["RCC_PLLCFGR.PLLN"].val
            q_div = bits_data["RCC_PLLCFGR.PLLQ"].val
            p_div = {
                0b00: 2,
                0b01: 4,
                0b10: 6,
                0b11: 8,
            }[bits_data["RCC_PLLCFGR.PLLP"].val]
            assert m_div >= 2 and n_fact >= 2 and q_div >= 2
            self.state.pll_vco_freq = self.state.pll_in_freq / m_div * n_fact
            md_file.new_line(f"\t* VCO frequency = {self.state.pll_vco_freq / 1e6} MHz")
            self.state.pll_p_freq = self.state.pll_vco_freq / p_div
            self.state.pll_q_freq = self.state.pll_vco_freq / q_div
            md_file.new_line(f"\t* PLL P output frequency (system clock) = {self.state.pll_p_freq / 1e6} MHz")
            md_file.new_line(f"\t* PLL P output frequency (USB OTG FS, SDMMC, RND) = {self.state.pll_q_freq / 1e6} MHz")
    else:
        md_file.new_line("* Main PLL is OFF or not ready")

    sws = bits_data["RCC_CFGR.SWS"].val
    if sws == 0:
        self.state.sys_freq = self.state.hsi_freq
        md_file.new_line(f"* System clock = HSI = {self.state.sys_freq / 1e6} MHz")
    elif sws == 1:
        self.state.sys_freq = self.state.hse_freq
        md_file.new_line(f"* System clock = HSE = {self.state.sys_freq / 1e6} MHz")
    elif sws == 2:
        self.state.sys_freq = self.state.pll_p_freq
        md_file.new_line(f"* System clock = PLL.P = {self.state.sys_freq / 1e6} MHz")
    else:
        raise ValueError

    # MCO1
    mco1_src = bits_data["RCC_CFGR.MCO1"].val
    mco1_pre = bits_data["RCC_CFGR.MCO1PRE"].val
    mco1_div = (mco1_pre - 2) if mco1_pre >= 4 else 1
    if mco1_src == 0:
        if self.state.hsi_freq is not None:
            self.state.mco1_freq = self.state.hsi_freq / mco1_div
            md_file.new_line(f"* MCO = HSI / {mco1_div} = {self.state.mco1_freq / 1e6} MHz")
    elif mco1_src == 1:
        # LSE oscillator
        self.state.mco1_freq = self.state.lse_freq / mco1_div
        md_file.new_line(f"* MCO = LSE / {mco1_div} = {self.state.mco1_freq / 1e6} MHz")
    elif mco1_src == 2:
        self.state.mco1_freq = self.state.hse_freq / mco1_div
        md_file.new_line(f"* MCO = HSE / {mco1_div} = {self.state.mco1_freq / 1e6} MHz")
    elif mco1_src == 3:
        self.state.mco1_freq = self.state.pll_p_freq / mco1_div
        md_file.new_line(f"* MCO = PLL.P / {mco1_div} = {self.state.mco1_freq / 1e6} MHz")

    # MCO2
    mco2_src = bits_data["RCC_CFGR.MCO2"].val
    # 00: System clock (SYSCLK) selected
    # 01: PLLI2S clock selected
    # 10: HSE oscillator clock selected
    # 11: PLL clock selected
    mco2_div = bits_data["RCC_CFGR.MCO2PRE"].val

    # mco1_freq: Frequency = None
    # mco2_freq: Frequency = None

    md_file.new_line("***")
