"""
Tests of collections of memory-mapped registers.
"""

import pytest

from emb_spy.socs.reg import CoreReg, MmapReg, Reg
from emb_spy.socs.soc import SoC


def test_soc() -> None:
    """Check basic functions of SoC."""
    reg1 = MmapReg(name="name1", addr=1)
    reg2 = MmapReg(name="name2", addr=2)
    reg3 = CoreReg(name="name3", addr=3)
    reg3 = CoreReg(name="name3", addr=3)
    # Check append().
    soc = SoC()
    assert isinstance(soc.regs, list) and not soc.regs
    soc.append(reg1).append(reg2).append(reg3)
    with pytest.raises(TypeError):
        soc.append(0)
    with pytest.raises(ValueError):
        soc.append(MmapReg(name="name2", addr=2))
    assert len(soc.regs) == 3
    assert set(soc.names()) == {"name1", "name2", "name3"}
    assert set(soc.map_name().keys()) == {"name1", "name2", "name3"}
    assert soc.map_name()[reg1.name] == reg1
    assert set(soc.map_address().keys()) == {1, 2, 3}
    assert soc.map_address()[reg2.addr] == reg2
    # Check iadd().
    soc = SoC()
    soc += [reg1, reg2, reg3]
    assert set(soc.names()) == {"name1", "name2", "name3"}
    with pytest.raises(TypeError):
        soc += 1
    # Check add().
    soc = SoC()
    soc = soc + [reg1, reg2, reg3]
    assert set(soc.names()) == {"name1", "name2", "name3"}
    with pytest.raises(TypeError):
        soc = soc + 1
    # Check extend().
    soc = SoC()
    soc.extend([reg1, reg2, reg3])
    assert set(soc.names()) == {"name1", "name2", "name3"}
    with pytest.raises(TypeError):
        soc.extend(1)


def check_soc(soc: SoC) -> None:
    """
    Sanity checking a collection of registers.
    """
    regs: list[Reg] = soc.regs
    assert soc.regs, "The SoC is empty."
    for reg in regs:
        assert issubclass(type(reg), Reg)
        assert isinstance(reg, (CoreReg, MmapReg)), \
            f"SoC contains {type(reg)} instance: `{reg.name}`."

    map_name: dict[str, Reg] = soc.map_name()
    assert map_name, "The SoC is empty."
    assert len(regs) == len(map_name)
    assert isinstance(map_name, dict)
    for name, reg in map_name.items():
        assert isinstance(name, str)
        assert issubclass(type(reg), Reg)
        assert isinstance(reg, (CoreReg, MmapReg)), \
            f"SoC contains {type(reg)} instance: `{reg.name}`."

    map_address: dict[int | str, Reg] = soc.map_address()
    assert map_address, "The SoC is empty."
    assert isinstance(map_address, dict)
    for addr, reg in map_address.items():
        assert isinstance(addr, (int | str))
        assert issubclass(type(reg), Reg)
        assert isinstance(reg, (CoreReg, MmapReg)), \
            f"SoC contains {type(reg)} instance: `{reg.name}`."
