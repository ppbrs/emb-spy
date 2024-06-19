"""
Dataclass storing information about bit sets within registers, e.g. RCC_APB1ENR.USART5EN.
"""
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass
class Bits:
    """A set of bits, within a register, aka subregister, aka submmreg."""
    # TODO: rename to bits

    name: str
    """Name, e.g. USART5EN."""
    bits: list[int]
    """List of bits from the least significant to the most significant, e.g. [3, 4, 5]."""
    descr: str | None
    """Human-readable description of the set of bits."""
    descr_vals: dict[int, str]
    """Human-readable description of possible values."""

    def __init__(self,
                 name: str,
                 bits: int | Iterable[int],
                 descr: str | None = None,
                 descr_vals: dict[int, str] | None = None) -> None:
        """
        Create a set of bits.

        : param bits :
            Integer, e.g. bits=30, means that the subregister consists of one bit only.
            List of integers, e.g. bits=[15, 16], means that the subregister has several
            bits, starting from the least significant bit.
            A generator, e.g. range(8, 16), can be used to create a list.
        """
        self.bits = self._bits_checked(bits)

        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if len(name) == 0:
            raise ValueError("Name cannot be blank.")
        self.name = name

        if descr is not None and not isinstance(descr, str):
            raise TypeError("Description must be a string.")
        if descr is not None and len(descr) == 0:
            raise ValueError("Description cannot be blank.")
        self.descr = descr

        descr_vals = {} if descr_vals is None else descr_vals
        if not isinstance(descr_vals, dict):
            raise TypeError("Values description must be a dictionary.")
        for val, descr_ in descr_vals.items():
            if not isinstance(val, int) or not isinstance(descr_, str):
                raise TypeError("Values description must be a mapping from int to str.")
        self.descr_vals = descr_vals

    @staticmethod
    def _bits_checked(bits: int | Iterable[int]) -> list[int]:
        """Check bits argument and return the correct type for the constructor."""
        if isinstance(bits, int):
            if bits > 31:
                raise ValueError("Ony 32-bit registers are supported.")
            if bits < 0:
                raise ValueError("Bit index cannot be negative.")
            return [bits, ]
        if isinstance(bits, Iterable):
            if len(list(bits)) == 0:
                raise ValueError("At least one bit is required.")
            if not all(isinstance(i, int) for i in bits):
                raise TypeError("An iterable of integers is required.")
            if any(i < 0 for i in bits):
                raise ValueError("Bit index cannot be negative.")
            if any(i > 31 for i in bits):
                raise ValueError("Ony 32-bit registers are supported.")
            return sorted(bits)
        raise TypeError(f"Unsupported type of `bits`: {type(bits)}")

    def get_value(self, reg_value: int | bytes) -> int:
        """
        Get bits value for a given register value.
        """
        if isinstance(reg_value, (bytes, bytearray)):
            reg_value = int.from_bytes(reg_value, byteorder="little", signed=False)
        elif not isinstance(reg_value, int):
            raise TypeError("reg_value type must be integer or bytes/bytearray")

        value = 0
        for value_pos, bit_pos in enumerate(self.bits, start=0):
            if reg_value & (1 << bit_pos):
                value |= (1 << value_pos)
        return value

    def get_mask(self, invert: bool = False) -> int:
        """
        Get a bit mask for the bits.

        For example, bits=[0] gives 1 or ((2**32 - 1) - 1) inverted.
        """
        mask = 0
        for bit_pos in self.bits:
            mask |= (1 << bit_pos)
        return mask ^ 0xFFFFFFFF if invert else mask

    def get_reg_value(self, reg_value: int, bits_value: int) -> int:
        """
        Modify bits value in a given register value, then return the resulting register value.
        """
        mask = 0
        for bits_value_pos, bit_pos in enumerate(self.bits, start=0):
            if bits_value & (1 << bits_value_pos):
                mask |= (1 << bit_pos)
        return (reg_value & self.get_mask(invert=True)) | mask

    def get_descr(self, reg_value: int | bytes, verbose: bool = False) -> str:
        """
        Compose a short or vebose human-readable description of bits for a given register value.
        """
        # todo: Rename to get_report or something else, because get_descr is misleading.
        bits_val: int = self.get_value(reg_value=reg_value)
        bits_val_bin: str = format(bits_val, f"#0{2 + len(self.bits)}b")
        res = f"{self.name} = 0x{bits_val:X} = {bits_val_bin} = {bits_val}u."
        if self.descr is not None and verbose:
            bits_str = f"@{self.bits}".replace(" ", "")
            res += f" {self.descr}, {bits_str}."
            if verbose:
                if bits_val in self.descr_vals:
                    res += f"\n{bits_val} = {self.descr_vals[bits_val]}"
        return res
