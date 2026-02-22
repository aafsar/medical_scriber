# AI Medical Scriber - Master Progress Tracker

> **Last Updated:** 2026-02-22
> **Status:** Phase 1 Done (e2e test pending real API key), Ready for Phase 2

---

## Overall Progress

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 0: Project Setup | DONE | API keys pending (manual) |
| Phase 1: Audio + Deepgram Transcription | DONE | e2e test pending real API key |
| Phase 2: ElevenLabs Transcription | NOT STARTED | |
| Phase 3: Speaker Role Mapping | NOT STARTED | |
| Phase 4: Note Generation (Claude) | NOT STARTED | |
| Phase 5: Patient Info + Polish | NOT STARTED | |
| Phase 6: End-to-End Testing | NOT STARTED | |

**Status legend:** NOT STARTED | IN PROGRESS | DONE | BLOCKED

---

## Phase 0: Project Setup

**Status:** DONE (API keys pending). Details → [`_plans/phase0/tracker_phase0.md`](phase0/tracker_phase0.md)

---

## Phase 1: Audio Recording + Deepgram Transcription

**Status:** DONE (e2e test pending real API key). Details → [`_plans/phase1/tracker_phase1.md`](phase1/tracker_phase1.md)

---

## Phase 2: ElevenLabs Transcription

| Task | Status | Notes |
|------|--------|-------|
| Implement `transcribe_elevenlabs()` function | NOT STARTED | `scribe_v2`, `diarize=True` |
| Create medical `keyterms` list in `config.py` | NOT STARTED | Up to 100 terms |
| Reconstruct utterances from word-level speaker_id | NOT STARTED | ElevenLabs returns word-level, not utterance-level |
| Add provider toggle in UI (radio/selectbox) | NOT STARTED | `[Deepgram] / [ElevenLabs]` |
| Test with same audio on both providers | NOT STARTED | |
| Compare: medical term accuracy | NOT STARTED | |
| Compare: diarization accuracy | NOT STARTED | |
| Compare: latency | NOT STARTED | |

**Blockers:** Requires ElevenLabs API key from Phase 0.

---

## Phase 3: Speaker Role Mapping

| Task | Status | Notes |
|------|--------|-------|
| Add speaker assignment UI (radio buttons) | NOT STARTED | "Speaker 0 is: Doctor / Patient" |
| Default first speaker = Doctor | NOT STARTED | |
| Re-label transcript with Doctor/Patient tags | NOT STARTED | |
| Format transcript for LLM input | NOT STARTED | `Doctor: "..."` / `Patient: "..."` |

**Blockers:** Requires Phase 1 or 2 working.

---

## Phase 4: Note Generation with Claude

| Task | Status | Notes |
|------|--------|-------|
| Create `note_generator.py` | NOT STARTED | |
| Write system prompt with note template | NOT STARTED | Consultation note format from plan Section 3.1 |
| Add guardrails to prompt | NOT STARTED | No hallucination, mark "Not discussed" sections |
| Request JSON output matching template schema | NOT STARTED | |
| Implement `generate_notes()` function | NOT STARTED | Input: transcript + patient_info, Output: dict |
| Parse JSON response + handle edge cases | NOT STARTED | Missing sections, malformed output |
| Display formatted notes in UI | NOT STARTED | Expandable sections, dimmed "Not discussed" |
| Test with sample transcript | NOT STARTED | |

**Blockers:** Requires Phase 3 (labeled transcript) and Anthropic API key.

---

## Phase 5: Patient Info + Polish

| Task | Status | Notes |
|------|--------|-------|
| Add sidebar form for patient metadata | NOT STARTED | Name, DOB, Date of Service, Specialty |
| Add Referring Physician field (optional) | NOT STARTED | |
| Add Specialty dropdown | NOT STARTED | Ortho, Cardio, Neuro, GI, Derm, etc. |
| Merge patient info into note header | NOT STARTED | |
| Add "Download Notes" button (Markdown) | NOT STARTED | |
| Error handling: no audio recorded | NOT STARTED | |
| Error handling: API failures | NOT STARTED | Timeout, auth errors |
| Error handling: empty/short recordings | NOT STARTED | |
| Add processing spinners + status messages | NOT STARTED | |

**Blockers:** Requires Phase 4 working.

---

## Phase 6: End-to-End Testing

| Task | Status | Notes |
|------|--------|-------|
| Write ortho consultation script | NOT STARTED | Knee pain scenario |
| Write cardio consultation script | NOT STARTED | Chest pain scenario |
| Write multi-problem follow-up script | NOT STARTED | General scenario |
| Record ortho script | NOT STARTED | |
| Record cardio script | NOT STARTED | |
| Record multi-problem script | NOT STARTED | |
| Run ortho through full pipeline (both providers) | NOT STARTED | |
| Run cardio through full pipeline (both providers) | NOT STARTED | |
| Run multi-problem through full pipeline | NOT STARTED | |
| Document provider comparison results | NOT STARTED | See comparison section below |
| Identify and fix issues found | NOT STARTED | |

**Blockers:** Requires all prior phases working.

---

## Provider Comparison Results

*To be filled after Phase 6 testing.*

### Test 1: Orthopedic Consultation

| Metric | Deepgram | ElevenLabs | Winner |
|--------|----------|------------|--------|
| Medical term accuracy | | | |
| Diarization accuracy | | | |
| Latency (seconds) | | | |
| Note quality (1-5) | | | |

### Test 2: Cardiology Consultation

| Metric | Deepgram | ElevenLabs | Winner |
|--------|----------|------------|--------|
| Medical term accuracy | | | |
| Diarization accuracy | | | |
| Latency (seconds) | | | |
| Note quality (1-5) | | | |

### Test 3: Multi-Problem Follow-up

| Metric | Deepgram | ElevenLabs | Winner |
|--------|----------|------------|--------|
| Medical term accuracy | | | |
| Diarization accuracy | | | |
| Latency (seconds) | | | |
| Note quality (1-5) | | | |

### Overall Winner: *TBD*

---

## Issues & Bugs Log

| # | Date | Phase | Description | Status | Resolution |
|---|------|-------|-------------|--------|------------|
| | | | | | |

---

## Decisions Log

| # | Date | Decision | Reasoning |
|---|------|----------|-----------|
| 1 | 2026-02-21 | Use Streamlit for UI | Pure Python, built-in audio recording, fastest to prototype |
| 2 | 2026-02-21 | Compare Deepgram vs ElevenLabs | Both offer diarization; compare quality for medical use |
| 3 | 2026-02-21 | Use Claude API for note generation | Best structured extraction, strong guardrails against hallucination |
| 4 | 2026-02-21 | Hybrid SOAP/H&P note format | Covers CMS essentials, mirrors real specialist EHR output |
| 5 | 2026-02-21 | No database for v1 | Download notes as files; simplicity over persistence |
| 6 | 2026-02-22 | Python 3.14.3 (no fallback needed) | Latest stable, all 5 deps have 3.14 wheels |
| 7 | 2026-02-22 | Private GitHub repo | `aafsar/medical_scriber` |

---

## Files Inventory

| File | Purpose | Status |
|------|---------|--------|
| `_plans/masterplan.md` | Detailed project plan | DONE |
| `tracker_master.md` | This progress tracker | DONE |
| `app.py` | Main Streamlit app | DONE (Phase 1) |
| `transcriber.py` | Deepgram + ElevenLabs logic | DONE (Deepgram) |
| `note_generator.py` | Claude API note generation | NOT STARTED |
| `_plans/phase1/plan_phase1.md` | Phase 1 design doc | DONE |
| `_plans/phase1/tracker_phase1.md` | Phase 1 task tracker | DONE |
| `config.py` | Shared config, medical keyterms | DONE |
| `requirements.txt` | Python dependencies | DONE |
| `.env` | API keys (placeholder) | DONE |
| `.gitignore` | Git ignore rules | DONE |
| `sample_scripts/ortho_knee_pain.md` | Test script | NOT STARTED |
| `sample_scripts/cardio_chest_pain.md` | Test script | NOT STARTED |
