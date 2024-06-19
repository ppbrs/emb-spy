

from emb_spy.reader._reader import _Reader
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC
from emb_spy import ReaderConfigMmapReg


def test_reader_mmreg() -> None:
    pass

    mmReg1 = MmapReg(name="name1", addr=1)
    mmReg2 = MmapReg(name="name2", addr=2)
    soc = SoC().append(mmReg1).append(mmReg2)

    config: list[ReaderConfigMmapReg] = [
        ReaderConfigMmapReg(name="name1", verbose=False),
        ReaderConfigMmapReg(name="name2", verbose=False),
    ]

    reader = _Reader(
        config=config, soc=soc,
    )
    _ = reader
