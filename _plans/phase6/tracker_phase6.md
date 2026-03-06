# Phase 6: End-to-End Testing — Tracker

> **Last Updated:** 2026-03-06
> **Phase Status:** IN PROGRESS

---

## Implementation Order

| # | Task | Status | Depends On | Notes |
|---|------|--------|------------|-------|
| 6.1 | Write ortho consultation script | DONE | — | `sample_scripts/ortho_knee_pain.md` |
| 6.2 | Write cardio consultation script | DONE | — | `sample_scripts/cardio_chest_pain.md` |
| 6.3 | Write multi-problem follow-up script | DONE | — | `sample_scripts/multi_problem_followup.md` |
| 6.4 | Record ortho script audio | NOT STARTED | 6.1 | Two speakers, quiet environment |
| 6.5 | Record cardio script audio | NOT STARTED | 6.2 | Two speakers, quiet environment |
| 6.6 | Record multi-problem script audio | NOT STARTED | 6.3 | Two speakers, quiet environment |
| 6.7 | Run ortho through pipeline (Deepgram) | NOT STARTED | 6.4 | Fill comparison table below |
| 6.8 | Run ortho through pipeline (ElevenLabs) | NOT STARTED | 6.4 | Fill comparison table below |
| 6.9 | Run cardio through pipeline (Deepgram) | NOT STARTED | 6.5 | Fill comparison table below |
| 6.10 | Run cardio through pipeline (ElevenLabs) | NOT STARTED | 6.5 | Fill comparison table below |
| 6.11 | Run multi-problem through pipeline (Deepgram) | NOT STARTED | 6.6 | Fill comparison table below |
| 6.12 | Run multi-problem through pipeline (ElevenLabs) | NOT STARTED | 6.6 | Fill comparison table below |
| 6.13 | Document provider comparison results | NOT STARTED | 6.7–6.12 | Summarize findings, pick winner |
| 6.14 | Identify and fix issues found | NOT STARTED | 6.7–6.12 | Log bugs, fix, re-test |

---

## Provider Comparison Results

*To be filled during testing.*

### Test 1: Orthopedic Consultation

| Metric | Deepgram | ElevenLabs | Winner |
|--------|----------|------------|--------|
| Medical term accuracy | | | |
| Diarization accuracy | | | |
| Latency (seconds) | | | |
| Note quality (1-5) | | | |

**Deepgram transcript notes:**

**ElevenLabs transcript notes:**

**Generated note observations:**

### Test 2: Cardiology Consultation

| Metric | Deepgram | ElevenLabs | Winner |
|--------|----------|------------|--------|
| Medical term accuracy | | | |
| Diarization accuracy | | | |
| Latency (seconds) | | | |
| Note quality (1-5) | | | |

**Deepgram transcript notes:**

**ElevenLabs transcript notes:**

**Generated note observations:**

### Test 3: Multi-Problem Follow-up

| Metric | Deepgram | ElevenLabs | Winner |
|--------|----------|------------|--------|
| Medical term accuracy | | | |
| Diarization accuracy | | | |
| Latency (seconds) | | | |
| Note quality (1-5) | | | |

**Deepgram transcript notes:**

**ElevenLabs transcript notes:**

**Generated note observations (especially multi-problem handling + sentinel values):**

### Overall Winner: *TBD*

---

## Verification Checklist

- [x] 3 consultation scripts exist in `sample_scripts/`
- [x] Scripts cover diverse medical terminology from `config.py` keyterms
- [x] Scripts exercise all 13 note sections (Script 3 intentionally omits family history)
- [x] Phase 6 plan + tracker docs follow project templates
- [x] Master tracker updated with Phase 6 link
- [ ] Ortho script recorded
- [ ] Cardio script recorded
- [ ] Multi-problem script recorded
- [ ] All 6 pipeline runs completed (3 scripts x 2 providers)
- [ ] Comparison tables filled
- [ ] Issues logged and resolved
- [ ] Overall winner determined

---

## Issues

| # | Date | Issue | Resolution |
|---|------|-------|------------|
| — | — | — | — |

---

## Next

-> Provider evaluation backlog (masterplan Section 2.2): use same test recordings to benchmark additional providers (AssemblyAI, OpenAI Whisper, etc.). Prerequisites: Phase 6 baseline comparison complete.
