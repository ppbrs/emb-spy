"""Part of AnalyzerSTM32F745 class."""


def _get_af_descr(port: str, pin_idx: int, af_idx: int) -> str:
    """
    :param port: For example, "A".
    """
    af_idx_top = 16
    pin_idx_top = 16
    ports_valid = ("A", "B", "C", "D", "E", "F", "I", "J", "K")
    assert 0 <= pin_idx < pin_idx_top
    assert 0 <= af_idx < af_idx_top
    assert port in ports_valid
    # af_map maps port name to a matrix with pin rows and af colums - the same way
    # it is presented in the datasheet.
    af_map: dict[str, list[list[str]]] = {
        port_: [
            [f"TBD-{port_}-{pin_idx_}-{af_idx_}"
             for af_idx_ in range(af_idx_top)] for pin_idx_ in range(pin_idx_top)]
        for port_ in ports_valid}
    af_map["A"][0][1] = "TIM2_CH1 / TIM2_ETR"
    af_map["A"][1][1] = "TIM2_CH2"
    af_map["A"][2][1] = "TIM2_CH3"
    af_map["A"][8][0] = "MCO1"
    af_map["A"][13][0] = "JTMS / SWDIO"
    af_map["A"][14][0] = "JTCK / SWCLK"
    af_map["A"][15][0] = "JTDI"

    af_map["B"][3][0] = "JTDO / TRACESWO"
    af_map["B"][4][0] = "NJTRST"

    af_map["C"][9][0] = "MCO2"

    return af_map[port][pin_idx][af_idx]
