# Phase 1: Audio Recording + Deepgram Transcription — Plan & Context

> **Goal:** Build a Streamlit app that records audio via the browser, sends it to Deepgram for transcription with speaker diarization, and displays the diarized transcript.
> **Outcome:** Implemented. App records audio, sends to Deepgram SDK v5 for diarized transcription, displays Speaker N labels with timestamps. Note: Pydantic v0 warning on Python 3.14 is cosmetic only.

---

## Pre-Conditions

- Phase 0 complete (repo, venv, deps, config)
- Deepgram API key obtained and added to `.env`
- All dependencies installed (`streamlit`, `deepgram-sdk`, `python-dotenv`)

---

## `app.py` Design

The main Streamlit app provides a linear top-to-bottom workflow:

1. **Page config** — `st.set_page_config(page_title="AI Medical Scriber", layout="wide")`
2. **API key warning** — if `DEEPGRAM_API_KEY` is missing, show `st.warning()` at the top so the user knows transcription won't work
3. **Audio recording** — `st.audio_input("Record consultation")` returns an `UploadedFile` (BytesIO subclass) containing WAV at 16 kHz
4. **Audio playback** — the recorded audio displays inline automatically via `st.audio_input`; additionally show `st.audio()` after recording for explicit playback
5. **Transcribe button** — `st.button("Transcribe")` triggers `transcribe_deepgram()` inside a `st.spinner()`
6. **Session state** — store the transcript in `st.session_state.transcript` so it persists across Streamlit reruns (button clicks, widget interactions)
7. **Transcript display** — render each utterance with `Speaker N` label and timestamps

### Session state keys

| Key | Type | Purpose |
|-----|------|---------|
| `transcript` | `list[Utterance] \| None` | Persisted diarized transcript |

---

## `transcriber.py` Design

A single module with a dataclass and one public function.

### `Utterance` dataclass

Fields: `speaker: int`, `text: str`, `start: float`, `end: float`. Represents one speaker turn from the diarized transcript.

### `transcribe_deepgram(audio_bytes: bytes) -> list[Utterance]`

1. Validate that `DEEPGRAM_API_KEY` is set — raise `ValueError` if missing
2. Create a `DeepgramClient(api_key=...)` instance
3. Call the SDK v5 transcription method (see Deepgram SDK v5 section below)
4. Parse the response utterances into `list[Utterance]`
5. Return the list

### Error handling

| Error | Raised as | When |
|-------|-----------|------|
| Missing API key | `ValueError` | `DEEPGRAM_API_KEY` is `None` or empty |
| API failure | `RuntimeError` | SDK raises any exception during the API call |

---

## Deepgram SDK v5 Integration

The project uses `deepgram-sdk` 5.3.2, which is a Fern-generated SDK with a different API surface than the old v3 SDK. Many online examples reference the deprecated v3 API — do **not** use those patterns.

### Correct call chain (SDK v5)

```
client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
response = client.listen.v1.media.transcribe_file(
    request=audio_bytes,       # bytes directly, NOT a dict
    model=DEEPGRAM_MODEL,      # "nova-2-medical"
    diarize=True,
    utterances=True,           # REQUIRED — without this, .results.utterances is None
    smart_format=True,
    punctuate=True,
)
```

### Response parsing

```
response                                    # MediaTranscribeResponse
  .results                                  # ListenV1Response
    .utterances                             # list[...UtterancesItem] (None if utterances=False)
      [i].speaker                           # Optional[int] — speaker ID (0, 1, ...)
      [i].transcript                        # Optional[str] — utterance text
      [i].start                             # Optional[float] — start time in seconds
      [i].end                               # Optional[float] — end time in seconds
```

### Key gotchas

- `request` takes `bytes` directly — do **not** wrap in a dict like `{"buffer": data}`
- All options are flat kwargs — there is no `PrerecordedOptions` class in v5
- Must pass `utterances=True` or `.results.utterances` will be `None`
- Speaker IDs are integers starting at 0

---

## `st.audio_input()` Details

- Returns `UploadedFile` (a `BytesIO` subclass) or `None` if no recording
- Audio format: WAV at 16 kHz — this is Deepgram's optimal input format, so no conversion needed
- Use `.getvalue()` to extract raw bytes for the Deepgram API call

---

## How Files Interact

```
app.py
  ├── imports from config.py        (DEEPGRAM_API_KEY for warning check)
  ├── imports from transcriber.py   (transcribe_deepgram, Utterance)
  └── uses streamlit                (UI widgets, session state)

transcriber.py
  ├── imports from config.py        (DEEPGRAM_API_KEY, DEEPGRAM_MODEL)
  └── imports deepgram SDK          (DeepgramClient)

config.py
  └── reads from .env               (API keys via python-dotenv)
```
