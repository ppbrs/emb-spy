"""Part of STM32H743 SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg
from emb_spy.socs.soc import SoC


def init_pwr(self: SoC) -> None:
    assert self.__class__.__name__ == "STM32H743"

    pwr_base = 0x58024800

    self.append(MmapReg(
        name="PWR_CR1", addr=(pwr_base + 0x000), descr="PWR control register 1", ))
    self.append(MmapReg(
        name="PWR_CSR1", addr=(pwr_base + 0x004), descr="PWR control status register 1", ))
    self.append(MmapReg(
        name="PWR_CR2", addr=(pwr_base + 0x008), descr="PWR control register 2", ))
    self.append(MmapReg(
        name="PWR_CR3", addr=(pwr_base + 0x00C), descr="PWR control register 3",
        bits=[
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
            Bits(
                bits=2, name="SCUEN", descr="Supply configuration update enable",
                descr_vals={
                    0: "Supply configuration update locked..",
                    1: "Single write enabled to Supply configuration (LDOEN and BYPASS)",
                }
            ),
            Bits(
                bits=1, name="LDOEN", descr="Low drop-out regulator enable",
                descr_vals={
                    0: "Low drop-out regulator disabled.",
                    1: "Low drop-out regulator enabled (default)",
                }
            ),
            Bits(
                bits=0, name="BYPASS", descr="Power management unit bypass",
                descr_vals={
                    0: "Power management unit normal operation.",
                    1: "Power management unit bypassed, voltage monitoring still active.",
                }
            ),
        ]
    ))
    self.append(MmapReg(
        name="PWR_CPUCR", addr=(pwr_base + 0x010), descr="PWR CPU control register", ))
    self.append(MmapReg(
        name="PWR_D3CR", addr=(pwr_base + 0x018), descr="PWR D3 domain control register", ))
    self.append(MmapReg(
        name="PWR_WKUPCR", addr=(pwr_base + 0x020), descr="PWR wakeup clear register", ))
    self.append(MmapReg(
        name="PWR_WKUPFR", addr=(pwr_base + 0x024), descr="PWR wakeup flag register", ))
    self.append(MmapReg(
        name="PWR_WKUPEPR", addr=(pwr_base + 0x028),
        descr="PWR wakeup enable and polarity register", ))
