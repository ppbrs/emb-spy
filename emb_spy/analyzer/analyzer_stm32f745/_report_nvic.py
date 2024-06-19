"""Part of AnalyzerSTM32F745."""
from emb_spy import ReaderStaticResult

_irq_num = 98
_irq_descr = {irqn: f"IRQ{irqn}" for irqn in range(_irq_num)}

# 07settableWWDGWindow Watchdog interrupt0x0000 0040
# 18settablePVDPVD through EXTI line detection # interrupt0x0000 0044
# 29settableTAMP_STAMPTamper and TimeStamp interrupts # through the EXTI line0x0000 0048
# 310settableRTC_WKUPRTC Wakeup interrupt through the # EXTI line0x0000 004C
# 411settableFLASHFlash global interrupt0x0000 0050
# 512settableRCCRCC global interrupt0x0000 0054
# 613settableEXTI0EXTI Line0 interrupt0x0000 0058
# 714settableEXTI1EXTI Line1 interrupt0x0000 005C
# 815settableEXTI2EXTI Line2 interrupt0x0000 0060
# 916settableEXTI3EXTI Line3 interrupt0x0000 0064
# 1017settableEXTI4EXTI Line4 interrupt0x0000 0068
# 1118settableDMA1_Stream0DMA1 Stream0 global interrupt0x0000 006C
# 1219settableDMA1_Stream1DMA1 Stream1 global interrupt0x0000 0070
# 1320settableDMA1_Stream2DMA1 Stream2 global interrupt0x0000 0074
_irq_descr[14] = "DMA1_Stream3"  # 1421settableDMA1 Stream3 global interrupt0x0000 0078
# 1522settableDMA1_Stream4DMA1 Stream4 global interrupt0x0000 007C
# 1623settableDMA1_Stream5DMA1 Stream5 global interrupt0x0000 0080
# 1724settableDMA1_Stream6DMA1 Stream6 global interrupt0x0000 0084
# 1825settableADCADC1, ADC2 and ADC3 global # interrupts0x0000 0088
# 1926settableCAN1_TXCAN1 TX interrupts0x0000 008C
# 2027settableCAN1_RX0CAN1 RX0 interrupts0x0000 0090
# 2128settableCAN1_RX1CAN1 RX1 interrupt0x0000 0094
# 2229settableCAN1_SCECAN1 SCE interrupt0x0000 0098
# 2330settableEXTI9_5EXTI Line[9:5] interrupts0x0000 009C
# 2431settableTIM1_BRK_TIM9TIM1 Break interrupt and TIM9 global interrupt0x0000 00A0
_irq_descr[25] = "TIM1_UP_TIM10TIM1 Update interrupt and TIM10 global interrupt"  # 2532settable 0x0000 00A4
# 2633settableTIM1_TRG_COM_TIM11TIM1 Trigger and Commutation
# interrupts and TIM11 global interrupt0x0000 00A8
# 2734settableTIM1_CCTIM1 Capture Compare interrupt0x0000 00AC
# 2835settableTIM2TIM2 global interrupt0x0000 00B0
# 2936settableTIM3TIM3 global interrupt0x0000 00B4
# 3037settableTIM4TIM4 global interrupt0x0000 00B8
# 2C1 event interrupt0x0000 00BC
# Acronym
# Description
# Address
# 3138settableI2C1_EVI3239settableI2C1_ERI2C1 error interrupt0x0000 00C0
# I2C2_EVI2C2 event interrupt0x0000 00C4
# 0x0000 00C8
# 3340settable
# 3441settableI2C2_ERI2C2 error interrupt3542settableSPI1SPI1 global interrupt0x0000 00CC
# 3643settableSPI2SPI2 global interrupt0x0000 00D0
# 3744settableUSART1USART1 global interrupt0x0000 00D4
# 3845settableUSART2USART2 global interrupt0x0000 00D8
# 3946settableUSART3USART3 global interrupt0x0000 00DC
# 4047settableEXTI15_10EXTI Line[15:10] interrupts0x0000 00E0
# 4148settableRTC_AlarmRTC Alarms (A and B) through EXTI line interrupt0x0000 00E4
# 4249settableOTG_FS_WKUPUSB On-The-Go FS Wakeup through # EXTI line interrupt0x0000 00E8
# 4350settableTIM8_BRK_TIM12TIM8 Break interrupt and TIM12 # global interrupt0x0000 00EC
# 4451settableTIM8_UP_TIM13TIM8 Update interrupt and TIM13 # global interrupt0x0000 00F0
# 4552settableTIM8_TRG_COM_TIM14TIM8 Trigger and Commutation
# interrupts and TIM14 global interrupt0x0000 00F4
# 4653settableTIM8_CCTIM8 Capture Compare interrupt0x0000 00F8
# 4754settableDMA1_Stream7DMA1 Stream7 global interrupt0x0000 00FC
# 4855settableFSMCFSMC global interrupt0x0000 0100
# 4956settableSDMMC1SDMMC1 global interrupt0x0000 0104
# 5057settableTIM5TIM5 global interrupt0x0000 0108
# 5158settableSPI3SPI3 global interrupt0x0000 010C
# 5259settableUART4UART4 global interrupt0x0000 0110
# 5360settableUART5UART5 global interrupt0x0000 0114
# 5461settableTIM6_DACTIM6 global interrupt,
# DAC1 and DAC2 underrun error
# interrupts0x0000 0118
# 5562settableTIM7TIM7 global interrupt0x0000 011C
# 5663settableDMA2_Stream0DMA2 Stream0 global interrupt0x0000 0120
# 5764settableDMA2_Stream1DMA2 Stream1 global interrupt0x0000 0124
# 5865settableDMA2_Stream2DMA2 Stream2 global interrupt0x0000 0128
# 5966settableDMA2_Stream3DMA2 Stream3 global interrupt0x0000 012C
# 6067settableDMA2_Stream4DMA2 Stream4 global interrupt0x0000 0130
# 6168settableETHEthernet global interrupt0x0000 0134
# 6269settableETH_WKUPEthernet Wakeup through EXTI line
# interrupt0x0000 0138
# 6370settableCAN2_TXCAN2 TX interrupts0x0000 013C
# 6471settableCAN2_RX0CAN2 RX0 interrupts0x0000 0140
# 6572settableCAN2_RX1CAN2 RX1 interrupt0x0000 0144
# 6673settableCAN2_SCECAN2 SCE interrupt0x0000 0148
# 6774settableOTG_FSUSB On The Go FS global interrupt0x0000 014C
# 6875settableDMA2_Stream5DMA2 Stream5 global interrupt0x0000 0150
# 6976settableDMA2_Stream6DMA2 Stream6 global interrupt0x0000 0154
# 7077settableDMA2_Stream7DMA2 Stream7 global interrupt0x0000 0158
# 7178settableUSART6USART6 global interrupt0x0000 015C
# 2C3 event interrupt0x0000 0160
# Acronym
# Description
# Address
# 7279settableI2C3_EVI7380settableI2C3_ERI2C3 error interrupt0x0000 0164
# 7481settableOTG_HS_EP1_OUTUSB On The Go HS End Point 1 Out
# global interrupt0x0000 0168
# 7582settableOTG_HS_EP1_INUSB On The Go HS End Point 1 In
# global interrupt0x0000 016C
# 7683settableOTG_HS_WKUPUSB On The Go HS Wakeup through
# EXTI interrupt0x0000 0170
# 7784settableOTG_HSUSB On The Go HS global interrupt0x0000 0174
# 7885settableDCMIDCMI global interrupt0x0000 0178
# 7986settableCRYPCRYP crypto global interrupt0x0000 017C
# 8087settableHASH_RNGHash and Rng global interrupt0x0000 0180
# 8188settableFPUFPU global interrupt0x0000 0184
# 8289settableUART7UART7 global interrupt0x0000 0188
# 8390settableUART8UART8 global interrupt0x0000 018C
# 8491settableSPI4SPI4 global interrupt0x0000 0190
# 8592settableSPI5SPI5 global interrupt0x0000 0194
# 8693settableSPI6SPI6 global interrupt0x0000 0198
# 8794settableSAI1SAI1 global interrupt0x0000 019C
# 8895settableLCD-TFTLCD-TFT global interrupt0x0000 01A0
# 8996settableLCD-TFTLCD-TFT global Error interrupt0x0000 01A4
# 9097settableDMA2DDMA2D global interrupt0x0000 01A8
# 9198settableSAI2SAI2 global interrupt0x0000 01AC
# 9299settableQuadSPIQuadSPI global interrupt0x0000 01B0
# 93100settableLP Timer1LP Timer1 global interrupt0x0000 01B4
# 94101settableHDMI-CECHDMI-CEC global interrupt0x0000 01B8
# 95102settableI2C4_EVI2C4 event interrupt0x0000 01BC
# 96103settableI2C4_ERI2C4 Error interrupt0x0000 01C0
# 97104settableSPDIFRXSPDIFRX global interrupt0x0000 01C4


def report_nvic(
    self,
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    """Add the NVIC chapter to the report."""
    assert self.__class__.__name__ == "AnalyzerSTM32F745"
    # This is equivalent to assert isinstance(self, AnalyzerSTM32F745).
    # I do this to avoid the circular import error.
    self.report_nvic_stm32(bits_data=bits_data, md_file=md_file, irq_num=_irq_num, irq_descr=_irq_descr)
