# Phase 4: Claude-Powered Consultation Note Generation — Tracker

> **Last Updated:** 2026-03-05
> **Phase Status:** DONE (code complete, e2e test pending real API key)

---

## Implementation Order

| # | Task | Status | Depends On | Notes |
|---|------|--------|------------|-------|
| 4.R1 | **Research:** Design system prompt + guardrail strategy | DONE | — | Extract-only rules, "Not discussed" / "Not provided" sentinels, temperature=0.0, no-embellishment instruction |
| 4.R2 | **Research:** Design JSON output schema | DONE | — | Flat strings for all clinical sections, nested dict for patient_information only |
| 4.1 | Define `SYSTEM_PROMPT` constant in `note_generator.py` | DONE | 4.R1 | 6 guardrail rules, explicit JSON schema in prompt |
| 4.2 | Define `NOTE_SECTIONS` and `PATIENT_INFO_FIELDS` constants | DONE | 4.R2 | Ordered tuples of `(key, label)` |
| 4.3 | Implement `_build_user_message()` | DONE | — | Combines transcript + optional patient info |
| 4.4 | Implement `_parse_response()` | DONE | 4.R2 | Raw JSON + markdown fence fallback |
| 4.5 | Implement `_validate_note()` | DONE | 4.R1, 4.2 | Backfills missing sections with sentinel values |
| 4.6 | Implement `generate_notes()` | DONE | 4.1–4.5 | Validates → calls API → parses → validates |
| 4.7 | Add Anthropic API key warning in `app.py` | DONE | — | Same pattern as Deepgram/ElevenLabs warnings |
| 4.8 | Add Generate Notes button + spinner in `app.py` | DONE | 4.6 | Visible when `llm_transcript` exists, clears on re-transcribe |
| 4.9 | Add note display with expanders in `app.py` | DONE | 4.2, 4.8 | Discussed sections expanded, "Not discussed" collapsed/dimmed |
| 4.10 | Test `_parse_response()` edge cases | DONE | 4.4 | Raw JSON, fenced JSON — both pass |
| 4.11 | Test `_validate_note()` with incomplete dict | DONE | 4.5 | Missing sections backfilled, patient_information fields backfilled |
| 4.12 | End-to-end test with real transcript | NOT STARTED | 4.6–4.9 | Requires real Anthropic API key |

## Verification Checklist

- [x] `python -c "from note_generator import ..."` imports without errors
- [x] `_parse_response()` handles raw JSON
- [x] `_parse_response()` handles markdown-fenced JSON
- [x] `_validate_note()` backfills missing sections with "Not discussed"
- [x] `_validate_note()` backfills missing patient_information fields with "Not provided"
- [x] Anthropic API key warning appears when key is missing/placeholder
- [x] Generate Notes button appears only when `llm_transcript` exists in session state
- [ ] Note renders all 13 sections (patient_information + 12 clinical sections)
- [ ] Sections with content are expanded by default
- [ ] "Not discussed" sections are collapsed and dimmed
- [ ] `patient_information` renders as key-value list inside expander
- [ ] No hallucinated content — sections not discussed in transcript show "Not discussed"

## Issues

| # | Date | Issue | Resolution |
|---|------|-------|------------|
| — | — | — | — |

## Next

-> Phase 5: Patient info sidebar form, Download Notes button, error handling polish. Prerequisites: Phase 4 working (notes generated and displayed).
