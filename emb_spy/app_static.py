"""
Application that can read and print the contents of multiple registers from
an MCU connected via OpenOCD.
"""

from .mmreg.registers_if import Registers
from .backend import Backend


class AppStatic:
    """ A class that contains methods of the application.
    """

    def __init__(self, config: dict[str, dict], host: str, port: int, registers: Registers):
        self.config = config
        self.host = host
        self.port = port
        self.registers = registers

    def __call__(self):

        regs_dict_name = self.registers.get_dict_name()

        reg_addrs: list[int] = [reg.addr for reg_name, reg in regs_dict_name.items()
                                if reg_name in self.config.keys()]
        if not reg_addrs:
            print("There is nothing to read.")
            return

        with Backend(host=self.host, port=self.port) as backend:
            # print(f"Connected to backend; reading {reg_addrs}")
            reg_vals = backend.read_registers(addrs=reg_addrs)
            # print(reg_vals)

        for reg_name, reg_config in self.config.items():
            addr = regs_dict_name[reg_name].addr
            if reg_config is None:
                reg_config = {}
            reg_str = regs_dict_name[reg_name].get_str(value=reg_vals[addr], **reg_config)
            # print(reg_str, "\n")
            print(reg_str)
