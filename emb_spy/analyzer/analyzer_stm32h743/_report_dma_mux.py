"""Part of AnalyzerSTM32H743 class."""
from emb_spy import ReaderStaticResult


def report_dma_mux(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file
) -> None:
    """Add "DMAMUX" chapter to the report."""
    # Circular import error does not allow importing AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    md_file.new_header(level=1, title="DMAMUX")

    md_file.new_header(level=2, title="DMAMUX1")
    dma_mux_idx = 1
    legend, table = ["channel", "input request"], []
    for ch_idx in range(16):
        dmamux = f"DMAMUX{dma_mux_idx}"
        conf_reg = f"{dmamux}_C{ch_idx}CR"

        dma_idx = 1 if ch_idx < 8 else 2
        dma_stream_idx = ch_idx % 8
        ch_descr = f"{ch_idx} (DMA{dma_idx}, stream {dma_stream_idx})"
        row = [ch_descr]

        input_request = bits_data[f"{conf_reg}.DMAREQ_ID"].val
        if input_request:
            input_request_name = {
                1: "dmamux1_req_gen0",
                10: "adc2_dma",
                101: "dfsdm1_dma0",
                102: "dfsdm1_dma1",
                103: "dfsdm1_dma2",
                104: "dfsdm1_dma3",
                105: "TIM15_CH1",
                106: "TIM15_UP",
                107: "TIM15_TRIG",
                108: "TIM15_COM",
                109: "TIM16_CH1",
                11: "TIM1_CH1",
                110: "TIM16_UP",
                111: "TIM17_CH1",
                112: "TIM17_UP",
                113: "sai3_a_dma",
                114: "sai3_b_dma",
                115: "adc3_dma",
                12: "TIM1_CH2",
                13: "TIM1_CH3",
                14: "TIM1_CH4",
                15: "TIM1_UP",
                16: "TIM1_TRIG",
                17: "TIM1_COM",
                18: "TIM2_CH1",
                19: "TIM2_CH2",
                2: "dmamux1_req_gen1",
                20: "TIM2_CH3",
                21: "TIM2_CH4",
                22: "TIM2_UP",
                23: "TIM3_CH1",
                24: "TIM3_CH2",
                25: "TIM3_CH3",
                26: "TIM3_CH4",
                27: "TIM3_UP",
                28: "TIM3_TRIG",
                29: "TIM4_CH1",
                3: "dmamux1_req_gen2",
                30: "TIM4_CH2",
                31: "TIM4_CH3",
                32: "TIM4_UP",
                33: "i2c1_rx_dma",
                34: "i2c1_tx_dma",
                35: "i2c2_rx_dma",
                36: "i2c2_tx_dma",
                37: "spi1_rx_dma",
                38: "spi1_tx_dma",
                39: "spi2_rx_dma",
                4: "dmamux1_req_gen3",
                40: "spi2_tx_dma",
                41: "usart1_rx_dma",
                42: "usart1_tx_dma",
                43: "usart2_rx_dma",
                44: "usart2_tx_dma",
                45: "usart3_rx_dma",
                46: "usart3_tx_dma",
                47: "TIM8_CH1",
                48: "TIM8_CH2",
                49: "TIM8_CH3",
                5: "dmamux1_req_gen4",
                50: "TIM8_CH4",
                51: "TIM8_UP",
                52: "TIM8_TRIG95HR_REQ(1)",
                53: "TIM8_COM96HR_REQ(2)",
                54: "Reserved97HR_REQ(3)",
                55: "TIM5_CH198HR_REQ(4)",
                56: "TIM5_CH299HR_REQ(5)",
                57: "TIM5_CH3100HR_REQ(6)",
                58: "TIM5_CH4",
                59: "TIM5_UP",
                6: "dmamux1_req_gen5",
                60: "TIM5_TRIG",
                61: "spi3_rx_dma",
                62: "spi3_tx_dma",
                63: "uart4_rx_dma",
                64: "uart4_tx_dma",
                65: "uart5_rx_dma",
                66: "uart5_tx_dma",
                67: "dac_ch1_dma",
                68: "dac_ch2_dma",
                69: "TIM6_UP",
                7: "dmamux1_req_gen6",
                70: "TIM7_UP",
                71: "usart6_rx_dma",
                72: "usart6_tx_dma",
                73: "i2c3_rx_dma ",
                74: "i2c3_tx_dma ",
                75: "dcmi_dma ",
                76: "cryp_in_dma ",
                77: "cryp_out_dma ",
                78: "hash_in_dma ",
                79: "uart7_rx_dma ",
                8: "dmamux1_req_gen7",
                80: "uart7_tx_dma ",
                81: "uart8_rx_dma ",
                82: "uart8_tx_dma ",
                83: "spi4_rx_dma",
                84: "spi4_tx_dma",
                85: "spi5_rx_dma",
                86: "spi5_tx_dma",
                87: "sai1a_dma",
                88: "sai1b_dma",
                89: "sai2a_dma",
                9: "adc1_dma",
                90: "sai2b_dma",
                91: "swpmi_rx_dma",
                92: "swpmi_tx_dma",
                93: "spdifrx_dat_dma",
                94: "spdifrx_ctrl_dma",
            }[input_request]
            row.append(f"{input_request} = {input_request_name}")
        else:
            row.append("")

        table.extend(row)

    md_file.new_table(
        columns=len(legend), rows=(1 + len(table) // len(legend)), text_align="left",
        text=(legend + table),
    )

    md_file.new_line("***")

    md_file.new_header(level=2, title="DMAMUX2")
    md_file.new_line("***")
