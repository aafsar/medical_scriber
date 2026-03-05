# Phase 4: Claude-Powered Consultation Note Generation — Tracker

> **Last Updated:** 2026-02-22
> **Phase Status:** NOT STARTED

---

## Implementation Order

| # | Task | Status | Depends On | Notes |
|---|------|--------|------------|-------|
| 4.R1 | **Research:** Design system prompt + guardrail strategy | NOT STARTED | — | Draft prompt wording, test extraction style, decide sentinel values, evaluate partial-section handling. See plan Sections 1 & 3. |
| 4.R2 | **Research:** Design JSON output schema | NOT STARTED | — | Flat strings vs structured types for clinical sections. Evaluate against sample note in `masterplan.md` Section 3.3. See plan Section 2. |
| 4.1 | Define `SYSTEM_PROMPT` constant in `note_generator.py` | NOT STARTED | 4.R1 | Implement prompt based on research findings |
| 4.2 | Define `NOTE_SECTIONS` and `PATIENT_INFO_FIELDS` constants | NOT STARTED | 4.R2 | Ordered `(key, label)` tuples — structure depends on schema decision |
| 4.3 | Implement `_build_user_message()` | NOT STARTED | — | Combines transcript + optional patient info |
| 4.4 | Implement `_parse_response()` | NOT STARTED | 4.R2 | JSON extraction — parsing logic depends on schema decision |
| 4.5 | Implement `_validate_note()` | NOT STARTED | 4.R1, 4.2 | Backfills missing sections — sentinel values depend on prompt design |
| 4.6 | Implement `generate_notes()` | NOT STARTED | 4.1–4.5 | Main public function: validate → call API → parse → validate |
| 4.7 | Add Anthropic API key warning in `app.py` | NOT STARTED | — | Same pattern as Deepgram/ElevenLabs warnings |
| 4.8 | Add Generate Notes button + spinner in `app.py` | NOT STARTED | 4.6 | Visible when `llm_transcript` exists, stores result in session state |
| 4.9 | Add note display with expanders in `app.py` | NOT STARTED | 4.2, 4.8 | Discussed sections expanded, "Not discussed" collapsed/dimmed |
| 4.10 | Test `_parse_response()` edge cases | NOT STARTED | 4.4 | Raw JSON, fenced JSON, malformed input |
| 4.11 | Test `_validate_note()` with incomplete dict | NOT STARTED | 4.5 | Missing sections backfilled, patient_information fields backfilled |
| 4.12 | End-to-end test with sample transcript | NOT STARTED | 4.6–4.9 | Full pipeline: transcript → notes → UI display |

## Verification Checklist

- [ ] `streamlit run app.py` launches without errors
- [ ] Anthropic API key warning appears when key is missing/placeholder
- [ ] Generate Notes button appears only when `llm_transcript` exists in session state
- [ ] Note renders all 13 sections (patient_information + 12 clinical sections)
- [ ] Sections with content are expanded by default
- [ ] "Not discussed" sections are collapsed and dimmed
- [ ] `patient_information` renders as key-value list inside expander
- [ ] No hallucinated content — sections not discussed in transcript show "Not discussed"
- [ ] Missing API key raises `ValueError` displayed via `st.error()`
- [ ] Empty transcript raises `ValueError` displayed via `st.error()`
- [ ] Malformed API response raises `RuntimeError` displayed via `st.error()`

## Issues

| # | Date | Issue | Resolution |
|---|------|-------|------------|
| — | — | — | — |

## Next

-> Phase 5: Patient info sidebar form, Download Notes button, error handling polish. Prerequisites: Phase 4 working (notes generated and displayed).
