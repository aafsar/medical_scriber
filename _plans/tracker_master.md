# AI Medical Scriber - Master Progress Tracker

> **Last Updated:** 2026-03-06
> **Status:** Phases 0–5 code-complete (e2e tests pending real API keys), ready for Phase 6

---

## Overall Progress

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 0: Project Setup | DONE | API keys pending (manual) |
| Phase 1: Audio + Deepgram Transcription | DONE | Code complete, e2e test pending real API key |
| Phase 2: ElevenLabs Transcription | DONE | Code complete, e2e test pending real API key |
| Phase 3: Speaker Role Mapping | DONE | Code complete, UI smoke tests pending |
| Phase 4: Note Generation (Claude) | DONE | Code complete, e2e test pending real API key |
| Phase 5: Patient Info + Polish | DONE | Sidebar form, download button, empty transcript guard |
| Phase 6: End-to-End Testing | IN PROGRESS | Scripts written, recording + testing pending |

**Status legend:** NOT STARTED | IN PROGRESS | DONE | BLOCKED

---

## Phase 0: Project Setup

**Status:** DONE (API keys pending). Details → [`_plans/phase0/tracker_phase0.md`](phase0/tracker_phase0.md)

---

## Phase 1: Audio Recording + Deepgram Transcription

**Status:** DONE (e2e test pending real API key). Details → [`_plans/phase1/tracker_phase1.md`](phase1/tracker_phase1.md)

---

## Phase 2: ElevenLabs Transcription

**Status:** DONE (code complete, e2e test pending real API key). Details → [`_plans/phase2/tracker_phase2.md`](phase2/tracker_phase2.md)

---

## Phase 3: Speaker Role Mapping

**Status:** DONE (code complete, UI smoke tests pending). Details → [`_plans/phase3/tracker_phase3.md`](phase3/tracker_phase3.md)

---

## Phase 4: Note Generation with Claude

**Status:** DONE (code complete, e2e test pending real API key). Details → [`_plans/phase4/tracker_phase4.md`](phase4/tracker_phase4.md)

---

## Phase 5: Patient Info + Polish

**Status:** DONE. Implemented 2026-03-06, no separate plan/tracker docs (small phase).

| Task | Status | Notes |
|------|--------|-------|
| Add sidebar form for patient metadata | DONE | Name, DOB, Date of Service, Referring Physician, Specialty |
| Add Specialty dropdown | DONE | 16 specialties in `config.py` `SPECIALTIES` tuple |
| Pass patient_info to generate_notes | DONE | Claude echoes patient details into note |
| Add "Download Notes" button (Markdown) | DONE | `build_download_markdown()` in `note_generator.py` |
| Error handling: empty/short recordings | DONE | Empty transcript guard with warning message |
| Processing spinners + status messages | DONE | Already existed from prior phases |

---

## Phase 6: End-to-End Testing

**Status:** IN PROGRESS (scripts written, recording + testing pending). Details → [`_plans/phase6/tracker_phase6.md`](phase6/tracker_phase6.md)

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
| 8 | 2026-02-22 | Expand provider evaluation backlog | 12 additional providers shortlisted (AssemblyAI, AWS, Azure, Cartesia, Google, Livekit, OpenAI, Pipecat, Retell, Rime, Speechmatics, Vapi). Evaluate after Phase 6 baseline using same test recordings. See masterplan Section 2.2 |

---

## Files Inventory

| File | Purpose | Status |
|------|---------|--------|
| `_plans/masterplan.md` | Detailed project plan | DONE |
| `_plans/tracker_master.md` | This progress tracker | DONE |
| `app.py` | Main Streamlit app | DONE (Phase 5) |
| `transcriber.py` | Deepgram + ElevenLabs transcription | DONE (Phase 3) |
| `note_generator.py` | Claude API note generation + download formatting | DONE (Phase 5) |
| `config.py` | Shared config, medical keyterms | DONE |
| `requirements.txt` | Python dependencies | DONE |
| `.env` | API keys (placeholder) | DONE |
| `.gitignore` | Git ignore rules | DONE |
| `_plans/phase0/` | Phase 0 plan + tracker | DONE |
| `_plans/phase1/` | Phase 1 plan + tracker | DONE |
| `_plans/phase2/` | Phase 2 plan + tracker | DONE |
| `_plans/phase3/` | Phase 3 plan + tracker | DONE |
| `_plans/phase4/` | Phase 4 plan + tracker | DONE |
| `_plans/phase5/` | Phase 5 plan + tracker | N/A (small phase, tracked in master) |
| `_plans/phase6/` | Phase 6 plan + tracker | DONE |
| `sample_scripts/ortho_knee_pain.md` | Ortho test script (knee pain, 58yo male) | DONE |
| `sample_scripts/cardio_chest_pain.md` | Cardio test script (chest pain, 55yo female) | DONE |
| `sample_scripts/multi_problem_followup.md` | Multi-problem test script (DM + HTN + GERD, 65yo male) | DONE |
