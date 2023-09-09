"""Local module for STM32H743 Advanced Control Timers 1 and 8."""
# Disabling line-too-long because it's impossible to keep human-readable descriptions short.
# pylint: disable=line-too-long

from emb_spy.mmreg.registers_if import Register, Registers, RegisterBits  # pylint: disable=import-error


class _Tim1Tim8(Registers):

    TIM1_BASE = 0x40010000
    TIM8_BASE = 0x40010400

    def __init__(self):
        self.regs = []

        for pref, base in zip(["TIM1_", "TIM8_"], [self.TIM1_BASE, self.TIM8_BASE]):
            self.regs += [
                Register(
                    name=(pref + "CR1"), addr=(base + 0x00), descr="TIMx control register 1",
                    register_bits=[
                        # ...
                        RegisterBits(bits=range(8, 10), name="CKD", descr="Clock division"),
                        # ...
                        RegisterBits(bits=0, name="CEN", descr="Counter enable"),
                    ]
                ),
                Register(
                    name="CR2", addr=(base + 0x04), descr="TIMx control register 2",
                ),
                Register(
                    name=(pref + "CNT"), addr=(base + 0x24), descr="TIMx counter",
                    register_bits=[
                        RegisterBits(bits=31, name="UIFCPY", descr="UIF copy"),
                        RegisterBits(bits=range(0, 16), name="CNT", descr="Counter value"),
                    ]
                ),
                Register(
                    name=(pref + "PSC"), addr=(base + 0x28), descr="TIMx prescaler",
                    register_bits=[
                        RegisterBits(bits=range(0, 16), name="PSC", descr="Prescaler value"),
                    ]
                ),
                Register(
                    name=(pref + "ARR"), addr=(base + 0x2C), descr="TIMx auto-reload register",
                    register_bits=[
                        RegisterBits(bits=range(0, 16), name="ARR", descr="Auto-reload value"),
                    ]
                ),
                Register(
                    name=(pref + "CCR1"), addr=(base + 0x34), descr="TIMx capture/compare register 1",
                    register_bits=[
                        RegisterBits(bits=range(0, 16), name="CCR1", descr="Capture/Compare 1 value"),
                    ]
                ),
                Register(
                    name=(pref + "CCR2"), addr=(base + 0x38), descr="TIMx capture/compare register 2",
                    register_bits=[
                        RegisterBits(bits=range(0, 16), name="CCR2", descr="Capture/Compare 2 value"),
                    ]
                ),
                Register(
                    name=(pref + "CCR3"), addr=(base + 0x3C), descr="TIMx capture/compare register 3",
                    register_bits=[
                        RegisterBits(bits=range(0, 16), name="CCR3", descr="Capture/Compare 3 value"),
                    ]
                ),
                Register(
                    name=(pref + "CCR4"), addr=(base + 0x40), descr="TIMx capture/compare register 4",
                    register_bits=[
                        RegisterBits(bits=range(0, 16), name="CCR4", descr="Capture/Compare 4 value"),
                    ]
                ),
                Register(
                    name=(pref + "BDTR"), addr=(base + 0x44), descr="TIMx break and dead-time register",
                    register_bits=[
    # Bit 25 BK2P: Break 2 polarity
    # Bit 24 BK2E: Break 2 enable
    # Bits 23:20 BK2F[3:0]: Break 2 filter
    # Bits 19:16 BKF[3:0]: Break filter
    # Bit 15 MOE: Main output enable
    # Bit 14 AOE: Automatic output enable
    # Bit 13 BKP: Break polarity
    # Bit 12 BKE: Break enable
    # Bit 11 OSSR: Off-state selection for Run mode
    # Bit 10 OSSI: Off-state selection for Idle mode
    # Bits 9:8 LOCK[1:0]: Lock configuration
                        RegisterBits(bits=range(0, 8), name="DTG", descr="Dead-time generator setup"),
                    ]
                ),
            ]
