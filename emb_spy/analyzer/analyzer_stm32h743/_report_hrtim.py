"""Part of AnalyzerSTM32H743 class."""

from mdutils.mdutils import MdUtils

from emb_spy import ReaderStaticResult


def report_hrtim(
    self,  # : AnalyzerSTM32H743
    bits_data: dict[str, ReaderStaticResult],
    md_file: MdUtils,
) -> None:
    """Add "HRTIM" chapter to the report."""
    # Circular import error does not allow importin AnalyzerSTM32H743 from this module, hence this:
    assert self.__class__.__name__ == "AnalyzerSTM32H743"

    md_file.new_header(level=1, title="HRTIM")

    master_en = bool(bits_data["HRTIM_MCR.MCEN"].val)
    tmr_a_en = bool(bits_data["HRTIM_MCR.TACEN"].val)
    tmr_b_en = bool(bits_data["HRTIM_MCR.TBCEN"].val)
    tmr_c_en = bool(bits_data["HRTIM_MCR.TCCEN"].val)
    tmr_d_en = bool(bits_data["HRTIM_MCR.TDCEN"].val)
    tmr_e_en = bool(bits_data["HRTIM_MCR.TECEN"].val)

    if master_en:
        md_file.new_line("* Master timer enabled")
    else:
        md_file.new_line("* Master timer disabled")

    _report_hrtim_timer(self=self, idx="A", en=tmr_a_en, bits_data=bits_data, md_file=md_file)
    _report_hrtim_timer(self=self, idx="B", en=tmr_b_en, bits_data=bits_data, md_file=md_file)
    _report_hrtim_timer(self=self, idx="C", en=tmr_c_en, bits_data=bits_data, md_file=md_file)
    _report_hrtim_timer(self=self, idx="D", en=tmr_d_en, bits_data=bits_data, md_file=md_file)
    _report_hrtim_timer(self=self, idx="E", en=tmr_e_en, bits_data=bits_data, md_file=md_file)
    md_file.new_line("***")


def _report_hrtim_timer(
    self,  # : AnalyzerSTM32H743
    idx: str,
    en: bool,
    bits_data,
    md_file: MdUtils,
) -> None:
    assert idx in {"A", "B", "C", "D", "E"}

    if en:
        md_file.new_line(f"* Timer {idx} enabled")
        cnt = bits_data[f"HRTIM_CNT{idx}R.CNT"].val
        per = bits_data[f"HRTIM_PER{idx}R.PER"].val
        ckpsc = bits_data[f"HRTIM_TIM{idx}CR.CKPSC"].val
        match ckpsc:
            case 0b101:
                freq = self.state.hrtim_freq
            case 0b110:
                freq = self.state.hrtim_freq / 2
            case 0b111:
                freq = self.state.hrtim_freq / 4
            case _:
                raise ValueError(f"HRTIM_TIM{idx}CR.CKPSC")
        md_file.new_line(f"\t* {freq} Hz")
        md_file.new_line(f"\t* CNT = {cnt}, PER = {per} = {freq / per} Hz")
        #
        # Outputs
        #
        for out_idx in [1, 2]:
            for out_type in ["SET", "RST"]:
                events: list[str] = []
                reg = f"HRTIM_{out_type}{idx}{out_idx}R"
                if bits_data[f"{reg}.UPDATE"].val:
                    events.append("UPDATE = Registers update")
                if bits_data[f"{reg}.EXTEVNT10"].val:
                    events.append("EXTEVNT10 = External Event 10")
                if bits_data[f"{reg}.EXTEVNT9"].val:
                    events.append("EXTEVNT9 = External Event 9")
                if bits_data[f"{reg}.EXTEVNT8"].val:
                    events.append("EXTEVNT8 = External Event 8")
                if bits_data[f"{reg}.EXTEVNT7"].val:
                    events.append("EXTEVNT7 = External Event 7")
                if bits_data[f"{reg}.EXTEVNT6"].val:
                    events.append("EXTEVNT6 = External Event 6")
                if bits_data[f"{reg}.EXTEVNT5"].val:
                    events.append("EXTEVNT5 = External Event 5")
                if bits_data[f"{reg}.EXTEVNT4"].val:
                    events.append("EXTEVNT4 = External Event 4")
                if bits_data[f"{reg}.EXTEVNT3"].val:
                    events.append("EXTEVNT3 = External Event 3")
                if bits_data[f"{reg}.EXTEVNT2"].val:
                    events.append("EXTEVNT2 = External Event 2")
                if bits_data[f"{reg}.EXTEVNT1"].val:
                    events.append("EXTEVNT1 = External Event 1")
                if bits_data[f"{reg}.TIMEVNT9"].val:
                    events.append("TIMEVNT9 = Timer Event 9")
                if bits_data[f"{reg}.TIMEVNT8"].val:
                    events.append("TIMEVNT8 = Timer Event 8")
                if bits_data[f"{reg}.TIMEVNT7"].val:
                    events.append("TIMEVNT7 = Timer Event 7")
                if bits_data[f"{reg}.TIMEVNT6"].val:
                    events.append("TIMEVNT6 = Timer Event 6")
                if bits_data[f"{reg}.TIMEVNT5"].val:
                    events.append("TIMEVNT5 = Timer Event 5")
                if bits_data[f"{reg}.TIMEVNT4"].val:
                    events.append("TIMEVNT4 = Timer Event 4")
                if bits_data[f"{reg}.TIMEVNT3"].val:
                    events.append("TIMEVNT3 = Timer Event 3")
                if bits_data[f"{reg}.TIMEVNT2"].val:
                    events.append("TIMEVNT2 = Timer Event 2")
                if bits_data[f"{reg}.TIMEVNT1"].val:
                    events.append("TIMEVNT1 = imer Event 1")
                if bits_data[f"{reg}.MSTCMP4"].val:
                    events.append("MSTCMP4 = Master Compare 4")
                if bits_data[f"{reg}.MSTCMP3"].val:
                    events.append("MSTCMP3 = Master Compare 3")
                if bits_data[f"{reg}.MSTCMP2"].val:
                    events.append("MSTCMP2 = Master Compare 2")
                if bits_data[f"{reg}.MSTCMP1"].val:
                    events.append("MSTCMP1 = Master Compare 1")
                if bits_data[f"{reg}.MSTPER"].val:
                    events.append("MSTPER = Master Period")
                if bits_data[f"{reg}.CMP4"].val:
                    events.append(f"CMP4 = Timer {idx} Compare 4")
                if bits_data[f"{reg}.CMP3"].val:
                    events.append(f"CMP3 = Timer {idx} Compare 3")
                if bits_data[f"{reg}.CMP2"].val:
                    events.append(f"CMP2 = Timer {idx} Compare 2")
                if bits_data[f"{reg}.CMP1"].val:
                    events.append(f"CMP1 = Timer {idx} Compare 1")
                if bits_data[f"{reg}.PER"].val:
                    events.append(f"PER = Timer {idx} Period")
                if bits_data[f"{reg}.RESYNC"].val:
                    events.append("RESYNC = Timer A resynchronization")
                if bits_data[f"{reg}.SST"].val:
                    events.append("SST = Software Set trigger")

                if events:
                    md_file.new_line(f"\t* Output {out_idx} {out_type}: " + ", ".join(events))

        #
        # Interrupts
        #
        # HRTIM_TIM{idx}DIER

    else:
        md_file.new_line(f"* Timer {idx} disabled")
