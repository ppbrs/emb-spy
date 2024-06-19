"""Tests for reg class."""
from typing import Any

import pytest

from emb_spy.socs.reg import Reg
from emb_spy.socs.bits import Bits


def test_reg_init() -> None:
    """Check reg constructor."""
    name: Any
    # Address
    assert Reg(name="n", addr=0).addr == 0
    assert Reg(name="n", addr="r0").addr == "r0"
    for addr in [None, 1.2, ]:
        with pytest.raises(TypeError):
            Reg(name="n", addr=addr)
    # Name
    assert Reg(name="n", addr=0).name == "n"
    for name in [None, 1.2, 0, []]:
        with pytest.raises(TypeError):
            Reg(name=name, addr=0)
    with pytest.raises(ValueError):
        Reg(name="", addr=0)
    # Description
    assert Reg(name="n", addr=0, descr="descr").descr == "descr"
    assert Reg(name="n", addr=0).descr is None
    for descr in [1.2, 0, [], {}]:
        with pytest.raises(TypeError):
            Reg(name="n", addr=0, descr=descr)
    with pytest.raises(ValueError):
        Reg(name="n", descr="", addr=0)
    # Comment
    assert Reg(name="n", addr=0, comment="comment").comment == "comment"
    assert Reg(name="n", addr=0).comment is None
    for comment in [1.2, 0, [], {}]:
        with pytest.raises(TypeError):
            Reg(name="n", addr=0, comment=comment)
    with pytest.raises(ValueError):
        Reg(name="n", comment="", addr=0)
    # Bits
    assert Reg(name="n", addr=0, bits=[]).bits == []
    assert Reg(name="n", addr=0, bits=None).bits == []
    reg = Reg(
        name="n", addr=0,
        bits=[
            Bits(name="b", bits=31)
        ])
    assert len(reg.bits) == 1 and reg.bits[0].name == "b"


def test_reg_descr() -> None:
    """Test get_descr method."""
    reg1 = Reg(name="reg1", addr=1234, descr="descr1")
    assert reg1.get_descr(value=5678, verbose=False) \
        == "reg1 = 0x0000162E = 0b000000_00000000_00010110_00101110 = 5678u."
    assert reg1.get_descr(value=5678, verbose=True) \
        == "reg1 = 0x0000162E = 0b000000_00000000_00010110_00101110 = 5678u. descr1 @[0x000004D2]."

    reg2 = Reg(
        name="reg2", addr=2345, descr="descr2", comment="comment2",
        bits=[
            Bits(name="b0", bits=0, descr="bit0"),
            Bits(name="b1", bits=1, descr="bit1"),
        ])
    short2 = (
        "reg2 = 0x00001A85 = 0b000000_00000000_00011010_10000101 = 6789u.\n"
        "b0 = 0x1 = 0b1 = 1u.\n"
        "b1 = 0x0 = 0b0 = 0u.")
    verbose2 = (
        "reg2 = 0x00001A85 = 0b000000_00000000_00011010_10000101 = 6789u. descr2 @[0x00000929].\n"
        "comment2\n"
        "b0 = 0x1 = 0b1 = 1u. bit0, @[0].\n"
        "b1 = 0x0 = 0b0 = 0u. bit1, @[1].")
    value2 = 6789
    assert reg2.get_descr(value=value2, verbose=False) == short2
    assert reg2.get_descr(value=value2, verbose=True) == verbose2
    value2 = (6789).to_bytes(length=4, byteorder="little", signed=False)
    assert reg2.get_descr(value=value2, verbose=False) == short2
    assert reg2.get_descr(value=value2, verbose=True) == verbose2
