"""Part of AnalyzerSTM32F051."""
from emb_spy import ReaderStaticResult

_irq_descr = {
    0: "WWDG",
    1: "PVD_VDDIO2",
    2: "RTC",
    3: "FLASH",
    4: "RCC_CRS",
    5: "EXTI0_1",
    6: "EXTI2_3",
    7: "EXTI4_15",
    8: "TSC",
    9: "DMA_CH1",
    10: "DMA_CH2_3_DMA2_CH1_2",
    11: "DMA_CH4_5_6_7_DMA2_CH3_4_5",
    12: "ADC_COMP",
    13: "TIM1_BRK_UP_TRG_COM",
    14: "TIM1_CC",
    15: "TIM2",
    16: "TIM3",
    17: "TIM6_DAC",
    18: "TIM7",
    19: "TIM14",
    20: "TIM15",
    21: "TIM16",
    22: "TIM17",
    23: "I2C1",
    24: "I2C2",
    25: "SPI1",
    26: "SPI2",
    27: "USART1",
    28: "USART2",
    29: "USART3_4_5_6_7_8",
    30: "CEC_CAN",
    31: "USB",
}


def report_nvic(
    self,
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    """Add the NVIC chapter to the report."""
    assert self.__class__.__name__ == "AnalyzerSTM32F051"
    # This is equivalent to assert isinstance(self, AnalyzerSTM32F051).
    # I do this to avoid the circular import error.
    self.report_nvic_stm32(bits_data=bits_data, md_file=md_file, irq_num=32, irq_descr=_irq_descr)
