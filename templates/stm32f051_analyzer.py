"""A template showing how to use AnalyzerSTM32F051."""
import logging
import pathlib

from emb_spy import AnalyzerSTM32F051


def main():
    """Run the analyzer."""
    logging.basicConfig(level=logging.INFO)

    board_cfg = AnalyzerSTM32F051.BoardConfig(
        jtag_target_name="stm32f0x.cpu",
    )
    AnalyzerSTM32F051(
        board_cfg=board_cfg,
        report_file_path=pathlib.PosixPath(__file__).with_suffix(".md"),
    ).run()


if __name__ == "__main__":
    main()
