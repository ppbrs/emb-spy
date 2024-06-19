"""Part of ARMV6M SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_nvic(self: SoC) -> None:
    """Generate Register objects for System Timer core peripheral."""
    assert self.__class__.__name__ == "ARMV6M"

    # Note: Suffix 0 in ISER, ICER, ISPR, ICPRis used to make names compatible to ARM-V7E=M.
    self.append(
        MmapReg(name="NVIC_ISER0", addr=0xE000E100, descr="Interrupt Set-enable Register", bits=[
            Bits(bits=range(0, 32), name="SETENA"), ]))
    self.append(MmapReg(
        name="NVIC_ICER0", addr=0xE000E180, descr="Interrupt Clear-enable Register", bits=[
            Bits(bits=range(0, 32), name="CLRENA"), ]))
    self.append(MmapReg(
        name="NVIC_ISPR0", addr=0xE000E200, descr="Interrupt Set-pending Register", bits=[
            Bits(bits=range(0, 32), name="SETPEND"), ]))
    self.append(MmapReg(
        name="NVIC_ICPR0", addr=0xE000E280, descr="Interrupt Clear-pending Register", bits=[
            Bits(bits=range(0, 32), name="CLRPEND"), ]))

    ipr_arr = []
    irqn_num = 32
    for irqn in range(irqn_num):
        if irqn % 4 == 0:
            ipr_idx = irqn // 4
            ipr_arr.append(MmapReg(
                name=f"NVIC_IPR{ipr_idx}", addr=(0xE000E400 + ipr_idx * 4),
                descr=f"Interrupt Priority Register {ipr_idx}", bits=[]))
        bit_start = (irqn % 4) * 8
        bit_end = bit_start + 8
        ipr_arr[ipr_idx].bits.append(
            Bits(bits=range(bit_start, bit_end), name=f"PRI_{irqn}"),
        )

    self.extend(ipr_arr)
