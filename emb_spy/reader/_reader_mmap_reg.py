import ctypes
import dataclasses
from typing import Any

from emb_spy.reader._reader_common import MemAddr
from emb_spy.reader._reader_common import MemData
from emb_spy.reader._reader_common import ReaderConfig
from emb_spy.reader._reader_common import RegName
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import Reg
from emb_spy.socs.soc import SoC


@dataclasses.dataclass
class ReaderConfigMmapReg(ReaderConfig):
    """
    The structure filled by _Reader's caller; it defines how the register's value should be returned.
    """
    name: str
    """The name of the memory-mapped register, e.g. GPIOA_MODER."""
    ctype: Any = ctypes.c_uint32
    verbose: bool = False


@dataclasses.dataclass
class ReaderConfigMmapRegBits(ReaderConfig):
    """
    The structure filled by _Reader's caller; it defines how the bits' value should be returned.
    """
    name: str
    """The name of the bits in the memory-mapped register, e.g. GPIOA_MODER.MODER5."""
    verbose: bool = False


class _ReaderMmapReg:
    """"""

    @dataclasses.dataclass
    class _MmapRegConfigExt(ReaderConfigMmapReg):
        """
        Fields that are filled by _Reader.
        """
        mem_addr: int | MemAddr = None
        register: Reg | None = None

    @dataclasses.dataclass
    class _MmapRegBitsConfigExt(ReaderConfigMmapRegBits):
        """
        Fields that are filled by _Reader.
        """
        mem_addr: int | MemAddr = None
        bits: Bits | None = None

    def parse_config(
        self,
        config,
        mem_map,
        core_map,
    ) -> None:
        """"""

        for cfg in config:
            if isinstance(cfg, ReaderConfigMmapReg):
                # "casting" MmapRegConfig to _MmapRegConfigExt:
                cfg_ext = self._MmapRegConfigExt(name=cfg.name)
                for field in dataclasses.fields(cfg):
                    setattr(cfg_ext, field.name, getattr(cfg, field.name))
                self.config_mmap_reg.append(cfg_ext)
            elif isinstance(cfg, ReaderConfigMmapRegBits):
                # "casting" MmapRegBitsConfig to _MmapRegBitsConfigExt:
                cfg_ext = self._MmapRegBitsConfigExt(name=cfg.name)
                for field in dataclasses.fields(cfg):
                    setattr(cfg_ext, field.name, getattr(cfg, field.name))
                self.config_mmap_reg_bits.append(cfg_ext)

        if len(self.config_mmap_reg) or len(self.config_mmap_reg_bits):
            if self.soc is None:
                raise ValueError(
                    "Once reading memory-mapped registers is requested, `soc: SoC` object "
                    "must be provided.")
            if not isinstance(self.soc, SoC):
                raise ValueError(f"`soc: SoC` object type is wrong: {type(self.soc)}.")

        for idx, cfg in enumerate(self.config_mmap_reg):
            for name, register in self.soc.map_name().items():
                assert isinstance(register, Reg)
                if cfg.name == name:
                    self.logger.debug("Found `%s` register in SoC.", cfg.name)

                    mem_addr = register.addr
                    self.config_mmap_reg[idx].mem_addr = mem_addr
                    self.config_mmap_reg[idx].register = register
                    mem_data_size = 4
                    if (mem_data := mem_map.get(mem_addr)) is None or len(mem_data) < mem_data_size:
                        mem_data = bytes(mem_data_size)
                        mem_map[mem_addr] = mem_data
                    break
            else:
                raise ValueError(
                    f"Memory-mapped register `{cfg.name}` is not the provided Registers object.")

        for idx, cfg in enumerate(self.config_mmap_reg_bits):
            if len(cfg.name.split(".")) != 2:
                raise ValueError(
                    f"{cfg.name}: Memory-mapped register bits name is expected to have two parts "
                    "separated by a dot.")
            reg_name, bits_name = cfg.name.split(".")
            for name, register in self.soc.map_name().items():
                assert isinstance(register, Reg)
                if reg_name == name:
                    self.logger.debug("Found `%s` in SoC.", reg_name)
                    for bits in register.bits:
                        if bits.name == bits_name:
                            self.logger.debug("Found `%s` in `%s`.", bits_name, reg_name)
                            self.config_mmap_reg_bits[idx].bits = bits
                            break
                    else:
                        raise ValueError(f"Could not find bits `{bits_name}` in `{reg_name}`.")

                    mem_addr = register.addr
                    mem_data_size = 4
                    self.config_mmap_reg_bits[idx].mem_addr = mem_addr
                    if (mem_data := mem_map.get(mem_addr)) is None or len(mem_data) < mem_data_size:
                        mem_data = bytes(mem_data_size)
                        mem_map[mem_addr] = mem_data
                    break
            else:
                raise ValueError(
                    f"Memory-mapped register `{reg_name}` is not in the provided SoC object.")
