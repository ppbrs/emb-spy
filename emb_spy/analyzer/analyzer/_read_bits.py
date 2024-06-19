"""Part of AnalyzerSTM32H743 class."""
import inspect
import logging

from emb_spy import Backend
from emb_spy import ReaderConfigCoreReg
from emb_spy import ReaderConfigCoreRegBits
from emb_spy import ReaderConfigMemory
from emb_spy import ReaderConfigMmapReg
from emb_spy import ReaderConfigMmapRegBits
from emb_spy import ReaderStatic
from emb_spy import ReaderStaticResult
from emb_spy.socs.soc import SoC

ConfigType = list[
    ReaderConfigMmapReg | ReaderConfigMmapRegBits
    | ReaderConfigCoreReg | ReaderConfigCoreRegBits
    | ReaderConfigMemory
]


def read_bits(
    self,
    soc: SoC,
    config: ConfigType,
) -> dict[str, ReaderStaticResult]:
    """Read all necessary register bits from the SoC."""
    assert "Analyzer" in [cls.__name__ for cls in inspect.getmro(self.__class__)]
    # which is basically the same as issublass(self.__class__, Analyzer).

    results: dict[str, ReaderStaticResult] = ReaderStatic(
        config=config,
        host=self.server[0],
        port=self.server[1],
        soc=soc,
        target_name=self.board_cfg.jtag_target_name,
        restart_if_not_running=False,
        halt_if_running=False,
    ).read()

    with Backend(
        host=self.server[0],
        port=self.server[1],
        target_name=self.board_cfg.jtag_target_name,
    ) as backend:
        self.state.target_name, self.state.target_state = backend.get_current_target_state()

    logger = logging.getLogger("Analyzer")
    for name, result in results.items():
        logger.info("%s: %s, raw(le)=%s", name, result.val, result.raw[::-1].hex())

    return results
