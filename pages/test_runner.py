import os
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

from compare import (
    ScriptComparison,
    build_comparison_markdown,
    build_summary_markdown,
    check_term_accuracy,
    compute_diarization_stats,
    parse_key_terms,
)
from note_generator import build_download_markdown, generate_notes
from transcriber import format_transcript_for_llm, transcribe_deepgram, transcribe_elevenlabs

# --- Script registry ---
SCRIPT_REGISTRY = {
    "Ortho — Knee Pain": {
        "script_path": "sample_scripts/ortho_knee_pain.md",
        "folder_name": "ortho_knee_pain",
        "patient_info": {
            "name": "John Smith",
            "date_of_birth": "03/15/1967",
            "date_of_service": datetime.now().strftime("%m/%d/%Y"),
            "referring_physician": "Dr. Sarah Chen",
            "specialty": "Orthopedic Surgery",
        },
    },
    "Cardio — Chest Pain": {
        "script_path": "sample_scripts/cardio_chest_pain.md",
        "folder_name": "cardio_chest_pain",
        "patient_info": {
            "name": "Margaret Wilson",
            "date_of_birth": "08/22/1970",
            "date_of_service": datetime.now().strftime("%m/%d/%Y"),
            "referring_physician": "Dr. Thompson",
            "specialty": "Cardiology",
        },
    },
    "Multi-Problem — Follow-up": {
        "script_path": "sample_scripts/multi_problem_followup.md",
        "folder_name": "multi_problem_followup",
        "patient_info": {
            "name": "Robert Davis",
            "date_of_birth": "06/10/1960",
            "date_of_service": datetime.now().strftime("%m/%d/%Y"),
            "referring_physician": "Dr. Kim",
            "specialty": "Internal Medicine",
        },
    },
}

SPEAKER_MAP = {0: "Doctor", 1: "Patient"}

# --- Header ---
st.title("Test Runner")
st.caption("Automated dual-provider comparison pipeline")
st.divider()

# --- Script selection ---
script_name = st.selectbox("Select test script", list(SCRIPT_REGISTRY.keys()))
script_info = SCRIPT_REGISTRY[script_name]

# Show key terms and patient info
key_terms = parse_key_terms(script_info["script_path"])
if key_terms:
    st.markdown(f"**Key terms to check ({len(key_terms)}):** {', '.join(key_terms)}")

with st.expander("Patient info (auto-filled)"):
    info = script_info["patient_info"]
    for k, v in info.items():
        st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")

st.divider()

# --- Audio input ---
input_method = st.radio("Audio Source", ["Record", "Upload"], horizontal=True)
if input_method == "Record":
    audio = st.audio_input("Record consultation")
else:
    audio = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a", "ogg", "webm", "flac"])

if audio:
    st.audio(audio)


def _run_provider(provider_name: str, audio_bytes: bytes, script_name: str, key_terms: list[str], patient_info: dict):
    """Run transcription + note generation for one provider, return ScriptComparison and artifacts."""
    # Transcribe
    t0 = time.time()
    if provider_name == "Deepgram":
        utterances = transcribe_deepgram(audio_bytes)
    else:
        utterances = transcribe_elevenlabs(audio_bytes)
    transcription_time = time.time() - t0

    if not utterances:
        return None, None, None

    transcript_text = format_transcript_for_llm(utterances, SPEAKER_MAP)

    # Generate notes
    t0 = time.time()
    notes = generate_notes(transcript_text, patient_info=patient_info)
    note_generation_time = time.time() - t0

    notes_md = build_download_markdown(notes)

    # Compute metrics
    term_acc = check_term_accuracy(key_terms, transcript_text)
    diar_stats = compute_diarization_stats(utterances, SPEAKER_MAP)

    comparison = ScriptComparison(
        script_name=script_name,
        provider=provider_name,
        term_accuracy=term_acc,
        diarization=diar_stats,
        transcription_time=transcription_time,
        note_generation_time=note_generation_time,
    )

    return comparison, transcript_text, notes_md


# --- Run Full Test button ---
if audio and st.button("Run Full Test", type="primary", use_container_width=True):
    audio_bytes = audio.getvalue()

    # Initialize session timestamp (shared across scripts in same browser session)
    if "test_session_ts" not in st.session_state:
        st.session_state.test_session_ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    ts = st.session_state.test_session_ts
    folder = script_info["folder_name"]
    output_dir = Path("test_results") / ts / folder
    output_dir.mkdir(parents=True, exist_ok=True)

    dg_result = None
    dg_transcript = None
    dg_notes_md = None
    dg_error = None

    el_result = None
    el_transcript = None
    el_notes_md = None
    el_error = None

    # --- Deepgram ---
    with st.spinner("Running Deepgram..."):
        try:
            dg_result, dg_transcript, dg_notes_md = _run_provider(
                "Deepgram", audio_bytes, script_name, key_terms, script_info["patient_info"]
            )
        except Exception as e:
            dg_error = str(e)

    # --- ElevenLabs ---
    with st.spinner("Running ElevenLabs..."):
        try:
            el_result, el_transcript, el_notes_md = _run_provider(
                "ElevenLabs", audio_bytes, script_name, key_terms, script_info["patient_info"]
            )
        except Exception as e:
            el_error = str(e)

    # --- Save files ---
    with st.spinner("Comparing results..."):
        if dg_transcript:
            (output_dir / "deepgram_transcript.md").write_text(dg_transcript)
        if dg_notes_md:
            (output_dir / "deepgram_notes.md").write_text(dg_notes_md)
        if el_transcript:
            (output_dir / "elevenlabs_transcript.md").write_text(el_transcript)
        if el_notes_md:
            (output_dir / "elevenlabs_notes.md").write_text(el_notes_md)

        comparison_md = build_comparison_markdown(script_name, dg_result, el_result)
        (output_dir / "comparison.md").write_text(comparison_md)

    # Track results in session state for summary generation
    if "test_results" not in st.session_state:
        st.session_state.test_results = []
    if dg_result:
        st.session_state.test_results.append(dg_result)
    if el_result:
        st.session_state.test_results.append(el_result)

    # --- Display results ---
    st.divider()
    st.markdown("## Results")

    if dg_error:
        st.error(f"Deepgram failed: {dg_error}")
    if el_error:
        st.error(f"ElevenLabs failed: {el_error}")

    # Side-by-side comparison
    col_dg, col_el = st.columns(2)

    with col_dg:
        st.markdown("### Deepgram")
        if dg_result:
            acc = dg_result.term_accuracy
            st.metric("Term Accuracy", f"{len(acc.found)}/{acc.total} ({acc.accuracy:.0%})")
            st.caption(f"Transcription: {dg_result.transcription_time:.1f}s | Notes: {dg_result.note_generation_time:.1f}s")
            st.caption(f"Doctor: {dg_result.diarization.doctor_utterances} | Patient: {dg_result.diarization.patient_utterances} | First=Doctor: {'Yes' if dg_result.diarization.first_speaker_is_doctor else 'No'}")
            if acc.missing:
                st.warning(f"Missing terms: {', '.join(acc.missing)}")
        elif not dg_error:
            st.warning("No speech detected")

    with col_el:
        st.markdown("### ElevenLabs")
        if el_result:
            acc = el_result.term_accuracy
            st.metric("Term Accuracy", f"{len(acc.found)}/{acc.total} ({acc.accuracy:.0%})")
            st.caption(f"Transcription: {el_result.transcription_time:.1f}s | Notes: {el_result.note_generation_time:.1f}s")
            st.caption(f"Doctor: {el_result.diarization.doctor_utterances} | Patient: {el_result.diarization.patient_utterances} | First=Doctor: {'Yes' if el_result.diarization.first_speaker_is_doctor else 'No'}")
            if acc.missing:
                st.warning(f"Missing terms: {', '.join(acc.missing)}")
        elif not el_error:
            st.warning("No speech detected")

    st.success(f"Results saved to `{output_dir}/`")

# --- Summary generation ---
st.divider()

results = st.session_state.get("test_results", [])
if results:
    tested_scripts = {r.script_name for r in results}
    st.caption(f"Scripts tested this session: {', '.join(sorted(tested_scripts))}")

    if st.button("Generate Summary", use_container_width=True):
        ts = st.session_state.get("test_session_ts", datetime.now().strftime("%Y-%m-%d_%H%M%S"))
        summary_md = build_summary_markdown(results, ts)
        summary_path = Path("test_results") / ts / "test_summary.md"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(summary_md)
        st.markdown(summary_md)
        st.success(f"Summary saved to `{summary_path}`")
