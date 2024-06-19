"""Part of ARMV7EM SoC."""
from emb_spy.socs.bits import Bits
from emb_spy.socs.reg import MmapReg


def init_mpu(self):
    assert self.__class__.__name__ == "ARMV7EM"

    self.append(MmapReg(
        name="MPU_TYPE", addr=0xE000ED90,
        descr="MPU Type Register",
        bits=[
            Bits(bits=range(8, 16), name="DREGION", descr="Indicates the number of supported MPU data regions depending on your implementation"),
            # 0x08 = 8 MPU regions.
            # 0x10 = 16 MPU regions.
        ]))
    self.append(MmapReg(
        name="MPU_CTRL", addr=0xE000ED94,
        descr="MPU Control Register",
        bits=[
            Bits(bits=range(8, 16), name="DREGION", descr="Indicates the number of supported MPU data regions depending on your implementation"),
            # 0x08 = 8 MPU regions.
            # 0x10 = 16 MPU regions.

            Bits(bits=2, name="PRIVDEFENA", descr="Enables privileged software access to the default memory map"),
            Bits(bits=1, name="HFNMIENA", descr="Enables the operation of MPU during hard fault, NMI, and FAULTMASK handlers"),
            Bits(bits=0, name="ENABLE", descr="Enables the MPU"),
        ]))

    # 0xE000ED98 MPU_RNR RW Privileged MPU Region Number Register
    # 0xE000ED9C MPU_RBAR RW Privileged MPU Region Base Address Register
    # 0xE000EDA0 MPU_RASR RW Privileged MPU Region Attribute and Size Register
    # 0xE000EDA4 MPU_RBAR_A1 RW Privileged Alias of RBAR
    # 0xE000EDA8 MPU_RASR_A1 RW Privileged Alias of RASR
    # 0xE000EDAC MPU_RBAR_A2 RW Privileged Alias of RBAR
    # 0xE000EDB0 MPU_RASR_A2 RW Privileged Alias of RASR
    # 0xE000EDB4 MPU_RBAR_A3 RW Privileged Alias of RBAR
    # 0xE000EDB8 MPU_RASR_A3 RW Privileged Alias of RASR
