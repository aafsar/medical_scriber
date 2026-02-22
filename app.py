import streamlit as st

from config import DEEPGRAM_API_KEY
from transcriber import Utterance, transcribe_deepgram

st.set_page_config(page_title="AI Medical Scriber", layout="wide")

st.title("AI Medical Scriber")

if not DEEPGRAM_API_KEY or DEEPGRAM_API_KEY == "your_deepgram_key_here":
    st.warning("Deepgram API key is not set. Add it to your `.env` file to enable transcription.")

audio = st.audio_input("Record consultation")

if audio:
    st.audio(audio)

    if st.button("Transcribe"):
        with st.spinner("Transcribing audio..."):
            try:
                audio_bytes = audio.getvalue()
                st.session_state.transcript = transcribe_deepgram(audio_bytes)
            except ValueError as e:
                st.error(str(e))
            except RuntimeError as e:
                st.error(str(e))

if st.session_state.get("transcript"):
    st.subheader("Transcript")
    for u in st.session_state.transcript:
        minutes, seconds = divmod(u.start, 60)
        st.markdown(f"**Speaker {u.speaker}** [{int(minutes)}:{seconds:05.2f}]  \n{u.text}")
