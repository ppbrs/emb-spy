
import logging

from emb_spy.app_swo import _AppSwoParser, AppSwo


_logger = logging.getLogger(__name__)


def test_app_swo_parsing() -> None:
    test_cases = [
        (
            bytes.fromhex("0161026200036300000009710a72000b73000000"),
            {
                0: bytes.fromhex("61620063000000"),
                1: bytes.fromhex("71720073000000"),
            }
        ),
    ]

    for test_case in test_cases:
        in_bytes = test_case[0]
        out_expect = test_case[1]
        assert isinstance(in_bytes, bytes)
        assert isinstance(out_expect, dict)

        parser = _AppSwoParser(tsformat=AppSwo.TimestampFormat.ABSOLUTE)
        parser.process_bytes(in_bytes)
        out_parsed = parser.data
        assert {*out_expect.keys()} == {*out_parsed.keys()}
        for key in out_expect.keys():
            assert out_expect[key] == out_parsed[key]
        # _logger.info(parser.data)
