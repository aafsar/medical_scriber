from dataclasses import dataclass, field


@dataclass
class TermAccuracyResult:
    found: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    total: int = 0
    accuracy: float = 0.0


@dataclass
class DiarizationStats:
    doctor_utterances: int = 0
    patient_utterances: int = 0
    first_speaker_is_doctor: bool = False


@dataclass
class ScriptComparison:
    script_name: str = ""
    provider: str = ""
    term_accuracy: TermAccuracyResult = field(default_factory=TermAccuracyResult)
    diarization: DiarizationStats = field(default_factory=DiarizationStats)
    transcription_time: float = 0.0
    note_generation_time: float = 0.0


def parse_key_terms(script_path: str) -> list[str]:
    """Extract 'Key terms to verify' from script header, split on commas."""
    with open(script_path) as f:
        for line in f:
            if line.strip().startswith("> **Key terms to verify:**"):
                terms_str = line.split(":**", 1)[1].strip()
                return [t.strip() for t in terms_str.split(",") if t.strip()]
    return []


def check_term_accuracy(terms: list[str], transcript_text: str) -> TermAccuracyResult:
    """Case-insensitive substring check for each term in the transcript."""
    text_lower = transcript_text.lower()
    found = [t for t in terms if t.lower() in text_lower]
    missing = [t for t in terms if t.lower() not in text_lower]
    total = len(terms)
    accuracy = len(found) / total if total else 0.0
    return TermAccuracyResult(found=found, missing=missing, total=total, accuracy=accuracy)


def compute_diarization_stats(
    utterances: list, speaker_map: dict[int, str]
) -> DiarizationStats:
    """Count Doctor/Patient utterances and check first speaker."""
    doctor_count = 0
    patient_count = 0
    first_is_doctor = False

    for i, u in enumerate(utterances):
        role = speaker_map.get(u.speaker, "")
        if role == "Doctor":
            doctor_count += 1
            if i == 0:
                first_is_doctor = True
        elif role == "Patient":
            patient_count += 1

    return DiarizationStats(
        doctor_utterances=doctor_count,
        patient_utterances=patient_count,
        first_speaker_is_doctor=first_is_doctor,
    )


def build_comparison_markdown(
    script_name: str,
    deepgram: ScriptComparison | None,
    elevenlabs: ScriptComparison | None,
) -> str:
    """Per-script side-by-side comparison report."""
    lines = [f"# Comparison — {script_name}", ""]

    # Term accuracy table
    lines.append("## Medical Term Accuracy")
    lines.append("")
    lines.append("| Metric | Deepgram | ElevenLabs |")
    lines.append("|--------|----------|------------|")

    dg_acc = f"{len(deepgram.term_accuracy.found)}/{deepgram.term_accuracy.total} ({deepgram.term_accuracy.accuracy:.0%})" if deepgram else "N/A"
    el_acc = f"{len(elevenlabs.term_accuracy.found)}/{elevenlabs.term_accuracy.total} ({elevenlabs.term_accuracy.accuracy:.0%})" if elevenlabs else "N/A"
    lines.append(f"| Accuracy | {dg_acc} | {el_acc} |")
    lines.append("")

    for label, comp in [("Deepgram", deepgram), ("ElevenLabs", elevenlabs)]:
        if comp:
            lines.append(f"### {label}")
            lines.append(f"- Found ({len(comp.term_accuracy.found)}/{comp.term_accuracy.total}): {', '.join(comp.term_accuracy.found)}")
            if comp.term_accuracy.missing:
                lines.append(f"- Missing: {', '.join(comp.term_accuracy.missing)}")
            lines.append("")

    # Diarization stats
    lines.append("## Diarization Stats")
    lines.append("")
    lines.append("| Metric | Deepgram | ElevenLabs |")
    lines.append("|--------|----------|------------|")

    dg_doc = str(deepgram.diarization.doctor_utterances) if deepgram else "N/A"
    el_doc = str(elevenlabs.diarization.doctor_utterances) if elevenlabs else "N/A"
    dg_pat = str(deepgram.diarization.patient_utterances) if deepgram else "N/A"
    el_pat = str(elevenlabs.diarization.patient_utterances) if elevenlabs else "N/A"
    dg_first = ("Yes" if deepgram.diarization.first_speaker_is_doctor else "No") if deepgram else "N/A"
    el_first = ("Yes" if elevenlabs.diarization.first_speaker_is_doctor else "No") if elevenlabs else "N/A"

    lines.append(f"| Doctor utterances | {dg_doc} | {el_doc} |")
    lines.append(f"| Patient utterances | {dg_pat} | {el_pat} |")
    lines.append(f"| First speaker = Doctor | {dg_first} | {el_first} |")
    lines.append("")

    # Latency
    lines.append("## Latency")
    lines.append("")
    lines.append("| Metric | Deepgram | ElevenLabs |")
    lines.append("|--------|----------|------------|")

    dg_trans = f"{deepgram.transcription_time:.1f}s" if deepgram else "N/A"
    el_trans = f"{elevenlabs.transcription_time:.1f}s" if elevenlabs else "N/A"
    dg_note = f"{deepgram.note_generation_time:.1f}s" if deepgram else "N/A"
    el_note = f"{elevenlabs.note_generation_time:.1f}s" if elevenlabs else "N/A"
    dg_total = f"{deepgram.transcription_time + deepgram.note_generation_time:.1f}s" if deepgram else "N/A"
    el_total = f"{elevenlabs.transcription_time + elevenlabs.note_generation_time:.1f}s" if elevenlabs else "N/A"

    lines.append(f"| Transcription | {dg_trans} | {el_trans} |")
    lines.append(f"| Note generation | {dg_note} | {el_note} |")
    lines.append(f"| Total | {dg_total} | {el_total} |")
    lines.append("")

    return "\n".join(lines)


def build_summary_markdown(
    all_results: list[ScriptComparison], timestamp: str
) -> str:
    """Aggregate report across all scripts."""
    lines = [f"# Test Summary — {timestamp}", ""]

    # Group by script name
    scripts: dict[str, dict[str, ScriptComparison]] = {}
    for r in all_results:
        scripts.setdefault(r.script_name, {})[r.provider] = r

    # Overview table
    lines.append("## Overview")
    lines.append("")
    lines.append("| Script | DG Terms | EL Terms | DG Latency | EL Latency |")
    lines.append("|--------|----------|----------|------------|------------|")

    for script_name, providers in scripts.items():
        dg = providers.get("Deepgram")
        el = providers.get("ElevenLabs")
        dg_terms = f"{len(dg.term_accuracy.found)}/{dg.term_accuracy.total} ({dg.term_accuracy.accuracy:.0%})" if dg else "N/A"
        el_terms = f"{len(el.term_accuracy.found)}/{el.term_accuracy.total} ({el.term_accuracy.accuracy:.0%})" if el else "N/A"
        dg_lat = f"{dg.transcription_time:.1f}s + {dg.note_generation_time:.1f}s" if dg else "N/A"
        el_lat = f"{el.transcription_time:.1f}s + {el.note_generation_time:.1f}s" if el else "N/A"
        lines.append(f"| {script_name} | {dg_terms} | {el_terms} | {dg_lat} | {el_lat} |")
    lines.append("")

    # Medical Term Accuracy Detail
    lines.append("## Medical Term Accuracy Detail")
    lines.append("")
    for script_name, providers in scripts.items():
        for provider_name in ["Deepgram", "ElevenLabs"]:
            comp = providers.get(provider_name)
            if comp:
                lines.append(f"### {script_name} — {provider_name}")
                lines.append(f"Found ({len(comp.term_accuracy.found)}/{comp.term_accuracy.total}): {', '.join(comp.term_accuracy.found)}")
                if comp.term_accuracy.missing:
                    lines.append(f"Missing: {', '.join(comp.term_accuracy.missing)}")
                lines.append("")

    # Diarization Stats
    lines.append("## Diarization Stats")
    lines.append("")
    lines.append("| Script | Provider | Doctor | Patient | First=Doctor? |")
    lines.append("|--------|----------|--------|---------|---------------|")
    for script_name, providers in scripts.items():
        for provider_name in ["Deepgram", "ElevenLabs"]:
            comp = providers.get(provider_name)
            if comp:
                first = "Yes" if comp.diarization.first_speaker_is_doctor else "No"
                lines.append(f"| {script_name} | {provider_name} | {comp.diarization.doctor_utterances} | {comp.diarization.patient_utterances} | {first} |")
    lines.append("")

    # Latency
    lines.append("## Latency")
    lines.append("")
    lines.append("| Script | Provider | Transcription | Note Gen | Total |")
    lines.append("|--------|----------|---------------|----------|-------|")
    for script_name, providers in scripts.items():
        for provider_name in ["Deepgram", "ElevenLabs"]:
            comp = providers.get(provider_name)
            if comp:
                total = comp.transcription_time + comp.note_generation_time
                lines.append(f"| {script_name} | {provider_name} | {comp.transcription_time:.1f}s | {comp.note_generation_time:.1f}s | {total:.1f}s |")
    lines.append("")

    # Overall winner
    dg_accuracies = [r.term_accuracy.accuracy for r in all_results if r.provider == "Deepgram"]
    el_accuracies = [r.term_accuracy.accuracy for r in all_results if r.provider == "ElevenLabs"]
    dg_totals = [r.transcription_time + r.note_generation_time for r in all_results if r.provider == "Deepgram"]
    el_totals = [r.transcription_time + r.note_generation_time for r in all_results if r.provider == "ElevenLabs"]

    lines.append("## Overall")
    lines.append("")

    if dg_accuracies and el_accuracies:
        dg_avg = sum(dg_accuracies) / len(dg_accuracies)
        el_avg = sum(el_accuracies) / len(el_accuracies)
        if dg_avg > el_avg:
            lines.append(f"- Term accuracy winner: Deepgram ({dg_avg:.0%} vs {el_avg:.0%})")
        elif el_avg > dg_avg:
            lines.append(f"- Term accuracy winner: ElevenLabs ({el_avg:.0%} vs {dg_avg:.0%})")
        else:
            lines.append(f"- Term accuracy: Tie ({dg_avg:.0%})")

    if dg_totals and el_totals:
        dg_avg_lat = sum(dg_totals) / len(dg_totals)
        el_avg_lat = sum(el_totals) / len(el_totals)
        if dg_avg_lat < el_avg_lat:
            lines.append(f"- Latency winner: Deepgram ({dg_avg_lat:.1f}s avg vs {el_avg_lat:.1f}s avg)")
        elif el_avg_lat < dg_avg_lat:
            lines.append(f"- Latency winner: ElevenLabs ({el_avg_lat:.1f}s avg vs {dg_avg_lat:.1f}s avg)")
        else:
            lines.append(f"- Latency: Tie ({dg_avg_lat:.1f}s avg)")

    lines.append("")
    return "\n".join(lines)
