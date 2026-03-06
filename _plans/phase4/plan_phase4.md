# Phase 4: Claude-Powered Consultation Note Generation — Plan & Context

> **Goal:** Generate structured consultation notes from the diarized, role-labeled transcript using the Claude API.
> **Outcome:** Note generation implemented. `note_generator.py` with system prompt, flat-string JSON schema, extract-only guardrails, sentinel values. UI wired with Generate Notes button and expandable section display.

---

## Pre-Conditions

- Phase 3 complete: `st.session_state.llm_transcript` available with `Doctor: "..."` / `Patient: "..."` format
- Anthropic API key set in `.env` (already configured in `config.py` as `ANTHROPIC_API_KEY`)
- `anthropic` SDK installed (already in `requirements.txt`)

---

## 1. Module Design (`note_generator.py`)

A single new module containing all note generation logic. Follows the same patterns established in `transcriber.py` — public function wrapping API call, private helpers for message building / response parsing, errors raised as `ValueError` (config issues) or `RuntimeError` (API/parse failures).

### Constants

**`SYSTEM_PROMPT`** — A multi-line string that defines Claude's role and instructions. The exact wording and structure require deliberate design (see task 4.R1 in tracker). Key areas to decide during prompt design:
- Role framing (e.g. "medical scribe assistant" — but exact wording matters for output quality)
- How to instruct extraction for each of the 14 sections from `masterplan.md` Section 3.1
- Whether to include few-shot examples or rely on the template alone
- How to handle partially-discussed sections (e.g. PMH mentioned but incomplete)
- Sentinel value strategy: suggested starting point is `"Not discussed"` for clinical sections, `"Not provided"` for patient info fields — but alternatives exist
- Anti-hallucination guardrails: extract-only instructions, zero temperature, no-embellishment rules (see Section 3 for details)
- Output format instructions: JSON output, fence handling

**`NOTE_SECTIONS`** — Ordered list of `(key, label)` tuples for the 13 top-level JSON keys. Used by both the prompt (to define expected schema) and the UI (to render sections in order):
1. `("patient_information", "Patient Information")`
2. `("chief_complaint", "Chief Complaint")`
3. `("history_of_present_illness", "History of Present Illness")`
4. `("past_medical_history", "Past Medical History")`
5. `("medications", "Medications")`
6. `("allergies", "Allergies")`
7. `("social_history", "Social History")`
8. `("family_history", "Family History")`
9. `("review_of_systems", "Review of Systems")`
10. `("physical_examination", "Physical Examination")`
11. `("diagnostic_data", "Diagnostic Data")`
12. `("assessment", "Assessment")`
13. `("plan", "Plan")`

**`PATIENT_INFO_FIELDS`** — Ordered list of `(key, label)` tuples for the nested `patient_information` dict:
1. `("name", "Name")`
2. `("date_of_birth", "Date of Birth")`
3. `("date_of_service", "Date of Service")`
4. `("referring_physician", "Referring Physician")`
5. `("specialty", "Specialty")`

### Functions

**`generate_notes(transcript: str, patient_info: dict | None = None) -> dict`** — Main public function.
- Validates that `ANTHROPIC_API_KEY` is set (raises `ValueError` if not)
- Validates that `transcript` is non-empty (raises `ValueError` if empty)
- Calls Claude API: `claude-sonnet-4-20250514`, `max_tokens=4096`, `temperature=0.0`
- Delegates to `_build_user_message()`, `_parse_response()`, `_validate_note()`
- Returns a dict matching the JSON schema
- Wraps API errors as `RuntimeError`

**`_build_user_message(transcript: str, patient_info: dict | None) -> str`** — Combines the transcript with optional patient info into the user message content.
- Always includes: `"## Transcript\n{transcript}"`
- If `patient_info` is provided and non-empty, prepends: `"## Patient Information\n{formatted fields}"`
- Patient info is included so Claude can echo it back into the note's patient_information section

**`_parse_response(text: str) -> dict`** — Extracts JSON from Claude's response text.
- Primary: `json.loads(text)` on the raw response
- Fallback: strip markdown JSON fences (` ```json ... ``` `) and retry `json.loads()`
- Raises `RuntimeError` if neither approach yields valid JSON

**`_validate_note(note: dict) -> dict`** — Ensures all expected sections exist in the parsed dict.
- Iterates `NOTE_SECTIONS`: if a key is missing, sets it to `"Not discussed"` (or an empty dict for `patient_information`)
- For `patient_information`: iterates `PATIENT_INFO_FIELDS`, backfills missing fields with `"Not provided"`
- Returns the completed dict

---

## 2. JSON Output Schema

The exact JSON schema requires a design decision (see task 4.R2 in tracker). The core question: **should clinical sections be flat strings or structured types?**

`masterplan.md` Section 3.1 shows structure within several sections:
- **Physical Examination** — has Vitals (key-value pairs) + General + system-specific sub-findings
- **Assessment** — numbered problem list with clinical reasoning
- **Plan** — numbered items corresponding to assessment, each with sub-bullets
- **Medications** — list of medication + dosage pairs
- **ROS** — findings grouped by body system

**Suggested starting approach:** `patient_information` as a nested dict with 5 string fields; all 12 clinical sections as flat strings. This prioritizes parsing simplicity — Claude writes each section as a free-text narrative, and the UI renders them directly. The tradeoff is that downstream processing (e.g. extracting individual medications or plan items) would require re-parsing text.

**Alternative:** Use lists or nested objects for structured sections (medications, assessment, plan). This preserves structure but complicates both the prompt and the parser.

The research task should evaluate both approaches against the sample note in `masterplan.md` Section 3.3 to determine what level of structure is worth the complexity.

Suggested baseline schema (flat strings):

```
{
  "patient_information": {
    "name": "...",
    "date_of_birth": "...",
    "date_of_service": "...",
    "referring_physician": "...",
    "specialty": "..."
  },
  "chief_complaint": "...",
  "history_of_present_illness": "...",
  "past_medical_history": "...",
  "medications": "...",
  "allergies": "...",
  "social_history": "...",
  "family_history": "...",
  "review_of_systems": "...",
  "physical_examination": "...",
  "diagnostic_data": "...",
  "assessment": "...",
  "plan": "..."
}
```

---

## 3. Anti-Hallucination Guardrails

Medical note generation must not fabricate clinical information. The following are **suggested guardrail strategies** to evaluate during prompt design (task 4.R1):

1. **Extract only** — Instruct Claude to only include information explicitly stated in the transcript. Exact wording needs testing.
2. **Sentinel values** — Use a consistent marker (suggested: `"Not discussed"`) for sections not covered in the conversation. Open questions:
   - Should partially-discussed sections (e.g. patient mentions one medication but the full list isn't reviewed) use a different marker or a note like "Partially discussed"?
   - Should the sentinel be a fixed string or something more descriptive per section?
3. **Zero temperature** — `temperature=0.0` reduces creative variation. Worth confirming this doesn't degrade extraction quality.
4. **No embellishment** — Explicit instruction not to add clinical details, differentials, or recommendations the doctor didn't state.

These are not foolproof (see `masterplan.md` Section 8) but are appropriate for a learning project. The prompt design research task should test these strategies against the sample note in `masterplan.md` Section 3.3.

---

## 4. Error Handling

Same pattern as `transcriber.py`:
- `ValueError` for configuration issues (missing API key, empty transcript)
- `RuntimeError` for API failures (network errors, authentication, rate limits) and parse failures (invalid JSON response)
- All errors caught and displayed via `st.error()` in `app.py`

---

## 5. UI Integration (`app.py`)

### Anthropic API Key Warning

Same pattern as the existing Deepgram/ElevenLabs key warnings — check `ANTHROPIC_API_KEY` against empty / placeholder value. Displayed at the top of the page alongside existing provider warnings.

### Generate Notes Button

- Visible only when `st.session_state.llm_transcript` exists (Phase 3 complete)
- `st.button("Generate Notes")` with a spinner: `"Generating consultation notes..."`
- On success: stores result in `st.session_state.notes` and latency in `st.session_state.notes_latency_msg`
- On error: displays `st.error()` with the exception message

### Note Display

- Rendered below the transcript section
- Each section rendered as an `st.expander()` with the section label as the header
- Sections with actual content: expanded by default
- Sections containing `"Not discussed"` or `"Not provided"`: collapsed by default, with dimmed text styling
- `patient_information` rendered as a key-value list inside its expander
- All other sections rendered as plain text / markdown

### New Session State Keys

| Key | Type | Description |
|-----|------|-------------|
| `notes` | `dict` | Parsed consultation note from Claude |
| `notes_latency_msg` | `str` | e.g. `"Notes generated in 3.2s"` |

---

## 6. Files Changed

| File | Changes |
|------|---------|
| `note_generator.py` | **New file.** All constants and functions described in Section 1 |
| `app.py` | Add Anthropic key warning, Generate Notes button, note display with expanders |

No changes to `config.py` (already has `ANTHROPIC_API_KEY` and `CLAUDE_MODEL`). No changes to `transcriber.py`.

---

## 7. What Phase 4 Does NOT Do

These are deferred to Phase 5:
- Patient info sidebar form (manual entry of name, DOB, etc.)
- Download Notes button (Markdown export)
- Error handling polish (empty/short recordings, timeout handling)
