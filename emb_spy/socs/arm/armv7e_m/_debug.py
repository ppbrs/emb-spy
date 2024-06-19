"""Part of ARMV7EM SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg


def init_debug(self):
    assert self.__class__.__name__ == "ARMV7EM"

    self.append(MmapReg(
        name="DHCSR", addr=0xE000EDF0,
        descr="Debug Halting Control and Status Register",
    ))
    self.append(MmapReg(
        name="DCRSR", addr=0xE000EDF4,
        descr="Debug Core Register Selector Register",
    ))
    self.append(MmapReg(
        name="DCRDR", addr=0xE000EDF8,
        descr="Debug Core Register Data Register",
    ))
    self.append(MmapReg(
        name="DEMCR", addr=0xE000EDFC,
        descr="Debug Exception and Monitor Control Register",
        bits=[
            Bits(bits=24, name="TRCENA", descr="Global enable for all DWT and ITM features.")
        ],
    ))
    # ======================================================================================
    dwt_base = 0xE0001000
    self.append(MmapReg(
        name="DWT_PCSR", addr=dwt_base + 0x01C, descr="DWT program counter sample register",
        bits=[
            Bits(bits=range(0, 32), name="EIASAMPLE")
        ],
    ))
    # ======================================================================================
    itm_base = 0xE0000000
    self.append(MmapReg(
        name="ITM_TER", addr=itm_base + 0xE00, descr="ITM trace enable register",
        bits=[
            Bits(bits=range(0, 13), name="PRESCALER", descr="SWO baud rate scaling.")
        ],
    ))
    for i in range(8):
        self.append(MmapReg(
            name=f"ITM_STIM{i}", addr=itm_base + i * 4, descr=f"ITM stimulus register {i}",
            bits=[
            ],
        ))
    # ======================================================================================

    # dbgmcu_base = 0xE00E1000  # externally, 0x5C001000 internally
    dbgmcu_base = 0x5C001000
    # swo_base = 0xE00E3000
    swo_base = 0x5C003000
    # swtf_base = 0xE00E4000
    swtf_base = 0x5C004000
    # tsg_base = 0xE00E5000
    # tsg_base = 0x5C005000

    # ======================================================================================
    self.append(MmapReg(
        name="SWO_CODR", addr=swo_base + 0x010, descr="SWO current output divisor register",
        bits=[
            Bits(bits=range(0, 13), name="PRESCALER", descr="SWO baud rate scaling.")
        ],
    ))
    self.append(MmapReg(
        name="SWO_SPPR", addr=swo_base + 0x0F0, descr="SWO selected pin protocol register",
        bits=[
            Bits(bits=[0, 1], name="PPROT", descr="Pin protocol.")
        ],
    ))
    self.append(MmapReg(
        name="SWO_FFSR", addr=swo_base + 0x300, descr="SWO formatter and flush status register",
    ))
    self.append(MmapReg(
        name="SWO_CLAIMSET", addr=swo_base + 0xFA0, descr="SWO claim tag set register",
    ))
    self.append(MmapReg(
        name="SWO_CLAIMCLR", addr=swo_base + 0xFA4, descr="SWO claim tag clear register",
    ))
    self.append(MmapReg(
        name="SWO_LAR", addr=swo_base + 0xFB0, descr="SWO lock access register",
    ))
    self.append(MmapReg(
        name="SWO_LSR", addr=swo_base + 0xFB4, descr="SWO lock status register",
    ))
    self.append(MmapReg(
        name="SWO_AUTHSTAT", addr=swo_base + 0xFB8, descr="SWO authentication status register",
    ))
    self.append(MmapReg(
        name="SWO_DEVID", addr=swo_base + 0xFC8, descr="SWO device configuration register",
    ))
    self.append(MmapReg(
        name="SWO_DEVTYPE", addr=swo_base + 0xFCC, descr="SWO device type identifier register",
    ))
    self.append(MmapReg(
        name="SWO_PIDR4", addr=swo_base + 0xFD0,
        descr="SWO CoreSight peripheral identity register 4",
    ))
    self.append(MmapReg(
        name="SWO_PIDR0", addr=swo_base + 0xFE0,
        descr="SWO CoreSight peripheral identity register 0",
    ))
    self.append(MmapReg(
        name="SWO_PIDR1", addr=swo_base + 0xFE4,
        descr="SWO CoreSight peripheral identity register 1",
    ))
    self.append(MmapReg(
        name="SWO_PIDR2", addr=swo_base + 0xFE8,
        descr="SWO CoreSight peripheral identity register 2",
    ))
    self.append(MmapReg(
        name="SWO_PIDR3", addr=swo_base + 0xFEC,
        descr="SWO CoreSight peripheral identity register 3",
    ))
    self.append(MmapReg(
        name="SWO_CIDR0", addr=swo_base + 0xFF0,
        descr="SWO CoreSight component identity register 0",
    ))
    self.append(MmapReg(
        name="SWO_CIDR1", addr=swo_base + 0xFF4,
        descr="SWO CoreSight component identity register 1",
    ))
    self.append(MmapReg(
        name="SWO_CIDR2", addr=swo_base + 0xFF8,
        descr="SWO CoreSight component identity register 2",
    ))
    self.append(MmapReg(
        name="SWO_CIDR3", addr=swo_base + 0xFFC,
        descr="SWO CoreSight component identity register 3",
    ))
    # ======================================================================================
    self.append(MmapReg(
        name="SWTF_CTRL", addr=swtf_base + 0x000, descr="SWTF control register",
        bits=[
            Bits(bits=0, name="ENS0", descr="Slave port S0 enable."),
            Bits(bits=range(8, 12), name="MIN_HOLD_TIME",
                 descr="Number of transactions between arbitrations."),
        ],
    ))
    self.append(MmapReg(
        name="SWTF_PRIORITY", addr=swtf_base + 0x004, descr="SWTF priority register",
    ))
    self.append(MmapReg(
        name="SWTF_CLAIMSET", addr=swtf_base + 0xFA0, descr="SWTF claim tag set register",
    ))
    self.append(MmapReg(
        name="SWTF_CLAIMCLR", addr=swtf_base + 0xFA4, descr="SWTF claim tag clear register",
    ))
    self.append(MmapReg(
        name="SWTF_LAR", addr=swtf_base + 0xFB0, descr="SWTF lock access register",
    ))
    self.append(MmapReg(
        name="SWTF_LSR", addr=swtf_base + 0xFB4, descr="SWTF lock status register",
    ))
    self.append(MmapReg(
        name="SWTF_AUTHSTAT", addr=swtf_base + 0xFB8, descr="SWTF authentication status register",
    ))
    self.append(MmapReg(
        name="SWTF_DEVID", addr=swtf_base + 0xFC8, descr="SWTF CoreSight device identity register",
    ))
    self.append(MmapReg(
        name="SWTF_DEVTYPE", addr=swtf_base + 0xFCC,
        descr="SWTF CoreSight device type identity register",
    ))
    self.append(MmapReg(
        name="SWTF_PIDR4", addr=swtf_base + 0xFD0,
        descr="SWTF CoreSight peripheral identity register 4",
    ))
    self.append(MmapReg(
        name="SWTF_PIDR0", addr=swtf_base + 0xFE0,
        descr="SWTF CoreSight peripheral identity register 0",
    ))
    self.append(MmapReg(
        name="SWTF_PIDR1", addr=swtf_base + 0xFE4,
        descr="SWTF CoreSight peripheral identity register 1",
    ))
    self.append(MmapReg(
        name="SWTF_PIDR2", addr=swtf_base + 0xFE8,
        descr="SWTF CoreSight peripheral identity register 2",
    ))
    self.append(MmapReg(
        name="SWTF_PIDR3", addr=swtf_base + 0xFEC,
        descr="SWTF CoreSight peripheral identity register 3",
    ))
    self.append(MmapReg(
        name="SWTF_CIDR0", addr=swtf_base + 0xFF0,
        descr="SWTF CoreSight component identity register 0",
    ))
    self.append(MmapReg(
        name="SWTF_CIDR1", addr=swtf_base + 0xFF4,
        descr="SWTF CoreSight component identity register 1",
    ))
    self.append(MmapReg(
        name="SWTF_CIDR2", addr=swtf_base + 0xFF8,
        descr="SWTF CoreSight component identity register 2",
    ))
    self.append(MmapReg(
        name="SWTF_CIDR3", addr=swtf_base + 0xFFC,
        descr="SWTF CoreSight component identity register 3",
    ))
    # ======================================================================================
    self.append(MmapReg(
        name="DBGMCU_IDC", addr=dbgmcu_base + 0x000, descr="DBGMCU identity code register.",
        bits=[
            Bits(bits=range(16, 32), name="REV_ID", descr="Revision."),
            Bits(bits=range(12), name="DEV_ID", descr="Device ID."),
        ],
    ))
    self.append(MmapReg(
        name="DBGMCU_CR", addr=dbgmcu_base + 0x004, descr="DBGMCU configuration register.",
        bits=[
            Bits(bits=28, name="TRGOEN", descr="External trigger output enable"),
            Bits(bits=22, name="D3DBGCKEN", descr="D3 debug clock enable"),
            Bits(bits=21, name="D1DBGCKEN", descr="D1 debug clock enable"),
            Bits(bits=20, name="TRACECLKEN", descr="Trace port clock enable"),
            Bits(bits=2, name="DBGSTBY_D1", descr="D1 domain debug in Standby mode enable"),
            Bits(bits=1, name="DBGSTOP_D1", descr="D1 domain debug in Stop mode enable"),
            Bits(bits=0, name="DBGSLEEP_D1", descr="D1 domain debug in Sleep mode enable"),
        ],
    ))
    self.append(MmapReg(
        name="DBGMCU_APB3FZ1", addr=dbgmcu_base + 0x034,
        descr="DBGMCU APB3 peripheral freeze register",
    ))
    self.append(MmapReg(
        name="DBGMCU_APB1LFZ1", addr=dbgmcu_base + 0x03C,
        descr="DBGMCU APB1L peripheral freeze register",
    ))
    self.append(MmapReg(
        name="DBGMCU_APB2FZ1", addr=dbgmcu_base + 0x04C,
        descr="DBGMCU APB2 peripheral freeze register",
    ))
    self.append(MmapReg(
        name="DBGMCU_APB4FZ1", addr=dbgmcu_base + 0x054,
        descr="DBGMCU APB4 peripheral freeze register",
    ))
    # ======================================================================================
