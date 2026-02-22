import time

import streamlit as st

from config import DEEPGRAM_API_KEY, ELEVENLABS_API_KEY
from transcriber import transcribe_deepgram, transcribe_elevenlabs, format_transcript_for_llm

st.set_page_config(page_title="AI Medical Scriber", layout="wide")

st.title("AI Medical Scriber")

provider = st.radio("Transcription Provider", ["Deepgram", "ElevenLabs"])

if provider == "Deepgram" and (not DEEPGRAM_API_KEY or DEEPGRAM_API_KEY == "your_deepgram_key_here"):
    st.warning("Deepgram API key is not set. Add it to your `.env` file to enable transcription.")
elif provider == "ElevenLabs" and (not ELEVENLABS_API_KEY or ELEVENLABS_API_KEY == "your_elevenlabs_key_here"):
    st.warning("ElevenLabs API key is not set. Add it to your `.env` file to enable transcription.")

audio = st.audio_input("Record consultation")

if audio:
    st.audio(audio)

    if st.button("Transcribe"):
        with st.spinner("Transcribing audio..."):
            try:
                audio_bytes = audio.getvalue()
                t0 = time.time()
                if provider == "ElevenLabs":
                    st.session_state.transcript = transcribe_elevenlabs(audio_bytes)
                else:
                    st.session_state.transcript = transcribe_deepgram(audio_bytes)
                elapsed = time.time() - t0
                st.session_state.latency_msg = f"Transcribed in {elapsed:.1f}s via {provider}"
            except (ValueError, RuntimeError) as e:
                st.error(str(e))

if st.session_state.get("transcript"):
    if st.session_state.get("latency_msg"):
        st.caption(st.session_state.latency_msg)

    role_for_0 = st.radio("Speaker 0 is:", ["Doctor", "Patient"], horizontal=True)
    other_role = "Patient" if role_for_0 == "Doctor" else "Doctor"
    speaker_map = {0: role_for_0, 1: other_role}
    st.session_state.speaker_map = speaker_map
    st.session_state.llm_transcript = format_transcript_for_llm(
        st.session_state.transcript, speaker_map
    )

    st.subheader("Transcript")
    for u in st.session_state.transcript:
        role = speaker_map.get(u.speaker, f"Speaker {u.speaker}")
        minutes, seconds = divmod(u.start, 60)
        st.markdown(f"**{role}** [{int(minutes)}:{seconds:05.2f}]  \n{u.text}")
