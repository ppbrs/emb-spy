"""A template showing how to use AnalyzerSTM32H743."""
import logging
import pathlib

from emb_spy import AnalyzerSTM32H743


def main():
    """Run the analyzer."""
    logging.basicConfig(level=logging.INFO)

    # jtag_target_name = None
    # jtag_target_name = "stm32h7x.cpu0"
    jtag_target_name = "master.cpu0"
    # jtag_target_name = "solo.cpu0"
    # jtag_target_name = "axis1.cpu0"
    # jtag_target_name = "axis2.cpu0"

    board_cfg = AnalyzerSTM32H743.BoardConfig(
        jtag_target_name=jtag_target_name,
        resonator_freq=24e6,
        external_freq=4e6,
    )
    AnalyzerSTM32H743(
        board_cfg=board_cfg,
        report_file_path=pathlib.PosixPath(__file__).with_suffix(".md"),
    ).run()


if __name__ == "__main__":
    main()
