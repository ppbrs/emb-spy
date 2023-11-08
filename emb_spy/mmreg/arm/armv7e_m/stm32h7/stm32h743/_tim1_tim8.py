"""Local module for STM32H743 Advanced Control Timers 1 and 8."""
# Disabling line-too-long because it's impossible to keep human-readable descriptions short.
# pylint: disable=line-too-long
# pycodestyle: ignore=E501

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
                        RegisterBits(bits=11, name="UIFREMAP", descr="UIF status bit remapping"),
                        RegisterBits(bits=range(8, 11), name="CKD", descr="Clock division"),
                        RegisterBits(bits=7, name="ARPE", descr="Auto-reload preload enable", values={
                            0: "TIMx_ARR register is not buffered",
                            1: "TIMx_ARR register is buffered"}),
                        RegisterBits(bits=range(5, 6), name="CMS", descr="Center-aligned mode selection", values={
                            0b00: "Edge-aligned mode. The counter counts up or down depending on the direction bit (DIR)."}),
                        RegisterBits(bits=4, name="DIR", descr="Direction", values={
                            0: "Counter used as upcounter", 1: "Counter used as downcounter"}),
                        RegisterBits(bits=3, name="OPM", descr="One pulse mode"),
                        RegisterBits(bits=2, name="URS", descr="Update request source", values={
                            1: "Only counter overflow/underflow generates an update interrupt or DMA request if enabled."}),
                        RegisterBits(bits=1, name="UDIS", descr="Update disable"),
                        RegisterBits(bits=0, name="CEN", descr="Counter enable"),
                    ]
                ),
                Register(
                    name=(pref + "CR2"), addr=(base + 0x04), descr="TIMx control register 2",
                    register_bits=[
                        RegisterBits(bits=range(20, 24), name="MMS2", descr="Master mode selection 2 (TRGO2)", values={
                            0b0000: "Reset - the UG bit from the TIMx_EGR register is used as trigger output (TRGO2).",
                            0b0001: "Enable - the Counter Enable signal CNT_EN is used as trigger output (TRGO2).",
                            0b0010: "Update - the update event is selected as trigger output (TRGO2). For instance, a master timer can then be used as a prescaler for a slave timer.",
                            0b0011: "Compare pulse - the trigger output sends a positive pulse when the CC1IF flag is to be set (even if it was already high), as soon as a capture or compare match occurs (TRGO2).",
                            0b0100: "Compare - OC1REFC signal is used as trigger output (TRGO2)",
                            0b0101: "Compare - OC2REFC signal is used as trigger output (TRGO2)",
                            0b0110: "Compare - OC3REFC signal is used as trigger output (TRGO2)",
                            0b0111: "Compare - OC4REFC signal is used as trigger output (TRGO2)",
                            0b1000: "Compare - OC5REFC signal is used as trigger output (TRGO2)",
                            0b1001: "Compare - OC6REFC signal is used as trigger output (TRGO2)",
                            0b1010: "Compare Pulse - OC4REFC rising or falling edges generate pulses on TRGO2",
                            0b1011: "Compare Pulse - OC6REFC rising or falling edges generate pulses on TRGO2",
                            0b1100: "Compare Pulse - OC4REFC or OC6REFC rising edges generate pulses on TRGO2",
                            0b1101: "Compare Pulse - OC4REFC rising or OC6REFC falling edges generate pulses on TRGO2",
                            0b1110: "Compare Pulse - OC5REFC or OC6REFC rising edges generate pulses on TRGO2",
                            0b1111: "Compare Pulse - OC5REFC rising or OC6REFC falling edges generate pulses on TRGO2", }),
                        RegisterBits(bits=range(4, 7), name="MMS", descr="Master mode selection (TRGO)", values={
                            0b000: "Reset - the UG bit from the TIMx_EGR register is used as trigger output (TRGO).",
                            0b001: "Enable - the Counter Enable signal CNT_EN is used as trigger output (TRGO).",
                            0b010: "Update - The update event is selected as trigger output (TRGO).",
                            0b011: "Compare Pulse - The trigger output send a positive pulse when the CC1IF flag is to be set as soon as a capture or a compare match occurred. (TRGO).",
                            0b100: "Compare - OC1REFC signal is used as trigger output (TRGO)",
                            0b101: "Compare - OC2REFC signal is used as trigger output (TRGO)",
                            0b110: "Compare - OC3REFC signal is used as trigger output (TRGO)",
                            0b111: "Compare - OC4REFC signal is used as trigger output (TRGO)", }),
                        RegisterBits(bits=3, name="CCDS", descr="Capture/compare DMA selection", values={}),
                        RegisterBits(bits=2, name="CCUS", descr="Capture/compare control update selection", values={}),
                        RegisterBits(bits=0, name="CCPC", descr="Capture/compare preloaded control", values={
                            0: "CCxE, CCxNE and OCxM bits are not preloaded",
                            1: "CCxE, CCxNE and OCxM bits are preloaded, after having been written, they are updated only when a commutation event (COM) occurs", }),
                    ]
                ),
                Register(
                    name=(pref + "SMCR"), addr=(base + 0x08), descr="TIMx slave mode control register",
                    register_bits=[
                        RegisterBits(bits=[0, 1, 2, 16], name="SMS", descr="Slave mode selection", values={
                            0b0000: "Slave mode disabled",
                            0b0001: "Encoder mode 1",
                            0b0010: "Encoder mode 2",
                            0b0011: "Encoder mode 3",
                            0b0100: "Reset Mode",
                            0b0101: "Gated Mode",
                            0b0110: "Trigger Mode",
                            0b0111: "External Clock Mode 1",
                            0b1000: "Combined reset + trigger mode", }),
                    ]
                ),
                Register(
                    name=(pref + "DIER"), addr=(base + 0x0C), descr="DMA/interrupt enable register",
                    register_bits=[
                    ]
                ),
                Register(
                    name=(pref + "SR"), addr=(base + 0x10), descr="TIMx status register",
                    register_bits=[
                        RegisterBits(bits=17, name="CC6IF", descr="Compare 6 interrupt flag"),
                        RegisterBits(bits=16, name="CC5IF", descr="Compare 5 interrupt flag"),
                        RegisterBits(bits=13, name="SBIF", descr="System Break interrupt flag"),
                        RegisterBits(bits=12, name="CC4OF", descr="Capture/Compare 4 overcapture flag"),
                        RegisterBits(bits=11, name="CC3OF", descr="Capture/Compare 3 overcapture flag"),
                        RegisterBits(bits=10, name="CC2OF", descr="Capture/Compare 2 overcapture flag"),
                        RegisterBits(bits=9, name="CC1OF", descr="Capture/Compare 1 overcapture flag"),
                        RegisterBits(bits=8, name="B2IF", descr="Break 2 interrupt flag"),
                        RegisterBits(bits=7, name="BIF", descr="Break interrupt flag"),
                        RegisterBits(bits=6, name="TIF", descr="Trigger interrupt flag"),
                        RegisterBits(bits=5, name="COMIF", descr="COM interrupt flag"),
                        RegisterBits(bits=4, name="CC4IF", descr="Capture/Compare 4 interrupt flag"),
                        RegisterBits(bits=3, name="CC3IF", descr="Capture/Compare 3 interrupt flag"),
                        RegisterBits(bits=2, name="CC2IF", descr="Capture/Compare 2 interrupt flag"),
                        RegisterBits(bits=1, name="CC1IF", descr="Capture/Compare 1 interrupt flag"),
                        RegisterBits(bits=0, name="UIF", descr="Update interrupt flag"),
                    ]
                ),
                Register(
                    name=(pref + "EGR"), addr=(base + 0x14), descr="TIMx event generation register (write only)",
                    register_bits=[
                    ]
                ),
                Register(
                    name=(pref + "CCMR1-input-capture"), addr=(base + 0x18), descr="TIMx capture/compare mode register 1",
                    register_bits=[
                    ]
                ),
                Register(
                    name=(pref + "CCMR1-output-compare"), addr=(base + 0x18), descr="TIMx capture/compare mode register 1",
                    register_bits=[
                        RegisterBits(bits=15, name="OC2CE", descr="Output Compare 2 clear enable"),
                        RegisterBits(bits=[12, 13, 14, 24], name="OC2M", descr="Output Compare 2 mode", values={
                            0b0000: "Frozen",
                            0b0001: "Set channel 1 to active level on match.",
                            0b0010: "Set channel 1 to inactive level on match.",
                            0b0011: "Toggle",
                            0b0100: "Force inactive level",
                            0b0101: "Force active level",
                            0b0110: "PWM mode 1",
                            0b0111: "PWM mode 2",
                            0b1000: "Retriggerable OPM mode 1",
                            0b1001: "Retriggerable OPM mode 2",
                            0b1100: "Combined PWM mode 1",
                            0b1101: "Combined PWM mode 2",
                            0b1110: "Asymmetric PWM mode 1",
                            0b1111: "Asymmetric PWM mode 2", }),
                        RegisterBits(bits=11, name="OC2PE", descr="Output Compare 2 preload enable", values={
                            0: "Preload register on TIMx_CCR2 disabled.",
                            1: "Preload register on TIMx_CCR2 enabled.", }),
                        RegisterBits(bits=10, name="OC2FE", descr="Output Compare 2 fast enable"),
                        RegisterBits(bits=[8, 9], name="CC2S", descr="Capture/Compare 2 selection", values={
                            0b00: "CC1 channel is configured as output",
                            0b01: "CC1 channel is configured as input, IC2 is mapped on TI2",
                            0b10: "CC1 channel is configured as input, IC2 is mapped on TI1",
                            0b11: "CC1 channel is configured as input, IC2 is mapped on TRC.", }),
                        RegisterBits(bits=7, name="OC1CE", descr="Output Compare 1 clear enable"),
                        RegisterBits(bits=[4, 5, 6, 16], name="OC1M", descr="Output Compare 1 mode", values={
                            0b0000: "Frozen",
                            0b0001: "Set channel 1 to active level on match.",
                            0b0010: "Set channel 1 to inactive level on match.",
                            0b0011: "Toggle",
                            0b0100: "Force inactive level",
                            0b0101: "Force active level",
                            0b0110: "PWM mode 1",
                            0b0111: "PWM mode 2",
                            0b1000: "Retriggerable OPM mode 1",
                            0b1001: "Retriggerable OPM mode 2",
                            0b1100: "Combined PWM mode 1",
                            0b1101: "Combined PWM mode 2",
                            0b1110: "Asymmetric PWM mode 1",
                            0b1111: "Asymmetric PWM mode 2", }),
                        RegisterBits(bits=3, name="OC1PE", descr="Output Compare 1 preload enable", values={
                            0: "Preload register on TIMx_CCR1 disabled.",
                            1: "Preload register on TIMx_CCR1 enabled.", }),
                        RegisterBits(bits=2, name="OC1FE", descr="Output Compare 1 fast enable"),
                        RegisterBits(bits=[0, 1], name="CC1S", descr="Capture/Compare 1 selection", values={
                            0b00: "CC1 channel is configured as output",
                            0b01: "CC1 channel is configured as input, IC1 is mapped on TI1",
                            0b10: "CC1 channel is configured as input, IC1 is mapped on TI2",
                            0b11: "CC1 channel is configured as input, IC1 is mapped on TRC.", }),
                    ]
                ),
                Register(
                    name=(pref + "CCMR2-input-capture"), addr=(base + 0x1C), descr="TIMx capture/compare mode register 2",
                    register_bits=[
                    ]
                ),
                Register(
                    name=(pref + "CCMR2-output-compare"), addr=(base + 0x1C), descr="TIMx capture/compare mode register 2",
                    register_bits=[
                    ]
                ),
                Register(
                    name=(pref + "CCER"), addr=(base + 0x20), descr="TIMx capture/compare enable register",
                    register_bits=[
                        RegisterBits(bits=21, name="CC6P", descr="Capture/Compare 6 output polarity", values={}),
                        RegisterBits(bits=20, name="CC6E", descr="Capture/Compare 6 output enable", values={}),
                        RegisterBits(bits=17, name="CC5P", descr="Capture/Compare 5 output polarity", values={}),
                        RegisterBits(bits=16, name="CC5E", descr="Capture/Compare 5 output enable", values={}),
                        RegisterBits(bits=15, name="CC4NP", descr="Capture/Compare 4 complementary output polarity", values={}),
                        RegisterBits(bits=13, name="CC4P", descr="Capture/Compare 4 output polarity", values={}),
                        RegisterBits(bits=12, name="CC4E", descr="Capture/Compare 4 output enable", values={}),
                        RegisterBits(bits=11, name="CC3NP", descr="Capture/Compare 3 complementary output polarity", values={}),
                        RegisterBits(bits=10, name="CC3NE", descr="Capture/Compare 3 complementary output enable", values={}),
                        RegisterBits(bits=9, name="CC3P", descr="Capture/Compare 3 output polarity", values={}),
                        RegisterBits(bits=8, name="CC3E", descr="Capture/Compare 3 output enable", values={}),
                        RegisterBits(bits=7, name="CC2NP", descr="Capture/Compare 2 complementary output polarity", values={}),
                        RegisterBits(bits=6, name="CC2NE", descr="Capture/Compare 2 complementary output enable", values={}),
                        RegisterBits(bits=5, name="CC2P", descr="Capture/Compare 2 output polarity", values={}),
                        RegisterBits(bits=4, name="CC2E", descr="Capture/Compare 2 output enable", values={}),
                        RegisterBits(bits=3, name="CC1NP", descr="Capture/Compare 1 complementary output polarity", values={
                            0: "OC1N active high (output mode).",
                            1: "OC1N active low (output mode).", }),
                        RegisterBits(bits=2, name="CC1NE", descr="Capture/Compare 1 complementary output enable", values={}),
                        RegisterBits(bits=1, name="CC1P", descr="Capture/Compare 1 output polarity", values={
                            0: "OC1 active high (output mode).",
                            1: "OC1 active low (output mode).", }),
                        RegisterBits(bits=0, name="CC1E", descr="Capture/Compare 1 output enable", values={}),
                    ]
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
                # TIMx repetition counter register (TIMx_RCR)(x = 1, 8). Address offset: 0x30
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
                        RegisterBits(bits=25, name="BK2P", descr="Break 2 polarity"),
                        RegisterBits(bits=24, name="BK2E", descr="Break 2 enable"),
                        RegisterBits(bits=range(20, 24), name="BK2F", descr="Break 2 filter"),
                        RegisterBits(bits=range(16, 20), name="BKF", descr="Break filter"),
                        RegisterBits(bits=15, name="MOE", descr="Main output enable", values={
                            0: "OC and OCN outputs are disabled",
                            1: "OC and OCN outputs are enabled if their respective enable bits are set (CCxE, CCxNE in TIMx_CCER register).", }),
                        RegisterBits(bits=14, name="AOE", descr="Automatic output enable", values={
                            0: "MOE can be set only by software",
                            1: "MOE can be set by software or automatically at the next update event (if none of the break inputs BRK and BRK2 is active)", }),
                        RegisterBits(bits=13, name="BKP", descr="Break polarity"),
                        RegisterBits(bits=12, name="BKE", descr="Break enable"),
                        RegisterBits(bits=11, name="OSSR", descr="Off-state selection for Run mode"),
                        RegisterBits(bits=10, name="OSSI", descr="Off-state selection for Idle mode"),
                        RegisterBits(bits=[8, 9], name="LOCK", descr="Lock configuration"),
                        RegisterBits(bits=range(0, 8), name="DTG", descr="Dead-time generator setup"),
                    ]
                ),
            ]
