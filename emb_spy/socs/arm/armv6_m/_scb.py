"""Part of ARMV6M SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_scb(self: SoC) -> None:
    """Generate Register objects for System Timer core peripheral."""
    assert self.__class__.__name__ == "ARMV6M"
    self.append(MmapReg(name="CPUID", addr=0xE000ED00, descr="CPUID Register"))
    self.append(MmapReg(
        name="ICSR", addr=0xE000ED04, descr="Interrupt Control and State Register"))
    self.append(MmapReg(
        name="AIRCR", addr=0xE000ED0C,
        descr="a0xFA050000 Application Interrupt and Reset Control Register"))
    self.append(MmapReg(name="SCR", addr=0xE000ED10, descr="System Control Register"))
    self.append(MmapReg(
        name="CCR", addr=0xE000ED14, descr="Configuration and Control Register"))
    self.append(MmapReg(
        name="SHPR2", addr=0xE000ED1C, descr="System Handler Priority Register 2",
        bits=[
            Bits(bits=range(24, 32), name="PRI_11",
                descr="Priority of system handler 11, SVCall"),]))
    self.append(MmapReg(
        name="SHPR3", addr=0xE000ED20, descr="System Handler Priority Register 3",
        bits=[
            Bits(
                bits=range(24, 32), name="PRI_15",
                descr="Priority of system handler 15, SysTick exception"),
            Bits(
                bits=range(16, 24), name="PRI_14",
                descr="Priority of system handler 14, PendSV"),]))
