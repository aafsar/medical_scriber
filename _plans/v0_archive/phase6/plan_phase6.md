# Phase 6: End-to-End Testing — Plan & Context

> **Goal:** Validate the full pipeline (record → transcribe → diarize → label speakers → generate notes → download) with realistic consultation scripts, compare Deepgram vs ElevenLabs, and document results.
> **Outcome:** Testing complete. ElevenLabs wins term accuracy (95% vs 88%) and diarization quality; Deepgram wins latency (26.6s vs 45.0s). No code bugs found. Claude note generation robust against transcription errors.

---

## Pre-Conditions

- Phases 0–5 code-complete
- API keys configured in `.env` (Deepgram, ElevenLabs, Anthropic)
- Two people available to record scripts (Doctor + Patient voices)

---

## 1. Test Scripts

Three consultation scripts in `sample_scripts/`, each designed to exercise specific medical terminology and note sections. Scripts are written as two-person dialogues (Doctor / Patient) to be read aloud and recorded.

| Script | File | Specialty | Scenario | Duration | Key Challenge |
|--------|------|-----------|----------|----------|---------------|
| 1 | `sample_scripts/ortho_knee_pain.md` | Orthopedic Surgery | 58yo male, 3-week right knee pain | ~3-4 min | Dense ortho terminology, physical exam findings |
| 2 | `sample_scripts/cardio_chest_pain.md` | Cardiology | 55yo female, exertional chest pain | ~3-4 min | Cardiology keyterms, lab values, multi-step plan |
| 3 | `sample_scripts/multi_problem_followup.md` | Internal Medicine | 65yo male, DM + HTN + new GERD | ~4-5 min | Multi-problem assessment/plan, sentinel values for undiscussed sections |

### Script Design Rationale

- **Script 1 (Ortho)** mirrors the sample note in `masterplan.md` Section 3.3, providing a direct comparison between expected and generated output
- **Script 2 (Cardio)** introduces a different specialty and tests cardiology keyterms from `config.py`
- **Script 3 (Multi-Problem)** tests Claude's ability to generate a multi-problem assessment/plan, and intentionally omits family history to verify sentinel value handling

All scripts cover the 13 note sections defined in `note_generator.py` `NOTE_SECTIONS`, with Script 3 intentionally leaving family history undiscussed.

---

## 2. Medical Terminology Coverage

Terms drawn from `config.py` `MEDICAL_KEYTERMS` and distributed across scripts:

| Category | Script 1 (Ortho) | Script 2 (Cardio) | Script 3 (Multi-Problem) |
|----------|-------------------|--------------------|--------------------------|
| Conditions | osteoarthritis, hypertension, diabetes mellitus | hyperlipidemia, coronary artery disease | diabetes mellitus, hypertension, gastroesophageal reflux |
| Medications | metformin, lisinopril, diclofenac, ibuprofen | atorvastatin, amlodipine, metoprolol | metformin, lisinopril, hydrochlorothiazide, glipizide, omeprazole |
| Exam terms | effusion, crepitus, McMurray, Lachman, antalgic | murmur, auscultation, systolic | palpation, monofilament, neuropathy |
| Imaging/labs | X-ray, osteophyte, MRI | electrocardiogram, echocardiogram, troponin, ejection fraction | hemoglobin A1c, creatinine, BUN, microalbumin |
| General | medial, bilateral, palpation | dyspnea, palpitations, syncope | SpO2, BMI, retinopathy |

---

## 3. Automated Test Runner

An automated test runner pipeline was added to reduce manual effort. Recording is the only manual step — one button runs both providers, saves all outputs, and generates comparison reports with medical term accuracy metrics.

### Architecture

- **Separate Streamlit page** (`pages/test_runner.py`) — `app.py` untouched. Streamlit auto-detects `pages/` and adds sidebar navigation.
- **Pure logic module** (`compare.py`) — no Streamlit dependency. Handles script parsing, term checking, report generation.
- **No changes to production code** — test runner imports from existing `transcriber.py`, `note_generator.py`, `config.py`.

### Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Test UI location | `pages/test_runner.py` | Clean separation; `app.py` untouched |
| Speaker mapping | Auto: `{0: Doctor, 1: Patient}` | All scripts start with Doctor |
| Patient info | Auto-filled from script registry | Consistency across runs |
| Term matching | Case-insensitive substring | Specific medical terms won't false-match |
| Output structure | Timestamped session folders | Multiple test sessions without overwriting |

### Testing Protocol (Automated)

For each script:

1. Record script audio — two people reading Doctor/Patient parts in a quiet environment
2. Run `streamlit run app.py`, navigate to "Test Runner" in sidebar
3. Select script from dropdown (key terms + patient info auto-populate)
4. Upload/record audio, click "Run Full Test"
5. Pipeline runs both Deepgram and ElevenLabs sequentially, generates notes, computes metrics, saves 5 files per script
6. After all scripts tested, click "Generate Summary" for aggregate `test_summary.md`
7. Fill Phase 6 tracker comparison tables from summary results

### Automated Metrics

| Metric | How Measured |
|--------|-------------|
| Medical term accuracy | `compare.py` — case-insensitive substring check against "Key terms to verify" from script header |
| Diarization stats | `compare.py` — Doctor/Patient utterance counts, first-speaker check |
| Latency | Timed in `pages/test_runner.py` — transcription + note generation separately |

### Manual Metrics (not automated)

| Metric | How to Measure |
|--------|----------------|
| Note quality (1-5) | Subjective: review saved `*_notes.md` files |
| Diarization accuracy | Compare saved transcripts side-by-side with original scripts |

### Output Structure

```
test_results/{YYYY-MM-DD_HHMMSS}/
  ortho_knee_pain/
    deepgram_transcript.md
    deepgram_notes.md
    elevenlabs_transcript.md
    elevenlabs_notes.md
    comparison.md
  cardio_chest_pain/...
  multi_problem_followup/...
  test_summary.md
```

---

## 4. What This Phase Does NOT Do

- No new providers — this establishes the Deepgram vs ElevenLabs baseline for future provider evaluation (see `masterplan.md` Section 2.2)
