import ctypes
import dataclasses
from typing import Any

from emb_spy.reader._reader_common import MemAddr
from emb_spy.reader._reader_common import MemData
from emb_spy.reader._reader_common import ReaderConfig
# from emb_spy.reader._reader_common import MemName
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import Reg
from emb_spy.socs.soc import SoC


@dataclasses.dataclass
class ReaderConfigMemory(ReaderConfig):
    """
    The structure that defines how the value should be returned or printed.
    """
    addr: MemAddr
    ctype: Any = ctypes.c_uint32
    verbose: bool = False


class _ReaderMemory:
    """"""
    @dataclasses.dataclass
    class _MemoryConfigExt(ReaderConfigMemory):
        """
        Fields that are filled by _Reader.
        """

    def parse_config(
        self,
        config,
        mem_map,
        core_map,
    ) -> None:
        """"""

        for cfg in config:
            if isinstance(cfg, ReaderConfigMemory):
                # "casting" MemoryConfig to _MemoryConfigExt:
                cfg_ext = self._MemoryConfigExt(addr=cfg.addr)
                for field in dataclasses.fields(cfg):
                    setattr(cfg_ext, field.name, getattr(cfg, field.name))
                self.config_memory.append(cfg_ext)

        for idx, cfg in enumerate(self.config_memory):
            mem_addr = cfg.addr
            mem_data_size = ctypes.sizeof(cfg.ctype)
            self.config_memory[idx].mem_addr = mem_addr
            if (mem_data := mem_map.get(mem_addr)) is None or len(mem_data) < mem_data_size:
                mem_data = bytes(mem_data_size)
                mem_map[mem_addr] = mem_data
