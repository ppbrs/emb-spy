"""
Application that can read and print the contents of multiple registers and/or symbols
from a single MCU connected via OpenOCD.
"""
from __future__ import annotations

# Standard library imports
# Third party imports
# Local application/library imports
from .backend import Backend
from ._app_reader import _AppReader


class AppStaticReader(_AppReader):
    """A class that contains methods of the application."""

    def __call__(self) -> list:

        self.logger.debug("App called.")

        with Backend(
                host=self.host, port=self.port, target_name=self.target_name,
                logger_suffix=self.logger_suffix, start_if_reset=self.start_if_reset) as backend:
            for reg_data in self.regs_data:
                reg_data.val = backend.read_register(addr=reg_data.register.addr)
            for s_data in self.syms_data:
                s_data.val = backend.read_memory(addr=s_data.addr, ctype=s_data.ctype)

        res = {}
        print()
        for reg_data in self.regs_data:
            if reg_data.sub_register is None:
                reg_str = reg_data.register.get_str(
                    value=reg_data.val,
                    verbose=reg_data.verbose
                )
                print(f"{reg_str}\n")
            else:
                sub_reg_str = reg_data.sub_register.get_str(reg_value=reg_data.val, verbose=reg_data.verbose)
                print(f"{reg_data.register.name}.{sub_reg_str}\n")

        print()
        for s_data in self.syms_data:
            print(f"{s_data.name} = {s_data.val} / 0x{s_data.val:x} ({s_data.ctype})")
            res[s_data.name] = s_data.val

        return res
