# AI Medical Scriber - v1 Progress Tracker

> **Last Updated:** 2026-03-07
> **Status:** v1 development starting
> **v0 Archive:** [`v0_archive/`](v0_archive/README.md) — completed Phases 0–6

---

## v1 Feature Progress

### Priority 1 — Deploy & Export

| # | Feature | Status | Docs |
|---|---------|--------|------|
| v1.1 | Deployment | NOT STARTED | |
| v1.7 | PDF export | NOT STARTED | |

### Priority 2 — Harden & Expand

| # | Feature | Status | Docs |
|---|---------|--------|------|
| v1.2 | Prompt iteration | NOT STARTED | |
| v1.3 | Error recovery | NOT STARTED | |
| v1.4 | Cost tracking | NOT STARTED | |
| v1.5 | Recording consent notice | NOT STARTED | |
| v1.6 | Editable notes | NOT STARTED | |
| v1.8 | Persistence | NOT STARTED | |
| v1.9 | Note accuracy validation | NOT STARTED | |
| v1.10 | Longer consultation testing | NOT STARTED | |
| v1.11 | Audio preprocessing | NOT STARTED | |
| v1.12 | Multi-speaker support (>2) | NOT STARTED | |

### Priority 3 — Advanced / Architectural

| # | Feature | Status | Docs |
|---|---------|--------|------|
| v1.13 | Multiple note templates | NOT STARTED | |
| v1.14 | Specialty-specific prompts | NOT STARTED | |
| v1.15 | Real-time transcription | NOT STARTED | |
| v1.16 | Local/private mode | NOT STARTED | |
| v1.17 | React UI | NOT STARTED | |
| v1.18 | HIPAA compliance | NOT STARTED | |

**Status legend:** NOT STARTED | IN PROGRESS | DONE

---

## Provider Comparison Results

*Baseline from v0 Phase 6 testing (2026-03-07). Full detail → [`v0_archive/phase6/tracker_phase6.md`](v0_archive/phase6/tracker_phase6.md)*

| Script | DG Terms | EL Terms | DG Latency | EL Latency |
|--------|----------|----------|------------|------------|
| Ortho — Knee Pain | 12/13 (92%) | 13/13 (100%) | 25.4s | 46.7s |
| Cardio — Chest Pain | 13/14 (93%) | 13/14 (93%) | 24.5s | 44.2s |
| Multi-Problem — Follow-up | 12/15 (80%) | 14/15 (93%) | 29.9s | 43.9s |

| Category | Winner | Detail |
|----------|--------|--------|
| Term accuracy | **ElevenLabs** | 95% avg vs 88% avg |
| Diarization quality | **ElevenLabs** | Utterance counts match script |
| Latency | **Deepgram** | 26.6s avg vs 45.0s avg |
| Overall | **ElevenLabs** | Superior accuracy outweighs latency disadvantage |

---

## Issues & Bugs Log

*v0 issues → [`v0_archive/tracker_master_v0.md`](v0_archive/tracker_master_v0.md)*

| # | Date | Feature | Description | Status | Resolution |
|---|------|---------|-------------|--------|------------|
| | | | | | |

---

## Decisions Log

*Entries 1–9 → [`v0_archive/tracker_master_v0.md`](v0_archive/tracker_master_v0.md)*

| # | Date | Decision | Reasoning |
|---|------|----------|-----------|
| 10 | 2026-03-07 | Archive v0 docs, restructure for v1 | v0 complete; switch from sequential phases to feature-based workflow. Archive preserves history, slimmer master files focus on v1 |

---

## Files Inventory

| File | Purpose | Status |
|------|---------|--------|
| `app.py` | Main Streamlit app (UI + orchestration) | Active |
| `transcriber.py` | Deepgram + ElevenLabs transcription | Active |
| `note_generator.py` | Claude API note generation + download formatting | Active |
| `compare.py` | Test comparison logic (term accuracy, diarization, reports) | Active |
| `config.py` | Shared config, constants, medical keyterms | Active |
| `requirements.txt` | Python dependencies | Active |
| `.env` | API keys (not committed) | Active |
| `.gitignore` | Git ignore rules | Active |
| `pages/test_runner.py` | Automated test UI (dual-provider pipeline, metrics) | Active |
| `sample_scripts/ortho_knee_pain.md` | Ortho test script (knee pain, 58yo male) | Active |
| `sample_scripts/cardio_chest_pain.md` | Cardio test script (chest pain, 55yo female) | Active |
| `sample_scripts/multi_problem_followup.md` | Multi-problem test script (DM + HTN + GERD, 65yo male) | Active |
| `_plans/masterplan.md` | Project design reference (v1-focused) | Active |
| `_plans/tracker_master.md` | This tracker (v1 feature progress) | Active |
| `_plans/features/TEMPLATE.md` | Feature plan + tracker templates | Active |
| `_plans/v0_archive/` | Completed v0 phase docs (Phases 0–6) | Archived |
