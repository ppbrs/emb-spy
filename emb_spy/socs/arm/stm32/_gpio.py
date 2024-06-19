"""Part of any STM32 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_gpio(
    self: SoC,
    prefix: str,
    base: int
) -> None:
    """Generate all Register objects for GPIO."""
    moder_descr_vals = {
        0: "Input mode",
        1: "General purpose output mode",
        2: "Alternate function mode",
        3: "Analog mode (reset state)", }
    self.append(MmapReg(
        name=f"{prefix}_MODER", addr=(base + 0x00), descr="GPIO port mode register",
        bits=[
            Bits(bits=range(2 * pin, 2 * pin + 2), name=f"MODER{pin}",
                 descr_vals=moder_descr_vals) for pin in range(0, 16)
        ]
    ))

    otyper_descr_vals = {
        0: "Output push-pull (reset state)",
        1: "Output open-drain", }
    self.append(MmapReg(
        name=f"{prefix}_OTYPER", addr=(base + 0x04), descr="GPIO port output type register",
        bits=[
            Bits(bits=range(pin, pin + 1), name=f"OT{pin}",
                 descr_vals=otyper_descr_vals) for pin in range(0, 16)
        ]
    ))

    ospeed_descr_vals = {
        0: "Low speed",
        1: "Medium speed",
        2: "High speed",
        3: "Very high speed", }
    self.append(MmapReg(
        name=f"{prefix}_OSPEEDR", addr=(base + 0x08),
        descr="GPIO port output speed register",
        bits=[
            Bits(bits=range(2 * pin, 2 * pin + 2), name=f"OSPEEDR{pin}",
                 descr_vals=ospeed_descr_vals) for pin in range(0, 16)
        ]
    ))

    pupdr_descr_vals = {
        0: "No pull-up, pull-down",
        1: "Pull-up",
        2: "Pull-down",
        3: "Reserved", }
    self.append(MmapReg(
        name=f"{prefix}_PUPDR", addr=(base + 0x0C),
        descr="GPIO port pull-up/pull-down register",
        bits=[
            Bits(bits=range(2 * pin, 2 * pin + 2), name=f"PUPDR{pin}",
                 descr_vals=pupdr_descr_vals) for pin in range(0, 16)
        ]
    ))

    self.append(MmapReg(
        name=f"{prefix}_IDR", addr=(base + 0x10),
        descr="GPIO port input data register",
        bits=[Bits(bits=range(pin, pin + 1), name=f"IDR{pin}") for pin in range(0, 16)]
    ))

    self.append(MmapReg(
        name=f"{prefix}_ODR", addr=(base + 0x14),
        descr="GPIO port output data register",
        bits=[Bits(bits=range(pin, pin + 1), name=f"ODR{pin}") for pin in range(0, 16)]
    ))

    self.append(MmapReg(
        name=f"{prefix}_BSRR", addr=(base + 0x18), descr="GPIO port bit set/reset register",
        bits=([Bits(
            bits=pin, name=f"BS{pin}", descr=f"Port {prefix} set I/O pin {pin}",
            descr_vals={}) for pin in range(0, 16)]
            + [Bits(
                bits=(16 + pin), name=f"BR{pin}",
                descr=f"Port {prefix} reset I/O pin {pin}",
                descr_vals={}) for pin in range(0, 16)])
    ))

    lck_descr_vals = {
        0: "Port configuration not locked",
        1: "Port configuration locked", }
    lckr_bits = [Bits(
        bits=pin, name=f"LCK{pin}", descr=f"Port {prefix} lock I/O pin {pin}",
        descr_vals=lck_descr_vals) for pin in range(0, 16)]
    lckr_bits.append(Bits(
        bits=16, name="LCKK", descr="Lock key",
        descr_vals={
            0: "Port configuration lock key not active",
            1: "Port configuration lock key active. The GPIOx_LCKR register is locked "
               "until the next MCU reset or peripheral reset."}))
    self.append(MmapReg(
        name=f"{prefix}_LCKR", addr=(base + 0x1C),
        descr="GPIO port configuration lock register", bits=lckr_bits
    ))

    afr_descr_vals = {
        0b0000: "AF0",
        0b0001: "AF1",
        0b0010: "AF2",
        0b0011: "AF3",
        0b0100: "AF4",
        0b0101: "AF5",
        0b0110: "AF6",
        0b0111: "AF7",
        0b1000: "AF8",
        0b1001: "AF9",
        0b1010: "AF10",
        0b1011: "AF11",
        0b1100: "AF12",
        0b1101: "AF13",
        0b1110: "AF14",
        0b1111: "AF15", }
    self.append(MmapReg(
        name=f"{prefix}_AFRL", addr=(base + 0x20),
        descr="GPIO alternate function low register",
        bits=[
            Bits(bits=range(4 * pin, 4 * pin + 4), name=f"AFR{pin}",
                 descr_vals=afr_descr_vals) for pin in range(0, 8)
        ]))
    self.append(MmapReg(
        name=f"{prefix}_AFRH", addr=(base + 0x24),
        descr="GPIO alternate function high register",
        bits=[
            Bits(bits=range(4 * pin, 4 * pin + 4), name=f"AFR{pin + 8}",
                 descr_vals=afr_descr_vals) for pin in range(0, 8)
        ]))
