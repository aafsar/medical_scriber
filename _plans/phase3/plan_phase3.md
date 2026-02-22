# Phase 3: Speaker Role Mapping — Plan & Context

> **Goal:** Map numeric speaker IDs (Speaker 0/1) to semantic roles (Doctor/Patient) for transcript display and LLM input formatting.
> **Outcome:** [filled after completion]

---

## Pre-Conditions

- Phase 1 or Phase 2 working: diarized transcript available as `list[Utterance]` with `speaker: int`
- `app.py` already displays transcript lines as `**Speaker {N}**: text`
- `Utterance` dataclass defined in `transcriber.py`

---

## 1. Speaker Assignment UI

A single radio widget lets the user declare which speaker is the doctor:

```
st.radio("Speaker 0 is:", ["Doctor", "Patient"], horizontal=True)
```

Placement: between the latency caption and the transcript display, so the user sees it immediately after transcription completes.

**Default:** Speaker 0 = Doctor. The other speaker's role is inferred automatically (if Speaker 0 is Doctor, Speaker 1 is Patient, and vice versa).

This approach avoids dropdowns for each speaker — with exactly two participants, one radio button fully determines both roles.

---

## 2. Session State

Two new keys added to `st.session_state`:

| Key | Type | Description |
|-----|------|-------------|
| `speaker_map` | `dict[int, str]` | Maps speaker ID → role label, e.g. `{0: "Doctor", 1: "Patient"}` |
| `llm_transcript` | `str` | Formatted transcript for Phase 4 LLM input |

`speaker_map` is rebuilt whenever the radio selection changes. `llm_transcript` is generated from the current utterances + speaker map and stored for Phase 4 to consume.

---

## 3. LLM Transcript Formatting

A new function in `transcriber.py` converts the raw utterance list into the format Claude expects in Phase 4:

```
def format_transcript_for_llm(utterances: list[Utterance], speaker_map: dict[int, str]) -> str
```

**Output format:**
```
Doctor: "Chief complaint is right knee pain for about three weeks."
Patient: "Yeah, it started after I went hiking."
Doctor: "Any swelling or instability?"
```

Each utterance becomes one line: `{Role}: "{text}"`. The function joins all lines with newlines.

**Fallback:** If a speaker ID is not in `speaker_map` (e.g. a third speaker in unexpected multi-speaker audio), fall back to `"Speaker N"` as the label.

---

## 4. Display Changes

The transcript display in `app.py` currently shows `**Speaker {N}**:`. After Phase 3, it uses `speaker_map` to show `**Doctor**:` or `**Patient**:` instead. The mapping is applied inline when rendering — no changes to the stored `Utterance` objects.

---

## 5. Edge Cases

| Scenario | Behavior |
|----------|----------|
| **Single speaker** | Only one speaker ID in utterances. The radio still works — the mapped role applies to that speaker, the other role simply doesn't appear. |
| **More than 2 speakers** | Unexpected for doctor-patient consultations. Unmapped speaker IDs fall back to `"Speaker N"` in both display and LLM transcript. |
| **Empty transcript** | No utterances to map. `llm_transcript` is an empty string. UI shows nothing. |

---

## 6. Files Changed

| File | Changes |
|------|---------|
| `transcriber.py` | Add `format_transcript_for_llm()` function |
| `app.py` | Add speaker assignment radio, update transcript display to use role labels, store `llm_transcript` in session state |

No changes to `config.py` — speaker mapping is purely UI/logic, no new API keys or constants needed.
