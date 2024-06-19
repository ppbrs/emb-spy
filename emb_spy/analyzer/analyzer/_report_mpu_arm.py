"""Part of Analyzer class."""
import inspect

from emb_spy import ReaderStaticResult


def report_mpu_armv7e_m(
    self,
    bits_data: dict[str, ReaderStaticResult],
    md_file,
) -> None:
    """Add a Core chapter to the report."""
    assert "Analyzer" in [cls.__name__ for cls in inspect.getmro(self.__class__)]
    # which is basically the same as issublass(self.__class__, Analyzer).

    md_file.new_header(level=1, title="MPU (ARM v7e-m)")

    num_reg = bits_data["MPU_TYPE.DREGION"].val
    md_file.new_line(f"* {num_reg} MPU regions.")

    enabled = bits_data["MPU_CTRL.ENABLE"].val
    md_file.new_line("* MPU " + ("enabled." if enabled else "disabled"))

    hfnmiena = bits_data["MPU_CTRL.HFNMIENA"].val
    if hfnmiena:
        md_file.new_line("* The MPU is enabled during hard fault, NMI, and FAULTMASK handlers.")
    else:
        md_file.new_line(
            "* MPU is disabled during hard fault, NMI, and FAULTMASK handlers, "
            "regardless of the value of the ENABLE bit.")

    privdefena = bits_data["MPU_CTRL.PRIVDEFENA"].val
    if privdefena:
        md_file.new_line(
            "* If the MPU is enabled, the default memory map can be used as a background region "
            "for privileged software accesses.")
    else:
        md_file.new_line(
            "* If the MPU is enabled, the default memory map cannot be used as a background region "
            "for privileged software accesses.")

    md_file.new_line("***")
