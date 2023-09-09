from emb_spy.mmreg.registers_if import Register, Registers, RegisterBits  # pylint: disable=import-error


class _Nvic(Registers):

    def __init__(self):
        self.regs = []
        for irq in range(0, 240):
            if irq % 32 == 0:
                self.regs += [
                    Register(
                        name=f"NVIC_ISER{irq // 32}",
                        addr=0xE000E100 + 4 * (irq // 32),
                        descr="Interrupt Set-enable Register",
                        register_bits=[
                            RegisterBits(bits=n, name=f"SETENA{irq + n}", descr="", values={})
                            for n in range(32) if irq + n < 240
                        ],
                    ),
                    Register(
                        name=f"NVIC_ICER{irq // 32}",
                        addr=0XE000E180 + 4 * (irq // 32),
                        descr="Interrupt Clear-enable Register",
                        register_bits=[
                            RegisterBits(bits=n, name=f"CLRENA{irq + n}", descr="", values={})
                            for n in range(32) if irq + n < 240
                        ],
                    ),
                    Register(
                        name=f"NVIC_ISPR{irq // 32}",
                        addr=0XE000E200 + 4 * (irq // 32),
                        descr="Interrupt Set-pending Register",
                        register_bits=[
                            RegisterBits(bits=n, name=f"SETPEND{irq + n}", descr="", values={})
                            for n in range(32) if irq + n < 240
                        ],
                    ),
                    Register(
                        name=f"NVIC_ICPR{irq // 32}",
                        addr=0xE000E280 + 4 * (irq // 32),
                        descr="Interrupt Clear-pending Register",
                        register_bits=[
                            RegisterBits(bits=n, name=f"CLRPEND{irq + n}", descr="", values={})
                            for n in range(32) if irq + n < 240
                        ],
                    ),
                    Register(
                        name=f"NVIC_IABR{irq // 32}",
                        addr=0xE000E300 + 4 * (irq // 32),
                        descr="Interrupt Active Bit Register",
                        register_bits=[
                            RegisterBits(bits=n, name=f"ACTIVE{irq + n}", descr="", values={})
                            for n in range(32) if irq + n < 240
                        ],
                    ),
                ]

            if irq % 4 == 0:
                self.regs.append(
                    Register(
                        name=f"NVIC_IPR{irq // 4}",
                        addr=0xE000E400 + 4 * (irq // 4),
                        descr="Interrupt Priority Register",
                        register_bits=[
                            RegisterBits(bits=range(4 * n, 4 * n + 4), name=f"PRI_N{irq + n}", descr="", values={})
                            for n in range(4) if irq + n < 240
                        ],
                    )
                )

        self.regs.append(
            Register(
                name="STIR",
                addr=0xE000EF00,
                descr="Software Trigger Interrupt Register",
                register_bits=[
                    # RegisterBits(bits=31, name="APSR:N", descr="Negative flag", values={}),
                ],
            ),
        )
