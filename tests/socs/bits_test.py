"""Tests for Bits class."""
import pytest

from emb_spy.socs.bits import Bits


def test_bits_init() -> None:
    """Check Bits constructor."""
    # Integer bits.
    assert Bits(bits=0, name="n").bits == [0]
    assert Bits(bits=31, name="n").bits == [31]
    with pytest.raises(ValueError):
        Bits(bits=32, name="n")
    with pytest.raises(ValueError):
        Bits(bits=-1, name="n")
    # Iterable bits.
    assert Bits(bits=[0, 31], name="n").bits == [0, 31]
    assert Bits(bits={0, 1}, name="n").bits == [0, 1]
    assert Bits(bits=(1, 2), name="n").bits == [1, 2]
    assert Bits(bits=range(29, 32), name="n").bits == [29, 30, 31]
    for bits in [[], [-1, 0], [31, 32], range(-1, 10), range(0, 33), ]:
        with pytest.raises(ValueError):
            Bits(bits=bits, name="n")
    for bits in [["a", "b"], ]:
        with pytest.raises(TypeError):
            Bits(bits=bits, name="n")
    # Wrong type bits.
    for bits in [1.234, None, "bits"]:
        with pytest.raises(TypeError):
            Bits(bits=bits, name="n")
    # Bad name.
    with pytest.raises(ValueError):
        Bits(bits=0, name="")
    # Wrong type name.
    for name in [1, 1.234, None, [1, 2]]:
        with pytest.raises(TypeError):
            Bits(bits=0, name=name)
    # Wrong type descr.
    for descr in [1, 1.234, [1, 2]]:
        with pytest.raises(TypeError):
            Bits(bits=0, name="n", descr=descr)
    # Bad description.
    with pytest.raises(ValueError):
        Bits(bits=0, name="n", descr="")
    # Wrong type descr_vals.
    for descr_vals in [1, 1.234, "str", [1, 2], {1, 2}]:
        with pytest.raises(TypeError):
            Bits(bits=0, name="n", descr_vals=descr_vals)
    # Bad description.
    for descr_vals in [{None: None}, ]:
        with pytest.raises(TypeError):
            Bits(bits=0, name="n", descr_vals=descr_vals)


def test_bits() -> None:
    """Test get_value method."""
    assert Bits(bits=0, name="n").get_value(0b0001) == 1
    assert Bits(bits=1, name="n").get_value(0b0010) == 1
    assert Bits(bits=2, name="n").get_value(0b0100) == 1
    assert Bits(bits=3, name="n").get_value(0b1000) == 1
    # ...
    assert Bits(bits=30, name="n").get_value(0b01000000_00000000_00000000_00000000) == 1
    assert Bits(bits=31, name="n").get_value(0b10000000_00000000_00000000_00000000) == 1

    assert Bits(bits=0, name="n").get_value(0) == 0
    assert Bits(bits=31, name="n").get_value(0) == 0

    assert Bits(bits=[1, 2], name="n").get_value(0b0110) == 3
    assert Bits(bits=[30, 31], name="n").get_value(0b11000000_00000000_00000000_00000000) \
        == 3


def test_bits_mask() -> None:
    """Test get_value method."""
    assert Bits(bits=0, name="n").get_mask() == 0b00000000_00000000_00000000_00000001
    assert Bits(bits=[0, 31], name="n").get_mask() == 0b10000000_00000000_00000000_00000001
    assert Bits(bits=0, name="n").get_mask(invert=True) \
        == 0b11111111_11111111_11111111_11111110
    assert Bits(bits=[0, 31], name="n").get_mask(invert=True) \
        == 0b01111111_11111111_11111111_11111110


def test_bits_modify() -> None:
    """Test get_reg_value method."""
    assert Bits(bits=0, name="n").get_reg_value(reg_value=0b10101010, bits_value=0) \
        == 0b10101010
    assert Bits(bits=0, name="n").get_reg_value(reg_value=0b01010100, bits_value=1) \
        == 0b01010101
    assert Bits(bits=0, name="n").get_reg_value(reg_value=0b11111111, bits_value=0) \
        == 0b11111110
    assert Bits(bits=0, name="n").get_reg_value(reg_value=0b00000001, bits_value=1) \
        == 0b00000001

    assert Bits(bits=[0, 7], name="n").get_reg_value(reg_value=0b11111111, bits_value=0) \
        == 0b01111110
    assert Bits(bits=[0, 7], name="n").get_reg_value(reg_value=0b11111111, bits_value=1) \
        == 0b01111111
    assert Bits(bits=[0, 7], name="n").get_reg_value(reg_value=0b11111111, bits_value=2) \
        == 0b11111110
    assert Bits(bits=[0, 7], name="n").get_reg_value(reg_value=0b11111111, bits_value=3) \
        == 0b11111111


def test_bits_descr() -> None:
    """Test get_descr method."""
    obj = Bits(
        bits=[0, 1,], name="n", descr="descr",
        descr_vals={0: "zero", 1: "one", 2: "two", 3: "three"})
    val1 = 0b01
    val2 = 0b10
    short = obj.get_descr(reg_value=val1, verbose=False)
    verbose = obj.get_descr(reg_value=val2, verbose=True)
    assert short == "n = 0x1 = 0b01 = 1u."
    assert verbose == "n = 0x2 = 0b10 = 2u. descr, @[0,1].\n2 = two"

    short = obj.get_descr(reg_value=val1.to_bytes(length=1, byteorder="little", signed=False), verbose=False)
    verbose = obj.get_descr(reg_value=val2.to_bytes(length=1, byteorder="little", signed=False), verbose=True)
    assert short == "n = 0x1 = 0b01 = 1u."
    assert verbose == "n = 0x2 = 0b10 = 2u. descr, @[0,1].\n2 = two"
