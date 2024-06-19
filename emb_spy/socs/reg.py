"""
Dataclass storing information about a SoC register, e.g. TIM1_CNT, or SP.
"""
import abc
from dataclasses import dataclass

from emb_spy.socs.bits import Bits


@dataclass
class Reg(abc.ABC):
    """Base class for SoC registers."""

    name: str
    """Case-sensitive name."""
    addr: int | str | None
    """
    Address for a memory-mapped register or a name for a core register.
    Examples: 0xE000ED00 (as integer), "$lr" (as string).
    """
    descr: str | None
    """Human-readable description of the register."""
    comment: str | None
    """Any additional human-readable information."""
    bits: list[Bits]
    """List of bit sets."""

    def __init__(  # pylint: disable=too-many-arguments
            self,
            name: str,
            addr: int | str,
            descr: str | None = None,
            comment: str | None = None,
            bits: list[Bits] | None = None,
    ) -> None:
        """
        Construct a Register.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if len(name) == 0:
            raise ValueError("Name cannot be blank.")
        # TODO: check that there are not dots in name
        self.name = name

        if not isinstance(addr, (int, str)):
            raise TypeError("Address is an integer or a string.")
        self.addr = addr

        if descr is not None and not isinstance(descr, str):
            raise TypeError("Description must be a string.")
        if descr is not None and len(descr) == 0:
            raise ValueError("Description cannot be blank.")
        self.descr = descr

        if comment is not None and not isinstance(comment, str):
            raise TypeError("Comment must be a string.")
        if comment is not None and len(comment) == 0:
            raise ValueError("Comment cannot be blank.")
        self.comment = comment

        self.bits = [] if bits is None else bits

    def get_descr(self, value: int | bytes, verbose: bool = False) -> str:
        """
        Return a short or a vebose human-readable string with register description and values.
        """
        if isinstance(value, (bytes, bytearray)):
            value = int.from_bytes(value, byteorder="little", signed=False)
        elif not isinstance(value, int):
            raise TypeError("value type must be integer or bytes/bytearray")

        # Line 1
        value_bin = format(value, "#032b")
        value_bin = (value_bin[:-24] + "_" + value_bin[-24:-16] + "_" + value_bin[-16:-8] + "_"
                     + value_bin[-8:])
        res = f"{self.name} = 0x{value:08X} = {value_bin} = {value}u."
        if self.descr is not None and verbose:
            res += f" {self.descr}"
            if isinstance(self.addr, int):
                res += f" @[0x{self.addr:08X}]."
            elif isinstance(self.addr, str):
                res += f" @[{self.addr}]."
            elif self.addr is None:
                res += " @[None]."
            else:
                raise ValueError
        # Line 2
        if self.comment is not None and verbose:
            res += f"\n{self.comment}"
        # Lines 3...
        for register_bit in self.bits:
            res += ("\n" + register_bit.get_descr(reg_value=value, verbose=verbose))
        return res


# @dataclass
class CoreReg(Reg):  # pylint: disable=too-few-public-methods
    """Core register."""


# @dataclass
class MmapReg(Reg):  # pylint: disable=too-few-public-methods
    """Memory-mapped register."""
