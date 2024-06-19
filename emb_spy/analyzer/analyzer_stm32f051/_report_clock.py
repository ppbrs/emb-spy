"""Part of AnalyzerSTM32F051."""
from emb_spy import ReaderStaticResult


def report_clock(
    self,
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    """Add a Clock chapter to the report."""
    assert self.__class__.__name__ == "AnalyzerSTM32F051"
    # This is equivalent to assert isinstance(self, AnalyzerSTM32F051).
    # I do this to avoid the circular import error.

    md_file.new_header(level=1, title="Clock")

    hsi_freq = 8e6
    hsion, hsirdy = bits_data["RCC_CR.HSION"].val, bits_data["RCC_CR.HSIRDY"].val
    if hsirdy:
        md_file.new_line(f"HSI is running and ready, {hsi_freq / 1e6}MHz.")
    elif hsion:
        md_file.new_line("HSI is running but not ready.")
    else:
        md_file.new_line("HSI is not ready.")

    hseon, hserdy = bits_data["RCC_CR.HSEON"].val, bits_data["RCC_CR.HSERDY"].val
    if hserdy:
        md_file.new_line("HSE is running and ready.")
    elif hseon:
        md_file.new_line("HSE is running but not ready.")
    else:
        md_file.new_line("HSE is not ready.")

    pll_src = bits_data["RCC_CFGR.PLLSRC"].val
    if pll_src == 0:  # HSI/2 selected as PLL input clock
        pll_in_freq = hsi_freq / 2
        md_file.new_line(f"PLL input frequency = {pll_in_freq / 1e6}MHz.")

        pllon, pllrdy = bits_data["RCC_CR.PLLON"].val, bits_data["RCC_CR.PLLRDY"].val
        pll_mul = bits_data["RCC_CFGR.PLLMUL"].val
        if pllon and pllrdy:
            md_file.new_line("PLL is on and ready.")
        if pll_mul <= 14:
            pll_out_freq = pll_in_freq * (pll_mul + 2)
        else:
            pll_out_freq = pll_in_freq * 16
        md_file.new_line(f"PLL output frequency = {pll_out_freq / 1e6}MHz.")
    else:
        raise NotImplementedError

    sys_clk_src = bits_data["RCC_CFGR.SW"].val
    if sys_clk_src == 0:  # 00: HSI selected as system clock
        md_file.new_line("System clock (SYSCLK) is HSI.")
    elif sys_clk_src == 1:  # 01: HSE selected as system clock
        md_file.new_line("System clock (SYSCLK) is HSE.")
    elif sys_clk_src == 2:  # 10: PLL selected as system clock
        md_file.new_line(f"System clock (SYSCLK) is PLL, {pll_out_freq / 1e6}MHz")
        self.state.sys_freq = pll_out_freq
    elif sys_clk_src == 3:  # 11: HSI48 selected as system clock
        md_file.new_line("System clock (SYSCLK) is HSI48.")

    hclk_pre = bits_data["RCC_CFGR.HPRE"].val
    if hclk_pre < 8:
        hclk_freq = self.state.sys_freq
        
    else:
        hclk_div = {8: 2, 9: 4, 10: 8, 11: 16, 12: 64, 13: 128, 14: 256, 15: 512}[hclk_pre]
        hclk_freq = self.state.sys_freqb / hclk_div
    md_file.new_line(f"Internal AHB clock (HCLK) is {hclk_freq / 1e6}MHz")

    pclk_pre = bits_data["RCC_CFGR.PPRE"].val
    if pclk_pre < 4:
        self.state.pclk_freq = hclk_freq
    else:
        self.state.pclk_freq = hclk_freq / {4: 2, 9: 4, 10: 8, 11: 16}[pclk_pre]
    md_file.new_line(f"Internal APB clock (PCLK) is {self.state.pclk_freq / 1e6}MHz")

    md_file.new_line("***")
