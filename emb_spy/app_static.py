"""
Application that can read and print the contents of multiple registers from
a single MCU connected via OpenOCD.
"""

# Standard library imports
import logging
# Third party imports
# Local application/library imports
from .backend import Backend
from .mmreg.registers_if import Registers


class AppStatic:
    """A class that contains methods of the application."""

    def __init__(self,
                 config: dict[str, dict],
                 registers: Registers,
                 host: str, port: int, target_name: str | None = None,
                 logger_suffix: str | None = None
                 ):
        """
        :param logger_suffix: Optional suffix for the logger name.
        """
        self.logger = logging.getLogger(
            self.__class__.__name__ + ("" if logger_suffix is None else logger_suffix))
        self.config = config
        self.host = host
        self.port = port
        self.target_name = target_name
        self.logger_suffix = logger_suffix
        self.registers = registers

    def __call__(self):

        self.logger.debug("App called.")
        regs_dict_name = self.registers.get_dict_name()

        reg_addrs: list[int] = [reg.addr for reg_name, reg in regs_dict_name.items()
                                if reg_name in self.config.keys()]
        if not reg_addrs:
            self.logger.warning("There is nothing to read.")
            return

        with Backend(host=self.host, port=self.port, target_name=self.target_name,
                     logger_suffix=self.logger_suffix) as backend:
            # self.logger.debug(f"Connected to backend; reading {reg_addrs}")
            reg_vals = backend.read_registers(addrs=reg_addrs)
            # self.logger.debug(reg_vals)

        print()
        for reg_name, reg_config in self.config.items():
            addr = regs_dict_name[reg_name].addr
            if reg_config is None:
                reg_config = {}
            reg_str = regs_dict_name[reg_name].get_str(value=reg_vals[addr], **reg_config)
            # print(reg_str, "\n")
            print(reg_str)
