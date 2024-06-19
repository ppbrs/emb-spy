from __future__ import annotations

import logging
import pathlib

from emb_spy.reader._reader_common import MemAddr
from emb_spy.reader._reader_common import MemData
from emb_spy.reader._reader_common import ReaderConfig
from emb_spy.reader._reader_common import RegName
from emb_spy.reader._reader_common import SymbolName
from emb_spy.reader._reader_core_reg import ReaderConfigCoreReg
from emb_spy.reader._reader_core_reg import ReaderConfigCoreRegBits
from emb_spy.reader._reader_core_reg import _ReaderCoreReg
from emb_spy.reader._reader_memory import ReaderConfigMemory
from emb_spy.reader._reader_memory import _ReaderMemory
from emb_spy.reader._reader_mmap_reg import ReaderConfigMmapReg
from emb_spy.reader._reader_mmap_reg import ReaderConfigMmapRegBits
from emb_spy.reader._reader_mmap_reg import _ReaderMmapReg
from emb_spy.reader._reader_symbol import ReaderConfigSymbol
from emb_spy.reader._reader_symbol import _ReaderSymbol
# from emb_spy.socs.bits import Bits
# from emb_spy.socs.reg import Reg
from emb_spy.socs.soc import SoC


# todo: Config = MmapRegConfig | ...


class _Reader(_ReaderMmapReg, _ReaderCoreReg, _ReaderMemory, _ReaderSymbol):

    def __init__(
        self,
        config: list[ReaderConfig],
        host: str = "localhost",
        port: int | None = None,
        target_name: str | None = None,
        logger_suffix: str | None = None,
        soc: SoC | None = None,
        elf_path: pathlib.PosixPath | None = None,
        halt_if_running: bool = False,
        restart_if_not_running: bool = False,
    ) -> None:
        """
        Prepare for reading

        ELF file will be parsed here.
        Configuration will be checked here.

        :param logger_suffix: Optional suffix for the logger name.
        """
        self.logger = logging.getLogger(
            self.__class__.__name__ + ("" if logger_suffix is None else logger_suffix))
        self.host = host
        self.port = port
        self.target_name = target_name
        self.logger_suffix = logger_suffix

        self.soc = soc
        self.elf_path = elf_path

        self.restart_if_not_running = restart_if_not_running
        self.halt_if_running = halt_if_running

        self.config = config

        # Memory addresses that will be read from the target.
        # This array will be filled by addresses of symbols, memory mapped registers,
        # and other objects requested by the application.
        self.mem_map: dict[MemAddr, MemData] = {}
        self.core_map: dict[Name, MemData] = {}

        self.config_symbol = []
        self.config_mmap_reg = []
        """Sub-config that contains only memory-mapped registers requested by client."""
        self.config_mmap_reg_bits = []
        self.config_memory = []
        self.config_core_reg = []
        self.config_core_reg_bits = []

        self.parse_config(config)

    def parse_config(self, config):

        for cfg in config:
            if not isinstance(cfg, (ReaderConfigMmapReg, ReaderConfigMmapRegBits, ReaderConfigSymbol, ReaderConfigMemory, ReaderConfigCoreReg, ReaderConfigCoreRegBits)):
                raise TypeError(f"Config item has wrong type: {cfg}.")

        _ReaderMmapReg.parse_config(self, config, self.mem_map, self.core_map)
        _ReaderCoreReg.parse_config(self, config, self.mem_map, self.core_map)
        _ReaderMemory.parse_config(self, config, self.mem_map, self.core_map)
        _ReaderSymbol.parse_config(self, config, self.mem_map, self.core_map)
