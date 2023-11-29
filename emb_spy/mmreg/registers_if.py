
# Standard library imports
from dataclasses import dataclass
from collections.abc import Iterable
import abc
# Third party imports
# Local application/library imports


@dataclass
class RegisterBits:
    name: str
    bits_list: list[int]
    """
    List of bits from the lowest to the highest
    """
    descr: str | None
    values: dict[int, str]

    def __init__(self,
                 bits: int | list[int] | Iterable[int],
                 name: str,
                 descr: str | None = None,
                 values: dict[int, str] = {}) -> None:
        if isinstance(bits, int):
            self.bits_list = [bits, ]
        elif isinstance(bits, list) or isinstance(bits, range):
            self.bits_list = list(bits)
            self.bits_list.sort()
        else:
            raise TypeError(f"Unsupported type of `bits`: {type(bits)}")

        self.name = name
        self.descr = descr
        self.values = values

    def get_value(self, reg_value: int) -> int:
        """
        Get bits value for the given register value
        """
        value = 0
        for value_pos, bit_pos in enumerate(self.bits_list, start=0):
            if reg_value & (1 << bit_pos):
                value |= (1 << value_pos)
        return value

    def get_mask(self, invert: bool = False) -> int:
        """
        """
        mask = 0
        for bit_pos in self.bits_list:
            mask |= (1 << bit_pos)
        if invert:
            mask = mask ^ 0xFFFFFFFF
        return mask

    def get_reg_value(self, reg_value: int, bits_value: int) -> int:
        """
        Modify bit value and return resulting register value
        """
        mask = 0
        for bits_value_pos, bit_pos in enumerate(self.bits_list, start=0):
            if bits_value & (1 << bits_value_pos):
                mask |= (1 << bit_pos)
        return (reg_value & self.get_mask(invert=True)) | mask

    def get_str(self, reg_value: int, verbose: bool) -> str:

        bits_val: int = self.get_value(reg_value=reg_value)
        bits_val_bin: str = format(bits_val, f"#0{2 + len(self.bits_list)}b")
        res = f"{self.name} = 0x{bits_val:X} = {bits_val_bin} = {bits_val}u."
        if self.descr is not None and verbose:
            bits_list_str = f"@{self.bits_list}".replace(" ", "")
            res += f" {self.descr}, {bits_list_str}."
            if verbose:
                if bits_val in self.values:
                    res += f"\n\t\t{bits_val} = {self.values[bits_val]}"
        return res


@dataclass
class Register:
    """ A register can be either a memory mapped register or a core register.
    """
    name: str
    """ The name is case sensitive. """
    addr: int | str | None
    """ Examples: 0xE000ED00 (as integer), "$lr" (as string). """
    descr: str | None
    comment: str | None
    register_bits: list[RegisterBits] | None
    # TODO: Add reset value for informational purposes.

    def __init__(self, name: str, addr: int | str | None,
                 descr: str | None = None,
                 comment: str | None = None,
                 register_bits: list[RegisterBits] | None = []) -> None:
        self.name = name
        self.addr = addr
        self.descr = descr
        self.comment = comment
        self.register_bits = register_bits

    def get_str(self, value: int, verbose: bool = False) -> str:
        """
        Prepare a human-readable string with register description and values.
        """

        # print(f"Register({self.name}): get_str({value=})")
        value_bin = format(value, "#032b")
        value_bin = value_bin[:-24] + "_" + value_bin[-24:-16] + "_" + value_bin[-16:-8] + "_" + value_bin[-8:]
        res = f"{self.name} = 0x{value:08X} = {value_bin} = {value}u"
        if self.descr is not None and verbose:
            res += f" = {self.descr}"
            if isinstance(self.addr, int):
                res += f" @[0x{self.addr:08X}]."
            elif isinstance(self.addr, str):
                res += f" @[{self.addr}]."
            elif self.addr is None:
                res += " @[None]."
            else:
                raise ValueError
        else:
            res += "."
        if self.comment is not None and verbose:
            res += f"\n\t{self.comment}"
        for register_bit in self.register_bits:
            res += "\n\t"
            res += register_bit.get_str(reg_value=value, verbose=verbose)
        return res


class Registers(abc.ABC):
    """
    This is the base class for all SOCs.
    """

    __slots__ = ("regs")
    regs: list[Register]

    def get_names(self) -> list[str]:
        """ Return the list of names of all Register objects. """
        return [reg.name for reg in self.regs]

    def get_list(self) -> list[Register]:
        """ Return the list of all Register objects. """
        return self.regs

    def get_dict_name(self) -> dict[str, Register]:
        return {reg.name: reg for reg in self.regs}

    def get_dict_address(self) -> dict[int | str, Register]:
        return {reg.addr: reg for reg in self.regs}
