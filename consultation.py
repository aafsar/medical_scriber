import time
from datetime import date

import streamlit as st

from config import ANTHROPIC_API_KEY, APP_MODE, DEEPGRAM_API_KEY, ELEVENLABS_API_KEY, SPECIALTIES
from note_generator import NOTE_SECTIONS, PATIENT_INFO_FIELDS, build_download_pdf, detect_speaker_roles, generate_notes
from transcriber import transcribe_deepgram, transcribe_elevenlabs, format_transcript_for_llm

st.markdown("""
<style>
    /* Success alerts */
    .stAlert [data-testid="stNotification"][data-type="success"] {
        background-color: #5F8F6A20;
        border-left-color: #5F8F6A;
        color: #2E2E2E;
    }
    /* Warning alerts */
    .stAlert [data-testid="stNotification"][data-type="warning"] {
        background-color: #C9A24D20;
        border-left-color: #C9A24D;
        color: #2E2E2E;
    }
    /* Error alerts */
    .stAlert [data-testid="stNotification"][data-type="error"] {
        background-color: #B25C5C20;
        border-left-color: #B25C5C;
        color: #2E2E2E;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #E6E8E4;
    }
    /* Download button */
    .stDownloadButton button {
        background-color: #2F6F6B;
        color: #F6F7F5;
    }
    .stDownloadButton button:hover {
        background-color: #245a57;
        color: #F6F7F5;
    }
    /* Transcript container */
    .transcript-line {
        padding: 0.4rem 0.75rem;
        border-radius: 6px;
        margin-bottom: 0.25rem;
    }
    .transcript-doctor {
        background-color: #2F6F6B12;
        border-left: 3px solid #2F6F6B;
    }
    .transcript-patient {
        background-color: #D6C7B220;
        border-left: 3px solid #D6C7B2;
    }
    .transcript-role {
        font-weight: 600;
        font-size: 0.85rem;
    }
    .transcript-time {
        color: #888;
        font-size: 0.75rem;
        margin-left: 0.4rem;
    }
    .transcript-text {
        margin-top: 0.15rem;
        font-size: 0.95rem;
    }
    /* Section headers */
    .section-header {
        color: #2F6F6B;
        font-size: 1.1rem;
        font-weight: 600;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #2F6F6B;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
header_left, header_right = st.columns([4, 1])
with header_left:
    st.title("Angy Voice")
    st.caption("AI-powered medical consultation scriber")
with header_right:
    st.image("assets/Angy_logo_color.png", width=250)

st.divider()

# --- Demo defaults for patient info ---
_DEMO_PATIENT = {
    "name": "Maria Garcia",
    "date_of_birth": "04/15/1985",
    "date_of_service": date.today().strftime("%m/%d/%Y"),
    "referring_physician": "Dr. James Wilson",
    "specialty": "Internal Medicine",
}

if APP_MODE == "demo" and "patient_info" not in st.session_state:
    st.session_state.patient_info = dict(_DEMO_PATIENT)

# --- Sidebar: patient info form ---
with st.sidebar:
    with st.form("patient_info_form"):
        st.subheader("Patient Information")
        _defaults = st.session_state.get("patient_info", {}) if APP_MODE == "demo" else {}
        patient_name = st.text_input("Patient Name", value=_defaults.get("name", ""))
        _default_dob = (
            date(1985, 4, 15) if APP_MODE == "demo" and not st.session_state.get("_dob_edited") else None
        )
        dob = st.date_input("Date of Birth", value=_default_dob, min_value=date(1936, 1, 1))
        dos = st.date_input("Date of Service", value=date.today())
        referring = st.text_input("Referring Physician", value=_defaults.get("referring_physician", ""))
        _default_specialty_idx = SPECIALTIES.index("Internal Medicine") if APP_MODE == "demo" else 0
        specialty = st.selectbox("Specialty", SPECIALTIES, index=_default_specialty_idx)
        submitted = st.form_submit_button("Save Patient Info", use_container_width=True)
        if submitted:
            st.session_state.patient_info = {
                "name": patient_name or "",
                "date_of_birth": dob.strftime("%m/%d/%Y") if dob else "",
                "date_of_service": dos.strftime("%m/%d/%Y") if dos else "",
                "referring_physician": referring or "",
                "specialty": specialty or "",
            }
            st.success("Patient info saved.")

    # Show saved patient info summary
    if st.session_state.get("patient_info"):
        info = st.session_state.patient_info
        if info.get("name"):
            st.markdown("---")
            st.markdown(f"**Current Patient:** {info['name']}")
            if info.get("specialty"):
                st.caption(f"{info['specialty']}")

# --- API key warnings ---
api_warnings = []
if APP_MODE == "dev" and (not DEEPGRAM_API_KEY or DEEPGRAM_API_KEY == "your_deepgram_key_here"):
    api_warnings.append("Deepgram")
if not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "your_elevenlabs_key_here":
    api_warnings.append("ElevenLabs")
if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_anthropic_key_here":
    api_warnings.append("Anthropic")

if api_warnings:
    st.warning(f"Missing API keys: **{', '.join(api_warnings)}**. Add them to your `.env` file.")

# --- Step 1: Audio Input ---
st.markdown('<p class="section-header">1. Audio Input</p>', unsafe_allow_html=True)

if APP_MODE == "dev":
    input_col, provider_col = st.columns([2, 1])
    with provider_col:
        provider = st.radio("Transcription Provider", ["Deepgram", "ElevenLabs"])
    with input_col:
        input_method = st.radio("Audio Source", ["Record", "Upload"], horizontal=True)
        if input_method == "Record":
            audio = st.audio_input("Record consultation")
        else:
            audio = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a", "ogg", "webm", "flac"])
else:
    provider = "Deepgram"
    audio = st.audio_input("Record consultation")

if audio:
    st.audio(audio)
    if st.button("Transcribe", type="primary", use_container_width=True):
        with st.spinner("Transcribing audio..."):
            try:
                audio_bytes = audio.getvalue()
                t0 = time.time()
                if provider == "ElevenLabs":
                    result = transcribe_elevenlabs(audio_bytes)
                else:
                    result = transcribe_deepgram(audio_bytes)
                elapsed = time.time() - t0

                if not result:
                    st.warning("No speech detected. Try recording again with a longer or louder consultation.")
                else:
                    st.session_state.transcript = result
                    if APP_MODE == "dev":
                        st.session_state.latency_msg = f"Transcribed in {elapsed:.1f}s via {provider}"
                    st.session_state.pop("notes", None)
                    st.session_state.pop("notes_latency_msg", None)
                    st.session_state.pop("detected_doctor_speaker", None)

                    with st.spinner("Identifying speakers..."):
                        detected = detect_speaker_roles(st.session_state.transcript)
                        st.session_state.detected_doctor_speaker = detected
            except (ValueError, RuntimeError) as e:
                st.error(str(e))

# --- Step 2: Transcript ---
if st.session_state.get("transcript"):
    st.divider()
    st.markdown('<p class="section-header">2. Transcript</p>', unsafe_allow_html=True)

    if st.session_state.get("latency_msg"):
        st.caption(st.session_state.latency_msg)

    detected = st.session_state.get("detected_doctor_speaker", 0)
    if APP_MODE == "dev":
        role_for_0 = st.radio(
            "Speaker 0 is:", ["Doctor", "Patient"],
            index=(0 if detected == 0 else 1), horizontal=True,
        )
    else:
        role_for_0 = "Doctor" if detected == 0 else "Patient"
    other_role = "Patient" if role_for_0 == "Doctor" else "Doctor"
    speaker_map = {0: role_for_0, 1: other_role}
    st.session_state.speaker_map = speaker_map
    st.session_state.llm_transcript = format_transcript_for_llm(
        st.session_state.transcript, speaker_map
    )

    with st.container(height=400):
        for u in st.session_state.transcript:
            role = speaker_map.get(u.speaker, f"Speaker {u.speaker}")
            minutes, seconds = divmod(u.start, 60)
            css_class = "transcript-doctor" if role == "Doctor" else "transcript-patient"
            st.markdown(
                f'<div class="transcript-line {css_class}">'
                f'<span class="transcript-role">{role}</span>'
                f'<span class="transcript-time">[{int(minutes)}:{seconds:05.2f}]</span>'
                f'<div class="transcript-text">{u.text}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # --- Step 3: Generate Notes ---
    st.divider()
    st.markdown('<p class="section-header">3. Generate Notes</p>', unsafe_allow_html=True)

    if st.button("Generate Notes", type="primary", use_container_width=True):
        with st.spinner("Generating consultation notes..."):
            try:
                t0 = time.time()
                st.session_state.notes = generate_notes(
                    st.session_state.llm_transcript,
                    patient_info=st.session_state.get("patient_info"),
                )
                elapsed = time.time() - t0
                st.session_state.notes_latency_msg = f"Notes generated in {elapsed:.1f}s"
            except (ValueError, RuntimeError) as e:
                st.error(str(e))

# --- Step 4: Consultation Notes ---
if st.session_state.get("notes"):
    st.divider()
    st.markdown('<p class="section-header">4. Consultation Notes</p>', unsafe_allow_html=True)

    if st.session_state.get("notes_latency_msg"):
        st.caption(st.session_state.notes_latency_msg)

    notes = st.session_state.notes
    for key, label in NOTE_SECTIONS:
        value = notes.get(key, "Not discussed")

        if key == "patient_information":
            info = value if isinstance(value, dict) else {}
            all_not_provided = all(v == "Not provided" for v in info.values())
            with st.expander(f"**{label}**", expanded=not all_not_provided):
                for field_key, field_label in PATIENT_INFO_FIELDS:
                    field_val = info.get(field_key, "Not provided")
                    if field_val == "Not provided":
                        st.markdown(f"**{field_label}:** :gray[{field_val}]")
                    else:
                        st.markdown(f"**{field_label}:** {field_val}")
        else:
            is_discussed = value != "Not discussed"
            with st.expander(f"**{label}**", expanded=is_discussed):
                if is_discussed:
                    st.markdown(value)
                else:
                    st.markdown(f":gray[{value}]")

    # --- Download ---
    st.divider()
    patient_info = st.session_state.get("patient_info", {})
    name = patient_info.get("name", "").strip()
    dos_str = patient_info.get("date_of_service", "").replace("/", "-")
    if name:
        base_name = name.lower().replace(" ", "_")
        if dos_str:
            base_name = f"{base_name}_{dos_str}"
        base_name = f"{base_name}_consultation"
    else:
        base_name = "consultation_notes"

    try:
        pdf_bytes = build_download_pdf(notes)
        st.download_button(
            "Download Notes (PDF)",
            data=pdf_bytes,
            file_name=f"{base_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception as e:
        st.warning(f"PDF generation failed: {e}")
