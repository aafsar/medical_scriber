# Phase 6: End-to-End Testing — Plan & Context

> **Goal:** Validate the full pipeline (record → transcribe → diarize → label speakers → generate notes → download) with realistic consultation scripts, compare Deepgram vs ElevenLabs, and document results.
> **Outcome:** [filled after completion]

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

## 3. Testing Protocol

For each script (3 scripts x 2 providers = 6 total runs):

1. Record script audio — two people reading Doctor/Patient parts in a quiet environment
2. Open `streamlit run app.py`
3. Fill in patient info sidebar (name, DOB, date of service, referring physician, specialty)
4. Upload recording, select provider (Deepgram or ElevenLabs), click Transcribe
5. Set Speaker 0 role correctly (Doctor or Patient based on who speaks first)
6. Review transcript for medical term errors and diarization mistakes
7. Click Generate Notes
8. Compare generated note against expected content from script
9. Download the `.md` file
10. Record metrics in Phase 6 tracker comparison tables

### Metrics

| Metric | How to Measure |
|--------|----------------|
| Medical term accuracy | Count correctly transcribed keyterms / total keyterms in script |
| Diarization accuracy | Count correctly attributed utterances / total utterances |
| Latency | Note the time displayed by the app (transcription + note generation) |
| Note quality (1-5) | Subjective: completeness, accuracy, formatting, no hallucinations |

---

## 4. What This Phase Does NOT Do

- No automated tests — all testing is manual with real audio recordings
- No code changes (unless bugs are found during testing)
- No new providers — this establishes the Deepgram vs ElevenLabs baseline for future provider evaluation (see `masterplan.md` Section 2.2)
