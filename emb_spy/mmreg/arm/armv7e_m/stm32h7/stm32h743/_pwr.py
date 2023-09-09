"""Local module for STM32H743 Advanced Control Timers 1 and 8."""
# Disabling line-too-long because it's impossible to keep human-readable descriptions short.
# pylint: disable=line-too-long

from emb_spy.mmreg.registers_if import Register, Registers, RegisterBits  # pylint: disable=import-error


class _Pwr(Registers):

    PWR_BASE = 0x58024800

    def __init__(self):
        self.regs = [
            Register(name="PWR_CR1", addr=(self.PWR_BASE + 0x000), descr="PWR control register 1", register_bits=[]),
            Register(name="PWR_CSR1", addr=(self.PWR_BASE + 0x004), descr="PWR control status register 1", register_bits=[]),
            Register(name="PWR_CR2", addr=(self.PWR_BASE + 0x008), descr="PWR control register 2", register_bits=[]),
            Register(
                name="PWR_CR3", addr=(self.PWR_BASE + 0x00C), descr="PWR control register 3",
                register_bits=[
                    # Bit 26 USB33RDY: USB supply ready.
                    # 0: USB33 supply not ready.
                    # 1: USB33 supply ready.
                    # Bit 25 USBREGEN: USB regulator enable.
                    # 0: USB regulator disabled.
                    # 1: USB regulator enabled.
                    # Bit 24 USB33DEN: VDD33USB voltage level detector enable.
                    # Bit 9 VBRS: VBAT charging resistor selection
                    # 0: Charge VBAT through a 5 kΩ resistor.
                    # 1: Charge VBAT through a 1.5 kΩ resistor.
                    # Bit 8 VBE: VBAT charging enable
                    # 0: VBAT battery charging disabled.
                    # 1: VBAT battery charging enabled.
                    RegisterBits(
                        bits=2, name="SCUEN", descr="Supply configuration update enable",
                        values={
                            0: "Supply configuration update locked..",
                            1: "Single write enabled to Supply configuration (LDOEN and BYPASS)",
                        }
                    ),
                    RegisterBits(
                        bits=1, name="LDOEN", descr="Low drop-out regulator enable",
                        values={
                            0: "Low drop-out regulator disabled.",
                            1: "Low drop-out regulator enabled (default)",
                        }
                    ),
                    RegisterBits(
                        bits=0, name="BYPASS", descr="Power management unit bypass",
                        values={
                            0: "Power management unit normal operation.",
                            1: "Power management unit bypassed, voltage monitoring still active.",
                        }
                    ),
                ]
            ),
            Register(name="PWR_CPUCR", addr=(self.PWR_BASE + 0x010), descr="PWR CPU control register", register_bits=[]),
            Register(name="PWR_D3CR", addr=(self.PWR_BASE + 0x018), descr="PWR D3 domain control register", register_bits=[]),
            Register(name="PWR_WKUPCR", addr=(self.PWR_BASE + 0x020), descr="PWR wakeup clear register", register_bits=[]),
            Register(name="PWR_WKUPFR", addr=(self.PWR_BASE + 0x024), descr="PWR wakeup flag register", register_bits=[]),
            Register(name="PWR_WKUPEPR", addr=(self.PWR_BASE + 0x028), descr="PWR wakeup enable and polarity register", register_bits=[]),
        ]
