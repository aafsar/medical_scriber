# Phase 2: ElevenLabs Transcription + Provider Comparison — Plan & Context

> **Goal:** Add ElevenLabs Scribe v2 as a second transcription provider and let users switch between Deepgram and ElevenLabs in the UI.
> **Outcome:** [filled after completion]

---

## Pre-Conditions

- Phase 1 complete: `transcribe_deepgram()` working, `Utterance` dataclass defined, `app.py` wired up
- `elevenlabs==2.36.1` already installed (Phase 0)
- `ELEVENLABS_API_KEY` placeholder in `.env` and loaded in `config.py`
- `ELEVENLABS_MODEL = "scribe_v2"` and `MEDICAL_KEYTERMS` (71 terms) already in `config.py`

---

## 1. ElevenLabs SDK Integration

### API Call

Use `client.speech_to_text.convert()` from the `elevenlabs` package (v2.36.1):

```
client = ElevenLabs(api_key=...)
result = client.speech_to_text.convert(
    model_id="scribe_v2",
    file=audio_bytes,
    language_code="en",
    diarize=True,
    num_speakers=2,
    timestamps_granularity="word",
    tag_audio_events=False,
    keyterms=MEDICAL_KEYTERMS,
)
```

Key parameters:
- `num_speakers=2` — hint for doctor + patient (avoids over-splitting)
- `keyterms` — the 71 medical terms from `config.py` (max 100, each < 50 chars)
- `tag_audio_events=False` — skip non-speech sounds; we only need spoken words
- `timestamps_granularity="word"` — needed for start/end times on each word

### Response Structure

The response is a `SpeechToTextChunkResponseModel` with:
- `text: str` — full transcript (no speaker labels)
- `words: list[SpeechToTextWordResponseModel]` — flat, chronological word list
- `language_code: str`, `language_probability: float`

Each word object:
- `text: str` — the word
- `speaker_id: Optional[str]` — e.g. `"speaker_0"`, `"speaker_1"` (only when `diarize=True`)
- `start: Optional[float]` — seconds
- `end: Optional[float]` — seconds
- `type: str` — `"word"` | `"spacing"` | `"audio_event"`
- `logprob: float` — confidence in `[-inf, 0]`, closer to 0 = higher confidence

---

## 2. Word-Level → Utterance Reconstruction

This is the main technical difference from Deepgram. Deepgram returns ready-made utterances; ElevenLabs returns word-level objects. We must group consecutive words with the same `speaker_id` into `Utterance` objects.

### Algorithm

1. Filter out `spacing` tokens (they have `start=None`, no speaker content)
2. Iterate words in order; when `speaker_id` changes, close the current utterance and start a new one
3. Build text by joining word texts with spaces
4. Use the first word's `start` and last word's `end` for utterance timestamps
5. Extract the integer from `speaker_id` string (e.g. `"speaker_0"` → `0`) to match the `Utterance.speaker: int` field

### Edge Cases

- **`speaker_id` is `None`**: Possible for very short audio or silence. Skip these words or assign to the previous speaker.
- **Single-word utterances**: Valid — just one word between speaker changes.
- **Empty result**: If `words` is empty, return an empty list (same as Deepgram behavior).

---

## 3. Function Signature

The new function follows the same contract as `transcribe_deepgram()`:

```
def transcribe_elevenlabs(audio_bytes: bytes) -> list[Utterance]
```

- Same input: raw audio bytes from `st.audio_input().getvalue()`
- Same output: `list[Utterance]` with `speaker: int`, `text: str`, `start: float`, `end: float`
- Same exceptions: `ValueError` for missing API key, `RuntimeError` for API failures

This lets `app.py` swap providers without changing any display logic.

---

## 4. UI Changes — Provider Toggle

Add a provider selector in `app.py` before the Transcribe button:

- Use `st.radio()` with options `["Deepgram", "ElevenLabs"]`
- Route to `transcribe_deepgram()` or `transcribe_elevenlabs()` based on selection
- Show the appropriate API key warning based on selected provider
- The transcript display code stays unchanged (it already works with `list[Utterance]`)

### Validation

- If Deepgram is selected but `DEEPGRAM_API_KEY` is missing/placeholder → show warning
- If ElevenLabs is selected but `ELEVENLABS_API_KEY` is missing/placeholder → show warning

---

## 5. Latency Tracking

Wrap each transcription call with `time.time()` to measure round-trip latency. Display the elapsed time below the transcript (e.g. "Transcribed in 3.2s via Deepgram"). This enables the provider comparison without a dedicated comparison UI — the user can transcribe the same audio with each provider and compare.

---

## 6. Files Changed

| File | Changes |
|------|---------|
| `transcriber.py` | Add `transcribe_elevenlabs()` + word-grouping helper |
| `app.py` | Add provider radio, route transcription call, show latency, validate both API keys |

No changes needed to `config.py` or `requirements.txt` — ElevenLabs config and dependency are already in place from Phase 0.
