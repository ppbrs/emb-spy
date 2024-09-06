"""
Application that can read and print the contents of multiple registers and/or symbols
from a single MCU connected via OpenOCD.
"""
from __future__ import annotations

import dataclasses

from emb_spy.backend import Backend
from emb_spy.reader._reader import _Reader


class ReaderStatic(_Reader):
    """A class that contains methods of the application."""

    @dataclasses.dataclass
    class Result:
        """An instance of this type will be returned to ReaderStatic's caller."""

        val: int | float  # or ctypes
        raw: bytes
        """Raw bytes as they were read from a SoC."""
        descr: str
        """Human-readable report."""
        # name, type

    def read(self) -> dict[str, int]:
        """
        Read all locations once.
        """
        self.logger.debug("App called.")

        self.logger.debug("mem_map before: %s", self.mem_map)
        self.logger.debug("core_map before: %s", self.core_map)

        with Backend(
            host=self.host,
            port=self.port,
            target_name=self.target_name,
            logger_suffix=self.logger_suffix,
            restart_if_not_running=self.restart_if_not_running,
            halt_if_running=self.halt_if_running
        ) as backend:

            # self.mem_map is populated in the parent constructor.
            # mem_addr_array: dict[MemAddr, MemData] = {}

            for mem_addr in self.mem_map.keys():
                mem_data_size = len(self.mem_map[mem_addr])
                mem_data = backend.read_raw_memory(addr=mem_addr, size=mem_data_size)
                assert isinstance(mem_data, bytes)
                self.mem_map[mem_addr] = mem_data

            for core_reg_name in self.core_map.keys():
                mem_data = backend.read_core_register(name=core_reg_name)
                assert isinstance(mem_data, bytes)
                self.core_map[core_reg_name] = mem_data

        self.logger.debug("mem_map after: %s", self.mem_map)
        self.logger.debug("core_map after: %s", self.core_map)

        results: dict[str, ReaderStatic.Result] = {}

        for cfg in self.config_symbol:
            assert isinstance(cfg, self._SymbolConfigExt)
            # print(cfg)
            mem_addr = cfg.mem_addr
            mem_data = self.mem_map[mem_addr]
            val = cfg.ctype.from_buffer_copy(mem_data)
            result = self.Result(
                val=val,
                raw=mem_data,
                descr=None)
            results[cfg.name] = result

        for cfg in self.config_memory:
            assert isinstance(cfg, self._MemoryConfigExt)
            # print(cfg)
            mem_addr = cfg.addr
            mem_data = self.mem_map[mem_addr]
            val = cfg.ctype.from_buffer_copy(mem_data)
            result = self.Result(
                val=val,
                raw=mem_data,
                descr=None)
            results[cfg.addr] = result

        for cfg in self.config_mmap_reg:
            assert isinstance(cfg, self._MmapRegConfigExt)
            # print(cfg)
            mem_addr = cfg.mem_addr
            mem_data: bytes = self.mem_map[mem_addr]
            # val = int.from_bytes(mem_data, byteorder="little", signed=False)
            val = cfg.ctype.from_buffer_copy(mem_data)
            result = self.Result(
                val=val.value,
                raw=mem_data,
                descr=cfg.register.get_descr(value=mem_data, verbose=cfg.verbose))
            results[cfg.name] = result

        for cfg in self.config_mmap_reg_bits:
            assert isinstance(cfg, self._MmapRegBitsConfigExt)
            # print(cfg)
            mem_addr = cfg.mem_addr
            mem_data = self.mem_map[mem_addr]
            result = self.Result(
                val=cfg.bits.get_value(mem_data),
                raw=mem_data,
                descr=cfg.bits.get_descr(reg_value=mem_data, verbose=cfg.verbose))
            results[cfg.name] = result

        for cfg in self.config_core_reg:
            assert isinstance(cfg, self._CoreRegConfigExt)
            core_reg_name = cfg.reg_name
            mem_data = self.core_map[core_reg_name]
            val = cfg.ctype.from_buffer_copy(mem_data)
            result = self.Result(
                val=val.value,
                raw=mem_data,
                descr=cfg.reg.get_descr(value=mem_data, verbose=cfg.verbose))
            results[cfg.name] = result

        for cfg in self.config_core_reg_bits:
            assert isinstance(cfg, self._CoreRegBitsConfigExt)
            core_reg_name = cfg.reg_name
            mem_data = self.core_map[core_reg_name]
            result = self.Result(
                val=cfg.bits.get_value(mem_data),
                raw=mem_data,
                descr=cfg.bits.get_descr(reg_value=mem_data, verbose=cfg.verbose))
            results[cfg.name] = result

        return results
