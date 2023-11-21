
from emb_spy.mmreg.registers_if import Register, RegisterBits  # pylint: disable=import-error
from ._gpio import _Gpio
from ._tim1_tim8 import _Tim1Tim8


class MmregSTM32(_Gpio, _Tim1Tim8):
    """ """
    pass
