"""A template showing how to use AnalyzerSTM32F745."""
import logging
import pathlib

from emb_spy import AnalyzerSTM32F745


def main():
    """Run the analyzer."""
    logging.basicConfig(level=logging.INFO)

    jtag_target_name = "solo.cpu"
    # jtag_target_name = "master.cpu"
    # jtag_target_name = "axis.cpu"

    board_cfg = AnalyzerSTM32F745.BoardConfig(
        jtag_target_name=jtag_target_name,
        resonator_freq=24e6,
        external_freq=24e6,
    )
    AnalyzerSTM32F745(
        board_cfg=board_cfg,
        report_file_path=pathlib.PosixPath(__file__).with_suffix(".md"),
    ).run()


if __name__ == "__main__":
    main()
