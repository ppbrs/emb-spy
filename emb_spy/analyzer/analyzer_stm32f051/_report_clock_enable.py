"""Part of AnalyzerSTM32F051 class."""
from emb_spy import ReaderStaticResult
from emb_spy.analyzer.analyzer import ClockResetEnableItemStm32


def report_clock_enable(
    self,  # : AnalyzerSTM32F051
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    # Circular import error does not allow importing AnalyzerSTM32F051 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32F051"

    items = [
        ClockResetEnableItemStm32("TIM1", "RCC_APB2RSTR.TIM1RST", "RCC_APB2ENR.TIM1EN"),
        ClockResetEnableItemStm32("TIM2", "RCC_APB1RSTR.TIM2RST", "RCC_APB1ENR.TIM2EN"),
        ClockResetEnableItemStm32("TIM3", "RCC_APB1RSTR.TIM3RST", "RCC_APB1ENR.TIM3EN"),
        ClockResetEnableItemStm32("TIM6", "RCC_APB1RSTR.TIM6RST", "RCC_APB1ENR.TIM6EN"),
        ClockResetEnableItemStm32("TIM7", "RCC_APB1RSTR.TIM7RST", "RCC_APB1ENR.TIM7EN"),
        ClockResetEnableItemStm32("USART1", "RCC_APB2RSTR.USART1RST", "RCC_APB2ENR.USART1EN"),
        ClockResetEnableItemStm32("USART2", "RCC_APB1RSTR.USART2RST", "RCC_APB1ENR.USART2EN"),
        ClockResetEnableItemStm32("I2C1", "RCC_APB1RSTR.I2C1RST", "RCC_APB1ENR.I2C1EN"),
        ClockResetEnableItemStm32("I2C2", "RCC_APB1RSTR.I2C2RST", "RCC_APB1ENR.I2C2EN"),
    ]
    self.report_clock_enable_stm32(bits_data, md_file, items=items, title="Clock reset/enable")
