"""Part of ARMV7EM SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg


def init_nvic(self):
    assert self.__class__.__name__ == "ARMV7EM"
    for irq in range(0, 240):
        if irq % 32 == 0:
            self.append(MmapReg(
                name=f"NVIC_ISER{irq // 32}",
                addr=0xE000E100 + 4 * (irq // 32),
                descr="Interrupt Set-enable Register",
                bits=[
                    Bits(bits=n, name=f"SETENA{irq + n}")
                    for n in range(32) if irq + n < 240
                ],
            ))
            self.append(MmapReg(
                name=f"NVIC_ICER{irq // 32}",
                addr=0XE000E180 + 4 * (irq // 32),
                descr="Interrupt Clear-enable Register",
                bits=[
                    Bits(bits=n, name=f"CLRENA{irq + n}")
                    for n in range(32) if irq + n < 240
                ],
            ))
            self.append(MmapReg(
                name=f"NVIC_ISPR{irq // 32}",
                addr=0XE000E200 + 4 * (irq // 32),
                descr="Interrupt Set-pending Register",
                bits=[
                    Bits(bits=n, name=f"SETPEND{irq + n}")
                    for n in range(32) if irq + n < 240
                ],
            ))
            self.append(MmapReg(
                name=f"NVIC_ICPR{irq // 32}",
                addr=0xE000E280 + 4 * (irq // 32),
                descr="Interrupt Clear-pending Register",
                bits=[
                    Bits(bits=n, name=f"CLRPEND{irq + n}")
                    for n in range(32) if irq + n < 240
                ],
            ))
            self.append(MmapReg(
                name=f"NVIC_IABR{irq // 32}",
                addr=0xE000E300 + 4 * (irq // 32),
                descr="Interrupt Active Bit Register",
                bits=[
                    Bits(bits=n, name=f"ACTIVE{irq + n}")
                    for n in range(32) if irq + n < 240
                ],
            ))

        if irq % 4 == 0:
            self.append(MmapReg(
                name=f"NVIC_IPR{irq // 4}",
                addr=0xE000E400 + 4 * (irq // 4),
                descr="Interrupt Priority Register",
                bits=[
                    Bits(bits=range(4 * n, 4 * n + 4), name=f"PRI_{irq + n}")
                    for n in range(4) if irq + n < 240
                ],
            ))

    self.append(MmapReg(
        name="STIR", addr=0xE000EF00,
        descr="Software Trigger Interrupt Register",
        bits=[
            Bits(bits=range(0, 9), name="INTID",
                 descr="Interrupt ID of the interrupt to trigger, in the range 0-239"),
        ],
    ))
