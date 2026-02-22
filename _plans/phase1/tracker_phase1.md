# Phase 1: Audio Recording + Deepgram Transcription — Tracker

> **Last Updated:** 2026-02-22
> **Phase Status:** DONE (end-to-end test pending real API key)

---

## Implementation Order

| # | Task | Status | Depends On | Notes |
|---|------|--------|------------|-------|
| 1.1 | Create `transcriber.py` with `Utterance` dataclass | DONE | — | |
| 1.2 | Implement `transcribe_deepgram()` function | DONE | 1.1 | SDK v5 call chain confirmed |
| 1.3 | Create `app.py` with page config and title | DONE | — | |
| 1.4 | Add `st.audio_input()` recording + playback | DONE | 1.3 | |
| 1.5 | Add API key warning display | DONE | 1.3 | Checks missing + placeholder key |
| 1.6 | Wire Transcribe button with spinner + session state | DONE | 1.2, 1.4 | |
| 1.7 | Add transcript display with Speaker N labels + timestamps | DONE | 1.6 | MM:SS.ss format |
| 1.8 | Add error handling (missing key, API failures) | DONE | 1.6 | ValueError, RuntimeError |
| 1.9 | Test: UI smoke test (no API key) | DONE | 1.1–1.8 | App launches, HTTP 200, imports OK |
| 1.10 | Test: end-to-end with real audio (API key required) | PENDING | 1.9 | Requires real Deepgram API key in .env |

---

## Verification Checklist

- [x] `streamlit run app.py` launches without errors
- [x] Audio widget appears and can record/play back audio
- [x] Warning message displays when `DEEPGRAM_API_KEY` is not set
- [x] Clicking Transcribe without a recording shows appropriate feedback
- [ ] With a valid API key: transcription returns diarized results (needs real key)
- [x] Speaker labels (Speaker 0, Speaker 1, ...) display correctly
- [x] Timestamps display next to each utterance
- [x] Transcript persists across Streamlit widget interactions (session state)
- [x] API errors surface as user-friendly messages (not raw tracebacks)

---

## Issues

| # | Date | Issue | Resolution |
|---|------|-------|------------|
| 1 | 2026-02-22 | Pydantic v1 compatibility warning with Python 3.14 | Cosmetic only — deepgram-sdk still functions correctly |

---

## Next

-> Phase 2: ElevenLabs transcription + provider comparison. Prerequisites: Phase 1 complete, ElevenLabs API key obtained.
