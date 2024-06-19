import ctypes
import dataclasses
from typing import Any

from emb_spy.reader._reader_common import MemAddr
from emb_spy.reader._reader_common import MemData
from emb_spy.reader._reader_common import ReaderConfig
from emb_spy.reader._reader_common import RegName
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import CoreReg
from emb_spy.socs.reg import Reg
from emb_spy.socs.soc import SoC


@dataclasses.dataclass
class ReaderConfigCoreReg(ReaderConfig):
    """
    The structure filled by reader's client that defines how the value should be returned.
    """
    name: str
    ctype: Any = ctypes.c_uint32
    verbose: bool = False


@dataclasses.dataclass
class ReaderConfigCoreRegBits(ReaderConfig):
    """
    The structure filled by reader's client that defines how the value should be returned.
    """
    name: str
    verbose: bool = False


class _ReaderCoreReg:
    """"""

    @dataclasses.dataclass
    class _CoreRegConfigExt(ReaderConfigCoreReg):
        """CoreRegConfig with extra fields filled by _Reader."""
        reg_name: str = None
        reg: CoreReg = None
 
    @dataclasses.dataclass
    class _CoreRegBitsConfigExt(ReaderConfigCoreRegBits):
        """CoreRegBitsConfig with extra fields filled by _Reader."""
        reg_name: str = None
        reg: CoreReg = None

    def parse_config(
        self,
        config,
        mem_map,
        core_map,
    ) -> None:
        """"""

        for cfg in config:
            if isinstance(cfg, ReaderConfigCoreReg):
                # "Casting" CoreRegConfig to _CoreRegConfigExt:
                cfg_ext = self._CoreRegConfigExt(name=cfg.name)
                for field in dataclasses.fields(cfg):
                    setattr(cfg_ext, field.name, getattr(cfg, field.name))
                self.config_core_reg.append(cfg_ext)
            elif isinstance(cfg, ReaderConfigCoreRegBits):
                # "Casting" ReaderConfigCoreRegBits to _CoreRegBitsConfigExt:
                cfg_ext = self._CoreRegBitsConfigExt(name=cfg.name)
                for field in dataclasses.fields(cfg):
                    setattr(cfg_ext, field.name, getattr(cfg, field.name))
                self.config_core_reg_bits.append(cfg_ext)

        if len(self.config_core_reg) or len(self.config_core_reg_bits):
            if self.soc is None:
                raise ValueError(
                    "Once reading core registers is requested, `SoC` object must be provided.")
            if not isinstance(self.soc, SoC):
                raise ValueError(f"`soc: SoC` object type is wrong: {type(self.soc)}.")
            if not self.halt_if_running:
                self.logger.warning(
                    "`halt_if_running` must be True because reading core registers is requested.")

        for idx, cfg in enumerate(self.config_core_reg):
            for name, register in self.soc.map_name().items():
                assert isinstance(register, Reg)
                if cfg.name == name:
                    self.logger.debug("Found `%s` register in SoC.", cfg.name)

                    cr_name = register.addr
                    self.config_core_reg[idx].reg = register
                    self.config_core_reg[idx].reg_name = register.addr
                    mem_data_size = 4
                    if (mem_data := core_map.get(cr_name)) is None:
                        mem_data = bytes(mem_data_size)
                        core_map[cr_name] = mem_data
                    break
            else:
                raise ValueError(
                    f"Core register `{cfg.name}` is not in the provided SoC object.")

        for idx, cfg in enumerate(self.config_core_reg_bits):
            if len(cfg.name.split(".")) != 2:
                raise ValueError(
                    f"{cfg.name}: Core register bits name is expected to have two parts "
                    "separated by a dot.")
            reg_name, bits_name = cfg.name.split(".")
            for name, register in self.soc.map_name().items():
                assert isinstance(register, Reg)
                if reg_name == name:
                    self.logger.debug("Found `%s` in SoC.", reg_name)
                    for bits in register.bits:
                        if bits.name == bits_name:
                            self.logger.debug("Found `%s` in `%s`.", bits_name, reg_name)
                            self.config_core_reg_bits[idx].bits = bits
                            break
                    else:
                        raise ValueError(f"Could not find bits `{bits_name}` in `{reg_name}`.")

                    cr_name = register.addr
                    self.config_core_reg_bits[idx].reg = register
                    self.config_core_reg_bits[idx].reg_name = register.addr
                    mem_data_size = 4
                    if (mem_data := core_map.get(cr_name)) is None:
                        mem_data = bytes(mem_data_size)
                        core_map[cr_name] = mem_data
                    break
            else:
                raise ValueError(
                    f"Core register `{reg_name}` is not in the provided SoC object.")
