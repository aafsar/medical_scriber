# Phase 3: Speaker Role Mapping — Tracker

> **Last Updated:** 2026-02-22
> **Phase Status:** IN PROGRESS

---

## Implementation Order

| # | Task | Status | Depends On | Notes |
|---|------|--------|------------|-------|
| 3.1 | Add `format_transcript_for_llm()` to `transcriber.py` | DONE | — | Takes `list[Utterance]` + `speaker_map`, returns `Role: "text"` format |
| 3.2 | Add speaker assignment radio to `app.py` | DONE | 3.1 | `st.radio("Speaker 0 is:", ["Doctor", "Patient"])`, builds `speaker_map` |
| 3.3 | Update transcript display to use role labels | DONE | 3.2 | Replace `Speaker {N}` with `Doctor` / `Patient` using `speaker_map` |
| 3.4 | Store LLM-formatted transcript in session state | DONE | 3.1, 3.2 | `st.session_state.llm_transcript` for Phase 4 consumption |
| 3.5 | Create Phase 3 plan + tracker docs | DONE | — | This task |
| 3.6 | Test: UI smoke test | NOT STARTED | 3.3 | Radio renders, labels update, no errors on toggle |
| 3.7 | Test: LLM transcript format verification | NOT STARTED | 3.4 | Output matches `Doctor: "..."` / `Patient: "..."` format |
| 3.8 | Test: single-speaker edge case | NOT STARTED | 3.1 | One speaker ID → one role mapped, no crash |

## Verification Checklist

- [ ] `streamlit run app.py` launches without errors
- [ ] Speaker assignment radio appears after transcription completes
- [ ] Default is Speaker 0 = Doctor
- [ ] Toggling radio updates transcript labels (Doctor/Patient) without re-transcribing
- [ ] `format_transcript_for_llm()` returns correct `Role: "text"` format
- [ ] Unmapped speaker IDs fall back to `"Speaker N"` in display and LLM transcript
- [ ] Single-speaker audio: no crash, one role label shown
- [ ] `st.session_state.llm_transcript` contains formatted string after transcription
- [ ] Empty transcript: no errors, empty `llm_transcript`

## Issues

| # | Date | Issue | Resolution |
|---|------|-------|------------|
| — | — | — | — |

## Next

-> Phase 4: Note generation with Claude API. Prerequisite: `llm_transcript` available in session state with Doctor/Patient labels.
