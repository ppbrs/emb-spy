"""Part of AnalyzerSTM32H743 class."""
import inspect

from emb_spy import Backend
from emb_spy import ReaderConfigCoreReg
from emb_spy import ReaderConfigCoreRegBits
from emb_spy import ReaderConfigMemory
from emb_spy import ReaderConfigMmapReg
from emb_spy import ReaderConfigMmapRegBits
from emb_spy import ReaderStatic
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
) -> dict[str, ReaderStatic.Result]:
    """Read all necessary register bits from the SoC."""
    assert "Analyzer" in [cls.__name__ for cls in inspect.getmro(self.__class__)]
    # which is basically the same as issublass(self.__class__, Analyzer).

    port = Backend.find_openocd_telnet_port()
    results: dict[str, ReaderStatic.Result] = ReaderStatic(
        config=config,
        port=port,
        soc=soc,
        target_name=self.board_cfg.jtag_target_name,
        restart_if_not_running=False,
        halt_if_running=False,
    ).read()

    port = Backend.find_openocd_telnet_port()
    with Backend(port=port, target_name=None) as backend:
        self.state.target_name, self.state.target_state = backend.get_current_target_state()

    for name, result in results.items():
        print(f"{name}: {result.val}, raw(le)={result.raw[::-1].hex()}")

    return results
