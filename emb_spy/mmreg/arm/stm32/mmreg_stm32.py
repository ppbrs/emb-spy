
from emb_spy.mmreg.registers_if import Register, RegisterBits  # pylint: disable=import-error


class MmregSTM32():
    """ """

    @classmethod
    def init_gpio(cls, prefix: str, base: int) -> list[Register]:
        moder_values = {
            0: "Input mode",
            1: "General purpose output mode",
            2: "Alternate function mode",
            3: "Analog mode (reset state)", }
        otyper_values = {
            0: "Output push-pull (reset state)",
            1: "Output open-drain", }
        pupdr_values = {
            0: "No pull-up, pull-down",
            1: "Pull-up",
            2: "Pull-down",
            3: "Reserved", }
        afr_values = {
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
        lck_values = {
            0: "Port configuration not locked",
            1: "Port configuration locked", }
        regs = [
            Register(
                name=f"{prefix}_MODER", addr=(base + 0x00), descr="GPIO port mode register",
                register_bits=[
                    RegisterBits(bits=range(2 * pin, 2 * pin + 2), name=f"MODER{pin}", descr="", values=moder_values)
                    for pin in range(0, 16)
                ]
            ),
            Register(
                name=f"{prefix}_OTYPER", addr=(base + 0x04), descr="GPIO port output type register",
                register_bits=[
                    RegisterBits(bits=range(pin, pin + 1), name=f"OT{pin}", descr="", values=otyper_values)
                    for pin in range(0, 16)
                ]
            ),

            # GPIO port output speed register (GPIOx_OSPEEDR)
            # (x = A to K)
            # Address offset: 0x08
            # 00: Low speed
            # 01: Medium speed
            # 10: High speed
            # 11: Very high speed

            Register(
                name=f"{prefix}_PUPDR", addr=(base + 0x0C), descr="GPIO port pull-up/pull-down register",
                register_bits=[
                    RegisterBits(bits=range(2 * pin, 2 * pin + 2), name=f"PUPDR{pin}", descr="", values=pupdr_values)
                    for pin in range(0, 16)
                ]
            ),
            Register(
                name=f"{prefix}_IDR", addr=(base + 0x10), descr="GPIO port input data register",
                register_bits=[
                    RegisterBits(bits=range(pin, pin + 1), name=f"IDR{pin}", descr="", values={})
                    for pin in range(0, 16)
                ]
            ),
            Register(
                name=f"{prefix}_ODR", addr=(base + 0x14), descr="GPIO port output data register",
                register_bits=[
                    RegisterBits(bits=range(pin, pin + 1), name=f"ODR{pin}", descr="", values={})
                    for pin in range(0, 16)
                ]
            ),
            Register(
                name=f"{prefix}_BSRR", addr=(base + 0x18), descr="GPIO port bit set/reset register",
                register_bits=(
                    [RegisterBits(bits=pin, name=f"BS{pin}", descr=f"Port {prefix} set I/O pin {pin}", values={}) for pin in range(0, 16)]
                    + [RegisterBits(bits=(16 + pin), name=f"BR{pin}", descr=f"Port {prefix} reset I/O pin {pin}", values={}) for pin in range(0, 16)])
            ),
            Register(
                name=f"{prefix}_LCKR", addr=(base + 0x1C), descr="GPIO port configuration lock register",
                register_bits=(
                    [RegisterBits(
                        bits=16, name="LCKK", descr="Lock key",
                        values={
                            0: "Port configuration lock key not active",
                            1: "Port configuration lock key active. The GPIOx_LCKR register is locked until the next MCU reset or peripheral reset.", })]
                    + [RegisterBits(bits=pin, name=f"LCK{pin}", descr=f"Port {prefix} lock I/O pin {pin}", values=lck_values) for pin in range(0, 16)])
            ),
            Register(
                name=f"{prefix}_AFRL", addr=(base + 0x20), descr="GPIO alternate function low register",
                register_bits=[
                    RegisterBits(bits=range(4 * pin, 4 * pin + 4), name=f"AFRR{pin}", descr="", values=afr_values)
                    for pin in range(0, 8)
                ]
            ),
            Register(
                name=f"{prefix}_AFRH", addr=(base + 0x24), descr="GPIO alternate function high register",
                register_bits=[
                    RegisterBits(bits=range(4 * pin, 4 * pin + 4), name=f"AFR{pin + 8}", descr="", values=afr_values)
                    for pin in range(0, 8)
                ]
            ),
        ]
        return regs
