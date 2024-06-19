"""Part of AnalyzerSTM32H743 class."""


def get_af_descr(port: str, pin_idx: int, af_idx: int) -> str:
    """
    :param port: For example, "A".
    """
    af_idx_top = 16
    pin_idx_top = 16
    ports_valid = ("A", "B", "C", "D", "E", "F",)
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
    af_map["A"][1][11] = "ETH_MII_RX_CLK/ETH_RMII_REF_CLK"
    return af_map[port][pin_idx][af_idx]
