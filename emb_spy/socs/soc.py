"""
A class storing information about a SoC (System-on-Chip).
"""
from __future__ import annotations

import abc
from collections.abc import Iterable
from dataclasses import dataclass, field

from emb_spy.socs.reg import Reg


@dataclass
class SoC(abc.ABC):
    """The base class for all SoCs (Systems-on-Chip)."""

    _regs: list[Reg] = field(default_factory=lambda: [])

    def append(self, reg: Reg) -> SoC:
        """Add a regster to the SoC."""
        if not issubclass(type(reg), Reg):
            raise TypeError("Cannot append an object of this type.")
        if reg.name in self.names():
            raise ValueError(f"Register with this name ({reg.name}) is already there.")
        self._regs.append(reg)
        return self

    def __iadd__(self, regs: Iterable[Reg]) -> SoC:
        """Add a bunch of registers to the SoC."""
        for reg in regs:
            self.append(reg)
        return self

    def extend(self, regs: Iterable[Reg]) -> SoC:
        """Add a bunch of registers to the SoC."""
        self += regs
        return self

    def __add__(self, regs: Iterable[Reg]) -> SoC:
        """Add a bunch of registers to the SoC."""
        soc = self
        soc += regs
        return soc

    def names(self) -> list[str]:
        """Return the list of names of all Reg objects."""
        return [reg.name for reg in self._regs]

    @property
    def regs(self) -> list[Reg]:
        """Return the list of all Reg objects."""
        return self._regs
        # TODO: rename to registers

    def map_name(self) -> dict[str, Reg]:
        """Return a mapping of names of Registers to Registers themselves."""
        return {reg.name: reg for reg in self._regs}

    def map_address(self) -> dict[int | str, Reg]:
        """Return a mapping of addresses of Registers to Registers themselves."""
        return {reg.addr: reg for reg in self._regs}
