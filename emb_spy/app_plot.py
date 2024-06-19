#!/usr/bin/python3
"""

"""
# Standard library imports
import ctypes
from dataclasses import dataclass, field
import logging
import pathlib
import os
import time
# Third party imports
import elftools.elf.elffile
import matplotlib.pyplot as plt
# Local application/library imports
from .backend import Backend
# from mmreg.arm.armv7e_m.stm32h7.stm32h743 import STM32H743
from emb_spy.socs.arm.armv6_m.stm32f0.stm32f051 import STM32F051


HOST, PORT = "localhost", 4444


# ELF_PATH = pathlib.PosixPath("/home/boris/projects/emb1.wt0/bin/stm32f051_sbx.elf")
# ELF_PATH = pathlib.PosixPath("/home/boris/projects/emb1.wt0/bin/stm32h743_sbx.elf")
ELF_PATH = pathlib.PosixPath("/home/boris/projects/fw7.wt2/bin/serpens_application.elf")

TIME = 1.0
# todo: add timebase


@dataclass
class SymbolConf:
    name: str
    ctype: int
    # offset
    addr: int | None = field(default=None)


@dataclass
class MMRegConf:
    name: str
    ctype: int
    # offset bits and mask
    addr: int | None = field(default=None)


@dataclass
class SymbolInfo:
    addr: int
    size: int


CONFIG: list = [
    # SymbolConf(name="_ZN6sensor12_GLOBAL__N_126systemTemperaturesCriticalE", ctype=ctypes.c_uint32),

    # SymbolConf(name="_ZN12_GLOBAL__N_126highResolutionClockSecondsE", ctype=ctypes.c_uint32),
    # SymbolConf(name="_ZN12_GLOBAL__N_118steadyClockSecondsE", ctype=ctypes.c_uint32),
    # SymbolConf(name="_ZN4tick10sysTickCntE", ctype=ctypes.c_uint32),
    # SymbolConf(name="xTickCount", ctype=ctypes.c_uint32),

    MMRegConf(name="TIM3_CNT", ctype=ctypes.c_uint32)

]


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    # Parse elf file to get all symbols from it.
    with open(ELF_PATH, 'rb') as bin_file:
        symbols: dict[str, SymbolInfo] = {}
        elf_file = elftools.elf.elffile.ELFFile(bin_file)
        for section in elf_file.iter_sections(type="SHT_SYMTAB"):
            # logging.debug("section %s", section.name)
            for symbol in section.iter_symbols():
                symbol_info = SymbolInfo(addr=symbol["st_value"], size=symbol["st_size"])
                symbols[symbol.name] = symbol_info
                # logging.debug("symbol %s %s", symbol.name, symbol_info)

    regs_dict_name = STM32H743().map_name()

    # Check and enhance the configuration
    for item_conf in CONFIG:
        assert isinstance(item_conf, SymbolConf) or isinstance(item_conf, MMRegConf)
        if isinstance(item_conf, SymbolConf):
            assert item_conf.name in symbols
            symbol_info = symbols[item_conf.name]
            item_conf.addr = symbol_info.addr
            # todo: check size
        elif isinstance(item_conf, MMRegConf):
            assert item_conf.name in regs_dict_name
            item_conf.addr = regs_dict_name[item_conf.name].addr
        else:
            raise ValueError

    # collect values
    values_raw: dict[str, list[tuple[float, int]]] = {conf.name: [] for conf in CONFIG}

    with Backend(host=HOST, port=PORT) as backend:
        logging.info("Start capturing.")
        t_0 = time.monotonic()
        t_deadline = t_0 + TIME
        while time.monotonic() < t_deadline:
            for symbol_conf in CONFIG:
                t = time.monotonic() - t_0
                val = backend.read_register(addr=symbol_conf.addr)
                values_raw[symbol_conf.name].append((t, val))
        num_vals = len(values_raw[CONFIG[0].name])
        num_vals_per_s = num_vals / TIME
        logging.info(f"Done capturing. ({num_vals} values, {num_vals_per_s} values per second)")

    # logging.debug("%s", values_raw)

    # post-process values
    pass

    # plot
    logging.getLogger().setLevel(logging.INFO)
    fig = plt.figure(os.path.basename(__file__))

    ax1 = fig.add_subplot(1, 1, 1)

    for name, list_of_tuples in values_raw.items():
        t = [x[0] for x in list_of_tuples]
        vals = [x[1] for x in list_of_tuples]
        ax1.plot(t, vals, label="symbol=" + name)
        logging.info(f"{name}:")
        vals_max, vals_min = max(vals), min(vals)
        vals_range = vals_max - vals_min
        vals_mean = sum(vals) / len(vals)
        logging.info(f"{name}: {len(vals)} points, min={vals_min}, max={vals_max}, range={vals_range}, mean={vals_mean}")

    for ax in fig.get_axes():
        ax.grid(True)
        ax.legend(loc='best', fontsize='small')
    plt.show()
