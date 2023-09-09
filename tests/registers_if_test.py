

# Standard library imports
# Third party imports
# Local application/library imports
from emb_spy.mmreg.registers_if import RegisterBits


def test_register_bits():

    # TODO: check for bits greater than 31

    assert RegisterBits(bits=1, name="dummy", values={}).bits_list == [1]
    assert RegisterBits(bits=31, name="dummy", values={}).bits_list == [31]

    assert RegisterBits(bits=[3, 4], name="dummy", values={}).bits_list == [3, 4]

    assert RegisterBits(bits=range(29, 32), name="dummy", values={}).bits_list == [29, 30, 31]

    try:
        RegisterBits(bits=1.234, name="dummy", descr="dummy", values={})
        assert False, "Should fail"
    except TypeError:
        pass
    except Exception as e:
        raise e

    assert RegisterBits(bits=0, name="").get_value(0b0001) == 1
    assert RegisterBits(bits=1, name="").get_value(0b0010) == 1
    assert RegisterBits(bits=2, name="").get_value(0b0100) == 1
    assert RegisterBits(bits=3, name="").get_value(0b1000) == 1
    # ...
    assert RegisterBits(bits=30, name="").get_value(0b01000000_00000000_00000000_00000000) == 1
    assert RegisterBits(bits=31, name="").get_value(0b10000000_00000000_00000000_00000000) == 1

    assert RegisterBits(bits=0, name="").get_value(0) == 0
    assert RegisterBits(bits=31, name="").get_value(0) == 0

    assert RegisterBits(bits=[1, 2], name="").get_value(0b0110) == 3
    assert RegisterBits(bits=[30, 31], name="").get_value(0b11000000_00000000_00000000_00000000) == 3


def test_register_bits_mask():
    assert RegisterBits(bits=0, name="").get_mask() == 0b00000000_00000000_00000000_00000001
    assert RegisterBits(bits=[0, 31], name="").get_mask() == 0b10000000_00000000_00000000_00000001
    assert RegisterBits(bits=0, name="").get_mask(invert=True) == 0b11111111_11111111_11111111_11111110
    assert RegisterBits(bits=[0, 31], name="").get_mask(invert=True) == 0b01111111_11111111_11111111_11111110


def test_register_bits_modify():
    assert RegisterBits(bits=0, name="").get_reg_value(reg_value=0b10101010, bits_value=0) == 0b10101010
    assert RegisterBits(bits=0, name="").get_reg_value(reg_value=0b01010100, bits_value=1) == 0b01010101
    assert RegisterBits(bits=0, name="").get_reg_value(reg_value=0b11111111, bits_value=0) == 0b11111110
    assert RegisterBits(bits=0, name="").get_reg_value(reg_value=0b00000001, bits_value=1) == 0b00000001

    assert RegisterBits(bits=[0, 7], name="").get_reg_value(reg_value=0b11111111, bits_value=0) == 0b01111110
    assert RegisterBits(bits=[0, 7], name="").get_reg_value(reg_value=0b11111111, bits_value=1) == 0b01111111
    assert RegisterBits(bits=[0, 7], name="").get_reg_value(reg_value=0b11111111, bits_value=2) == 0b11111110
    assert RegisterBits(bits=[0, 7], name="").get_reg_value(reg_value=0b11111111, bits_value=3) == 0b11111111
