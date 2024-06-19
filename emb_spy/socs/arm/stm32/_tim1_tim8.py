"""Part of any STM32 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_tim1_tim8(
    self: SoC,
    prefix: str,
    base: int
) -> None:
    """Generate all Register objects for Advanced Control Timers 1 and 8."""
    self.append(MmapReg(
        name=(f"{prefix}_CR1"), addr=(base + 0x00), descr="TIMx control register 1",
        bits=[
            Bits(bits=11, name="UIFREMAP", descr="UIF status bit remapping"),
            Bits(bits=range(8, 11), name="CKD", descr="Clock division"),
            Bits(bits=7, name="ARPE", descr="Auto-reload preload enable", descr_vals={
                0: "TIMx_ARR register is not buffered",
                1: "TIMx_ARR register is buffered"}),
            Bits(
                bits=range(5, 6), name="CMS", descr="Center-aligned mode selection", descr_vals={
                    0b00: "Edge-aligned mode. The counter counts up or down depending "
                          "on the direction bit (DIR)."}),
            Bits(
                bits=4, name="DIR", descr="Direction", descr_vals={
                    0: "Counter used as upcounter", 1: "Counter used as downcounter"}),
            Bits(bits=3, name="OPM", descr="One pulse mode"),
            Bits(bits=2, name="URS", descr="Update request source", descr_vals={
                1: "Only counter overflow/underflow generates an update interrupt or DMA request "
                   "if enabled."}),
            Bits(bits=1, name="UDIS", descr="Update disable"),
            Bits(bits=0, name="CEN", descr="Counter enable"),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_CR2"), addr=(base + 0x04), descr="TIMx control register 2",
        bits=[
            Bits(
                bits=range(20, 24), name="MMS2", descr="Master mode selection 2 (TRGO2)",
                descr_vals={
                    0b0000: "Reset - the UG bit from the TIMx_EGR register is used "
                            "as trigger output (TRGO2).",
                    0b0001: "Enable - the Counter Enable signal CNT_EN is used "
                            "as trigger output (TRGO2).",
                    0b0010: "Update - the update event is selected as trigger output (TRGO2). "
                            "For instance, a master timer can then be used as a prescaler "
                            "for a slave timer.",
                    0b0011: "Compare pulse - the trigger output sends a positive pulse "
                            "when the CC1IF flag is to be set (even if it was already high), "
                            "as soon as a capture or compare match occurs (TRGO2).",
                    0b0100: "Compare - OC1REFC signal is used as trigger output (TRGO2)",
                    0b0101: "Compare - OC2REFC signal is used as trigger output (TRGO2)",
                    0b0110: "Compare - OC3REFC signal is used as trigger output (TRGO2)",
                    0b0111: "Compare - OC4REFC signal is used as trigger output (TRGO2)",
                    0b1000: "Compare - OC5REFC signal is used as trigger output (TRGO2)",
                    0b1001: "Compare - OC6REFC signal is used as trigger output (TRGO2)",
                    0b1010: "Compare Pulse - OC4REFC rising or falling edges generate pulses "
                            "on TRGO2",
                    0b1011: "Compare Pulse - OC6REFC rising or falling edges generate pulses "
                            "on TRGO2",
                    0b1100: "Compare Pulse - OC4REFC or OC6REFC rising edges generate pulses "
                            "on TRGO2",
                    0b1101: "Compare Pulse - OC4REFC rising or OC6REFC falling edges "
                            "generate pulses on TRGO2",
                    0b1110: "Compare Pulse - OC5REFC or OC6REFC rising edges "
                            "generate pulses on TRGO2",
                    0b1111: "Compare Pulse - OC5REFC rising or OC6REFC falling edges generate "
                            "pulses on TRGO2", }),
            Bits(
                bits=range(4, 7), name="MMS", descr="Master mode selection (TRGO)",
                descr_vals={
                    0b000: "Reset - the UG bit from the TIMx_EGR register is used as trigger "
                           "output (TRGO).",
                    0b001: "Enable - the Counter Enable signal CNT_EN is used as trigger "
                           "output (TRGO).",
                    0b010: "Update - The update event is selected as trigger output (TRGO).",
                    0b011: "Compare Pulse - The trigger output send a positive pulse when "
                           "the CC1IF flag is to be set as soon as a capture or a compare match "
                           "occurred. (TRGO).",
                    0b100: "Compare - OC1REFC signal is used as trigger output (TRGO)",
                    0b101: "Compare - OC2REFC signal is used as trigger output (TRGO)",
                    0b110: "Compare - OC3REFC signal is used as trigger output (TRGO)",
                    0b111: "Compare - OC4REFC signal is used as trigger output (TRGO)", }),
            Bits(bits=3, name="CCDS", descr="Capture/compare DMA selection"),
            Bits(bits=2, name="CCUS", descr="Capture/compare control update selection"),
            Bits(
                bits=0, name="CCPC", descr="Capture/compare preloaded control", descr_vals={
                    0: "CCxE, CCxNE and OCxM bits are not preloaded",
                    1: "CCxE, CCxNE and OCxM bits are preloaded, after having been written, "
                       "they are updated only when a commutation event (COM) occurs", }),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_SMCR"), addr=(base + 0x08), descr="TIMx slave mode control register",
        bits=[
            Bits(bits=[0, 1, 2, 16], name="SMS", descr="Slave mode selection", descr_vals={
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
    ))
    self.append(MmapReg(
        name=(f"{prefix}_DIER"), addr=(base + 0x0C), descr="DMA/interrupt enable register",
        bits=[
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_SR"), addr=(base + 0x10), descr="TIMx status register",
        bits=[
            Bits(bits=17, name="CC6IF", descr="Compare 6 interrupt flag"),
            Bits(bits=16, name="CC5IF", descr="Compare 5 interrupt flag"),
            Bits(bits=13, name="SBIF", descr="System Break interrupt flag"),
            Bits(bits=12, name="CC4OF", descr="Capture/Compare 4 overcapture flag"),
            Bits(bits=11, name="CC3OF", descr="Capture/Compare 3 overcapture flag"),
            Bits(bits=10, name="CC2OF", descr="Capture/Compare 2 overcapture flag"),
            Bits(bits=9, name="CC1OF", descr="Capture/Compare 1 overcapture flag"),
            Bits(bits=8, name="B2IF", descr="Break 2 interrupt flag"),
            Bits(bits=7, name="BIF", descr="Break interrupt flag"),
            Bits(bits=6, name="TIF", descr="Trigger interrupt flag"),
            Bits(bits=5, name="COMIF", descr="COM interrupt flag"),
            Bits(bits=4, name="CC4IF", descr="Capture/Compare 4 interrupt flag"),
            Bits(bits=3, name="CC3IF", descr="Capture/Compare 3 interrupt flag"),
            Bits(bits=2, name="CC2IF", descr="Capture/Compare 2 interrupt flag"),
            Bits(bits=1, name="CC1IF", descr="Capture/Compare 1 interrupt flag"),
            Bits(bits=0, name="UIF", descr="Update interrupt flag"),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_EGR"), addr=(base + 0x14),
        descr="TIMx event generation register (write only)", ))
    self.append(MmapReg(
        name=(f"{prefix}_CCMR1_IN"), addr=(base + 0x18),
        descr="TIMx capture/compare mode register 1", ))
    self.append(MmapReg(
        name=(f"{prefix}_CCMR1_OUT"), addr=(base + 0x18),
        descr="TIMx capture/compare mode register 1",
        bits=[
            Bits(bits=15, name="OC2CE", descr="Output Compare 2 clear enable"),
            Bits(bits=[12, 13, 14, 24], name="OC2M", descr="Output Compare 2 mode", descr_vals={
                0b0000: "Frozen",
                0b0001: "Set channel to active level on match.",
                0b0010: "Set channel to inactive level on match.",
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
            Bits(bits=11, name="OC2PE", descr="Output Compare 2 preload enable", descr_vals={
                0: "Preload register on TIMx_CCR2 disabled.",
                1: "Preload register on TIMx_CCR2 enabled.", }),
            Bits(bits=10, name="OC2FE", descr="Output Compare 2 fast enable"),
            Bits(bits=[8, 9], name="CC2S", descr="Capture/Compare 2 selection", descr_vals={
                0b00: "CC1 channel is configured as output",
                0b01: "CC1 channel is configured as input, IC2 is mapped on TI2",
                0b10: "CC1 channel is configured as input, IC2 is mapped on TI1",
                0b11: "CC1 channel is configured as input, IC2 is mapped on TRC.", }),

            Bits(bits=7, name="OC1CE", descr="Output Compare 1 clear enable"),
            Bits(bits=[4, 5, 6, 16], name="OC1M", descr="Output Compare 1 mode", descr_vals={
                0b0000: "Frozen",
                0b0001: "Set channel to active level on match.",
                0b0010: "Set channel to inactive level on match.",
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
            Bits(bits=3, name="OC1PE", descr="Output Compare 1 preload enable", descr_vals={
                0: "Preload register on TIMx_CCR1 disabled.",
                1: "Preload register on TIMx_CCR1 enabled.", }),
            Bits(bits=2, name="OC1FE", descr="Output Compare 1 fast enable"),
            Bits(bits=[0, 1], name="CC1S", descr="Capture/Compare 1 selection", descr_vals={
                0b00: "CC1 channel is configured as output",
                0b01: "CC1 channel is configured as input, IC1 is mapped on TI1",
                0b10: "CC1 channel is configured as input, IC1 is mapped on TI2",
                0b11: "CC1 channel is configured as input, IC1 is mapped on TRC.", }),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_CCMR2_IN"), addr=(base + 0x1C),
        descr="TIMx capture/compare mode register 2", ))
    self.append(MmapReg(
        name=(f"{prefix}_CCMR2_OUT"), addr=(base + 0x1C),
        descr="TIMx capture/compare mode register 2",
        bits=[
            Bits(bits=15, name="OC4CE", descr="Output Compare 4 clear enable"),
            Bits(bits=[12, 13, 14, 24], name="OC4M", descr="Output Compare 4 mode", descr_vals={
                0b0000: "Frozen",
                0b0001: "Set channel to active level on match.",
                0b0010: "Set channel to inactive level on match.",
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
            Bits(bits=11, name="OC4PE", descr="Output Compare 4 preload enable", descr_vals={
                0: "Preload register on TIMx_CCR4 disabled.",
                1: "Preload register on TIMx_CCR4 enabled.", }),
            Bits(bits=10, name="OC4FE", descr="Output Compare 4 fast enable"),
            Bits(bits=[8, 9], name="CC4S", descr="Capture/Compare 4 selection", descr_vals={
                0b00: "CC4 channel is configured as output",
                0b01: "CC4 channel is configured as input, IC2 is mapped on TI2",
                0b10: "CC4 channel is configured as input, IC2 is mapped on TI1",
                0b11: "CC4 channel is configured as input, IC2 is mapped on TRC.", }),

            Bits(bits=7, name="OC3CE", descr="Output Compare 3 clear enable"),
            Bits(bits=[4, 5, 6, 16], name="OC3M", descr="Output Compare 3 mode", descr_vals={
                0b0000: "Frozen",
                0b0001: "Set channel to active level on match.",
                0b0010: "Set channel to inactive level on match.",
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
            Bits(bits=3, name="OC3PE", descr="Output Compare 3 preload enable", descr_vals={
                0: "Preload register on TIMx_CCR3 disabled.",
                1: "Preload register on TIMx_CCR3 enabled.", }),
            Bits(bits=2, name="OC3FE", descr="Output Compare 3 fast enable"),
            Bits(bits=[0, 1], name="CC3S", descr="Capture/Compare 3 selection", descr_vals={
                0b00: "CC3 channel is configured as output",
                0b01: "CC3 channel is configured as input, IC1 is mapped on TI1",
                0b10: "CC3 channel is configured as input, IC1 is mapped on TI2",
                0b11: "CC3 channel is configured as input, IC1 is mapped on TRC.", }),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_CCER"), addr=(base + 0x20), descr="TIMx capture/compare enable register",
        bits=[
            Bits(bits=21, name="CC6P", descr="Capture/Compare 6 output polarity"),
            Bits(bits=20, name="CC6E", descr="Capture/Compare 6 output enable"),
            Bits(bits=17, name="CC5P", descr="Capture/Compare 5 output polarity"),
            Bits(bits=16, name="CC5E", descr="Capture/Compare 5 output enable"),
            Bits(bits=15, name="CC4NP", descr="Capture/Compare 4 complementary output polarity"),
            Bits(bits=13, name="CC4P", descr="Capture/Compare 4 output polarity"),
            Bits(bits=12, name="CC4E", descr="Capture/Compare 4 output enable"),
            Bits(bits=11, name="CC3NP", descr="Capture/Compare 3 complementary output polarity"),
            Bits(bits=10, name="CC3NE", descr="Capture/Compare 3 complementary output enable"),
            Bits(bits=9, name="CC3P", descr="Capture/Compare 3 output polarity"),
            Bits(bits=8, name="CC3E", descr="Capture/Compare 3 output enable"),
            Bits(bits=7, name="CC2NP", descr="Capture/Compare 2 complementary output polarity"),
            Bits(bits=6, name="CC2NE", descr="Capture/Compare 2 complementary output enable"),
            Bits(bits=5, name="CC2P", descr="Capture/Compare 2 output polarity"),
            Bits(bits=4, name="CC2E", descr="Capture/Compare 2 output enable"),
            Bits(
                bits=3, name="CC1NP", descr="Capture/Compare 1 complementary output polarity",
                descr_vals={
                    0: "OC1N active high (output mode).",
                    1: "OC1N active low (output mode).", }),
            Bits(bits=2, name="CC1NE", descr="Capture/Compare 1 complementary output enable"),
            Bits(bits=1, name="CC1P", descr="Capture/Compare 1 output polarity", descr_vals={
                0: "OC1 active high (output mode).",
                1: "OC1 active low (output mode).", }),
            Bits(bits=0, name="CC1E", descr="Capture/Compare 1 output enable"),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_CNT"), addr=(base + 0x24), descr="TIMx counter",
        bits=[
            Bits(bits=31, name="UIFCPY", descr="UIF copy"),
            Bits(bits=range(0, 16), name="CNT", descr="Counter value"),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_PSC"), addr=(base + 0x28), descr="TIMx prescaler",
        bits=[
            Bits(bits=range(0, 16), name="PSC", descr="Prescaler value"),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_ARR"), addr=(base + 0x2C), descr="TIMx auto-reload register",
        bits=[
            Bits(bits=range(0, 16), name="ARR", descr="Auto-reload value"),
        ]
    ))
    # TIMx repetition counter register (TIMx_RCR)(x = 1, 8). Address offset: 0x30
    self.append(MmapReg(
        name=(f"{prefix}_CCR1"), addr=(base + 0x34), descr="TIMx capture/compare register 1",
        bits=[
            Bits(bits=range(0, 16), name="CCR1", descr="Capture/Compare 1 value"),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_CCR2"), addr=(base + 0x38), descr="TIMx capture/compare register 2",
        bits=[
            Bits(bits=range(0, 16), name="CCR2", descr="Capture/Compare 2 value"),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_CCR3"), addr=(base + 0x3C), descr="TIMx capture/compare register 3",
        bits=[
            Bits(bits=range(0, 16), name="CCR3", descr="Capture/Compare 3 value"),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_CCR4"), addr=(base + 0x40), descr="TIMx capture/compare register 4",
        bits=[
            Bits(bits=range(0, 16), name="CCR4", descr="Capture/Compare 4 value"),
        ]
    ))
    self.append(MmapReg(
        name=(f"{prefix}_BDTR"), addr=(base + 0x44), descr="TIMx break and dead-time register",
        bits=[
            Bits(bits=25, name="BK2P", descr="Break 2 polarity"),
            Bits(bits=24, name="BK2E", descr="Break 2 enable"),
            Bits(bits=range(20, 24), name="BK2F", descr="Break 2 filter"),
            Bits(bits=range(16, 20), name="BKF", descr="Break filter"),
            Bits(
                bits=15, name="MOE", descr="Main output enable", descr_vals={
                    0: "OC and OCN outputs are disabled",
                    1: "OC and OCN outputs are enabled if their respective enable bits are set "
                       "(CCxE, CCxNE in TIMx_CCER register).", }),
            Bits(
                bits=14, name="AOE", descr="Automatic output enable", descr_vals={
                    0: "MOE can be set only by software",
                    1: "MOE can be set by software or automatically at the next update event "
                       "(if none of the break inputs BRK and BRK2 is active)", }),
            Bits(bits=13, name="BKP", descr="Break polarity"),
            Bits(bits=12, name="BKE", descr="Break enable"),
            Bits(bits=11, name="OSSR", descr="Off-state selection for Run mode"),
            Bits(bits=10, name="OSSI", descr="Off-state selection for Idle mode"),
            Bits(bits=[8, 9], name="LOCK", descr="Lock configuration"),
            Bits(bits=range(0, 8), name="DTG", descr="Dead-time generator setup"),
        ]
    ))
