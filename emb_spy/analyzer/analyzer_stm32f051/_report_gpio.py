"""Part of AnalyzerSTM32F051."""


def _get_af_descr(port: str, pin_idx: int, af_idx: int) -> str:
    """
    :param port: For example, "A".
    """
    af_idx_top = 8
    pin_idx_top = 16
    ports_valid = ("A", "B", "C")
    assert 0 <= pin_idx < pin_idx_top
    assert 0 <= af_idx < af_idx_top
    assert port in ports_valid
    # af_map maps port name to a matrix with pin rows and af colums - the same way
    # it is presented in the datasheet.
    af_map: dict[str, list[list[str]]] = {
        port_: [
            [f"TBD-P{port_}{pin_idx_}-AF{af_idx_}"
             for af_idx_ in range(af_idx_top)] for pin_idx_ in range(pin_idx_top)]
        for port_ in ports_valid}

    af_map["A"][2][1] = "USART2_TX"
    af_map["A"][3][1] = "USART2_RX"
    af_map["A"][13][0] = "SWDIO"
    af_map["A"][14][0] = "SWCLK"

    af_map["B"][6][1] = "I2C1_SCL"
    af_map["B"][7][1] = "I2C1_SDA"
    af_map["B"][10][1] = "I2C2_SCL"
    af_map["B"][11][1] = "I2C2_SDA"

    return af_map[port][pin_idx][af_idx]
