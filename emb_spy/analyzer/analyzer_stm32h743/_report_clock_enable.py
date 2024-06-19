"""Part of AnalyzerSTM32H743 class."""
from emb_spy import ReaderStaticResult
from emb_spy.analyzer.analyzer import ClockResetEnableItemStm32


def report_clock_enable(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    """Add "Clock reset/enabled" chapter to the report."""
    # Circular import error does not allow importing AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    _report_clock_enable_d1(self, bits_data=bits_data, md_file=md_file)
    _report_clock_enable_d2(self, bits_data=bits_data, md_file=md_file)
    _report_clock_enable_d3(self, bits_data=bits_data, md_file=md_file)


def _report_clock_enable_d1(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    items = [
        ClockResetEnableItemStm32("SDMMC1 and SDMMC1 Delay", None, "RCC_AHB3ENR.SDMMC1EN"),
        ClockResetEnableItemStm32("QUADSPI and QUADSPI Delay", None, "RCC_AHB3ENR.QSPIEN"),
        ClockResetEnableItemStm32("FMC", None, "RCC_AHB3ENR.FMCEN"),
        ClockResetEnableItemStm32("JPGDEC", None, "RCC_AHB3ENR.JPGDECEN"),
        ClockResetEnableItemStm32("DMA2D", None, "RCC_AHB3ENR.DMA2DEN"),
        ClockResetEnableItemStm32("MDMA", None, "RCC_AHB3ENR.MDMAEN"),
    ]
    self.report_clock_enable_stm32(
        items=items, bits_data=bits_data, md_file=md_file, title="Clock reset/enabled D1")


def _report_clock_enable_d2(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    items = [
        ClockResetEnableItemStm32("ADC12", None, "RCC_AHB1ENR.ADC12EN"),
        ClockResetEnableItemStm32("DAC12", None, "RCC_APB1LENR.DAC12EN"),
        ClockResetEnableItemStm32("DMA1", None, "RCC_AHB1ENR.DMA1EN"),
        ClockResetEnableItemStm32("DMA2", None, "RCC_AHB1ENR.DMA2EN"),
        ClockResetEnableItemStm32("Ethernet Reception", None, "RCC_AHB1ENR.ETH1RXEN"),
        ClockResetEnableItemStm32("Ethernet Transmission", None, "RCC_AHB1ENR.ETH1TXEN"),
        ClockResetEnableItemStm32("Ethernet MAC bus interface", None, "RCC_AHB1ENR.ETH1MACEN"),
        ClockResetEnableItemStm32("USB1 PHY", None, "RCC_AHB1ENR.USB1OTGHSULPIEN"),
        ClockResetEnableItemStm32("USB1 OTG Peripheral", None, "RCC_AHB1ENR.USB1OTGHSEN"),
        ClockResetEnableItemStm32("USB2 PHY", None, "RCC_AHB1ENR.USB2OTGHSULPIEN"),
        ClockResetEnableItemStm32("USB2 OTG Peripheral", None, "RCC_AHB1ENR.USB2OTGHSEN"),
        ClockResetEnableItemStm32("HRTIM", None, "RCC_APB2ENR.HRTIMEN"),
        ClockResetEnableItemStm32("SPI1", None, "RCC_APB2ENR.SPI1EN"),
        ClockResetEnableItemStm32("SPI2", None, "RCC_APB1LENR.SPI2EN"),
        ClockResetEnableItemStm32("SPI3", None, "RCC_APB1LENR.SPI3EN"),
        ClockResetEnableItemStm32("SPI4", None, "RCC_APB2ENR.SPI4EN"),
        ClockResetEnableItemStm32("SPI5", None, "RCC_APB2ENR.SPI5EN"),
        ClockResetEnableItemStm32("I2C1", None, "RCC_APB1LENR.I2C1EN"),
        ClockResetEnableItemStm32("I2C2", None, "RCC_APB1LENR.I2C2EN"),
        ClockResetEnableItemStm32("I2C3", None, "RCC_APB1LENR.I2C3EN"),
        ClockResetEnableItemStm32("USART1", None, "RCC_APB2ENR.USART1EN"),
        ClockResetEnableItemStm32("USART2", None, "RCC_APB1LENR.USART2EN"),
        ClockResetEnableItemStm32("USART3", None, "RCC_APB1LENR.USART3EN"),
        ClockResetEnableItemStm32("UART4", None, "RCC_APB1LENR.UART4EN"),
        ClockResetEnableItemStm32("UART5", None, "RCC_APB1LENR.UART5EN"),
        ClockResetEnableItemStm32("USART6", None, "RCC_APB2ENR.USART6EN"),
        ClockResetEnableItemStm32("UART7", None, "RCC_APB1LENR.UART7EN"),
        ClockResetEnableItemStm32("UART8", None, "RCC_APB1LENR.UART8EN"),
    ]
    self.report_clock_enable_stm32(
        items=items, bits_data=bits_data, md_file=md_file, title="Clock reset/enabled D2")


def _report_clock_enable_d3(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    items = [
        ClockResetEnableItemStm32("ADC3", None, "RCC_AHB4ENR.ADC3EN"),
        ClockResetEnableItemStm32("GPIOA", None, "RCC_AHB4ENR.GPIOAEN"),
        ClockResetEnableItemStm32("GPIOB", None, "RCC_AHB4ENR.GPIOBEN"),
        ClockResetEnableItemStm32("GPIOC", None, "RCC_AHB4ENR.GPIOCEN"),
        ClockResetEnableItemStm32("GPIOD", None, "RCC_AHB4ENR.GPIODEN"),
        ClockResetEnableItemStm32("GPIOE", None, "RCC_AHB4ENR.GPIOEEN"),
        ClockResetEnableItemStm32("GPIOF", None, "RCC_AHB4ENR.GPIOFEN"),
        ClockResetEnableItemStm32("GPIOG", None, "RCC_AHB4ENR.GPIOGEN"),
        ClockResetEnableItemStm32("GPIOH", None, "RCC_AHB4ENR.GPIOHEN"),
        ClockResetEnableItemStm32("GPIOI", None, "RCC_AHB4ENR.GPIOIEN"),
        ClockResetEnableItemStm32("GPIOJ", None, "RCC_AHB4ENR.GPIOJEN"),
        ClockResetEnableItemStm32("GPIOK", None, "RCC_AHB4ENR.GPIOKEN"),
        ClockResetEnableItemStm32("SYSCFG", None, "RCC_APB4ENR.SYSCFGEN"),
        ClockResetEnableItemStm32("SPI6", None, "RCC_APB4ENR.SPI6EN"),
        ClockResetEnableItemStm32("I2C4", None, "RCC_APB4ENR.I2C4EN"),
        ClockResetEnableItemStm32("LPUART1", None, "RCC_APB4ENR.LPUART1EN"),
    ]
    self.report_clock_enable_stm32(
        items=items, bits_data=bits_data, md_file=md_file, title="Clock reset/enabled D3")
