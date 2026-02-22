# Phase 2: ElevenLabs Transcription + Provider Comparison — Tracker

> **Last Updated:** 2026-02-22
> **Phase Status:** IN PROGRESS

---

## Implementation Order

| # | Task | Status | Depends On | Notes |
|---|------|--------|------------|-------|
| 2.1 | Add `_group_words_into_utterances()` helper in `transcriber.py` | DONE | — | Filters spacing tokens, groups by `speaker_id`, returns `list[Utterance]` |
| 2.2 | Implement `transcribe_elevenlabs()` in `transcriber.py` | DONE | 2.1 | `client.speech_to_text.convert()` with scribe_v2, diarize, keyterms; calls 2.1 for grouping |
| 2.3 | Add provider radio toggle in `app.py` | DONE | 2.2 | `st.radio("Transcription Provider", ["Deepgram", "ElevenLabs"])`; routes to correct function |
| 2.4 | Add per-provider API key validation in `app.py` | DONE | 2.3 | Shows warning only for the selected provider's missing key |
| 2.5 | Add latency display in `app.py` | DONE | 2.3 | `time.time()` around transcription call; shows "Transcribed in X.Xs via Provider" |
| 2.6 | Test: UI smoke test (no API key) | NOT STARTED | 2.3 | App launches, radio toggle works, warnings display for each provider |
| 2.7 | Test: ElevenLabs end-to-end with real audio | NOT STARTED | 2.2 | Requires real ElevenLabs API key in `.env` |
| 2.8 | Test: Compare both providers on same audio | NOT STARTED | 2.7 | Medical term accuracy, diarization accuracy, latency |

## Verification Checklist

- [ ] `streamlit run app.py` launches without errors
- [ ] Provider radio toggle appears and defaults to Deepgram
- [ ] Selecting ElevenLabs with missing API key shows appropriate warning
- [ ] Selecting Deepgram with missing API key shows appropriate warning (existing behavior preserved)
- [ ] `transcribe_elevenlabs()` returns `list[Utterance]` with correct speaker IDs, text, and timestamps
- [ ] Spacing tokens are filtered out (no empty utterances)
- [ ] Speaker changes produce separate utterances
- [ ] Transcript display works identically for both providers (same format)
- [ ] Latency is displayed after transcription completes
- [ ] With valid ElevenLabs API key: transcription returns diarized results
- [ ] Both providers produce comparable output for the same audio input

## Issues

| # | Date | Issue | Resolution |
|---|------|-------|------------|
| — | — | — | — |

## Next

-> Phase 3: Speaker role mapping (Speaker 0/1 → Doctor/Patient). Prerequisite: at least one provider tested end-to-end with real audio.
