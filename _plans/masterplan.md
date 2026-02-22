# AI Medical Scriber - Project Plan

## 1. Project Overview

A toy AI medical scriber application for US specialists. The app records a doctor-patient consultation, transcribes the audio with speaker separation, and uses an LLM to auto-fill structured consultation notes.

**Core flow:**

```
Doctor presses Record --> Consultation happens --> Audio is processed
   --> Speakers separated (Doctor vs Patient) --> Consultation notes auto-generated
```

**Scope:** Learning project. Simple, functional, not enterprise-grade.

---

## 2. Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | Python | All SDKs available, fastest to develop |
| **UI** | Streamlit | Pure Python, built-in `st.audio_input()` for mic recording, zero frontend code |
| **Transcription + Diarization** | Deepgram (Nova-2 Medical) **and** ElevenLabs (Scribe v2) | Compare both; both have built-in diarization via a single flag |
| **Note Generation** | Claude API (Anthropic) | Best at structured extraction, 200K context, reliable with guardrails |
| **Config / Secrets** | python-dotenv + `.env` file | Simple, standard |

### 2.1 Transcription Provider Comparison

We will implement **both** providers and compare quality on the same recordings.

| Feature | Deepgram (Nova-2 Medical) | ElevenLabs (Scribe v2) |
|---------|--------------------------|------------------------|
| **Diarization** | `diarize=True` | `diarize=True` |
| **Medical model** | Yes (`nova-2-medical`) | No dedicated model, but supports `keyterms` (up to 100 medical terms) |
| **Free tier** | $200 signup credits | ~2.5 hrs/month on free plan |
| **Pricing** | ~$0.26/hr ($0.0043/min) | ~$0.40/hr |
| **Response format** | Utterances with speaker labels | Word-level objects with `speaker_id` |
| **Unique features** | Medical-specific vocabulary model | `keyterms` prompting, audio event tagging, entity detection (56 categories) |
| **Max file size** | 2 GB | 3 GB |
| **Python SDK** | `deepgram-sdk` | `elevenlabs` |

**What we'll compare:**
- Transcription accuracy (especially medical terms: drug names, conditions, procedures)
- Speaker diarization accuracy (correct doctor/patient attribution)
- Latency (time to get results back)
- Ease of integration

### 2.2 LLM for Note Generation

**Claude API** via the `anthropic` Python SDK.

- Model: `claude-sonnet-4-20250514` (good balance of quality and cost) or `claude-haiku-4-5-20251001` (faster/cheaper for iteration)
- A 15-minute consultation produces ~3,500 tokens of transcript
- Cost per note: ~$0.01 (Haiku) to ~$0.06 (Sonnet)
- Output format: structured JSON matching our consultation note template

---

## 3. Consultation Note Format

Based on US clinical documentation standards (CMS guidelines, SOAP/H&P formats). This is a simplified hybrid that mirrors what specialists actually produce in EHR systems like Epic or Cerner.

### 3.1 Template Sections

```
CONSULTATION NOTE
=================

PATIENT INFORMATION
  - Name
  - Date of Birth
  - Date of Service
  - Referring Physician (if applicable)
  - Specialty

CHIEF COMPLAINT (CC)
  The primary reason for the visit, in the patient's own words.
  Example: "My right knee has been hurting for about 3 weeks."

HISTORY OF PRESENT ILLNESS (HPI)
  Narrative of the current problem covering (OLDCARTS mnemonic):
  - Onset: When did it start?
  - Location: Where is the problem?
  - Duration: How long has it lasted?
  - Character: What does it feel/look like?
  - Aggravating factors: What makes it worse?
  - Relieving factors: What makes it better?
  - Timing: Is it constant, intermittent?
  - Severity: How bad is it (e.g., pain scale 1-10)?

PAST MEDICAL HISTORY (PMH)
  Prior diagnoses, surgeries, hospitalizations.

MEDICATIONS
  Current medications with dosages.

ALLERGIES
  Drug allergies with reaction type (e.g., Penicillin - rash).

SOCIAL HISTORY
  Smoking, alcohol, occupation, relevant lifestyle factors.

FAMILY HISTORY
  Relevant familial conditions.

REVIEW OF SYSTEMS (ROS)
  Pertinent positive and negative findings by body system.
  At minimum: Constitutional + systems relevant to chief complaint.

PHYSICAL EXAMINATION
  - Vitals: BP, HR, RR, Temp, SpO2, Weight, BMI
  - General appearance
  - System-specific exam findings relevant to the consultation

DIAGNOSTIC DATA (if discussed)
  Lab results, imaging reports, other test results.

ASSESSMENT
  Numbered problem list with diagnoses.
  Clinical reasoning linking findings to conclusions.

PLAN
  Numbered plan corresponding to assessment items:
  - Medications prescribed/changed
  - Therapies ordered (e.g., physical therapy)
  - Tests/imaging ordered
  - Procedures planned
  - Patient education provided
  - Follow-up timing and instructions
```

### 3.2 What Gets Auto-Filled vs. Manual

| Section | Auto-fillable from conversation? | Notes |
|---------|-------------------------------|-------|
| Patient Info | No | Manually entered before recording |
| Chief Complaint | Yes | Patient typically states this early |
| HPI | Yes | Core of patient's narrative |
| PMH | Partially | Often mentioned but may be incomplete |
| Medications | Partially | Discussed when relevant |
| Allergies | Partially | Usually confirmed by doctor |
| Social History | Partially | Sometimes discussed |
| Family History | Partially | Sometimes discussed |
| ROS | Yes | Doctor systematically asks |
| Physical Exam | Yes | Doctor narrates findings aloud |
| Diagnostic Data | Partially | Doctor may reference results |
| Assessment | Yes | Doctor states diagnosis |
| Plan | Yes | Doctor states treatment decisions |

### 3.3 Sample Filled Note (Orthopedic Consultation)

```
CONSULTATION NOTE
=================

PATIENT INFORMATION
  Name: John Smith
  DOB: 03/15/1967
  Date of Service: 02/18/2026
  Referring Physician: Dr. Sarah Chen (PCP)
  Specialty: Orthopedic Surgery

CHIEF COMPLAINT
  "My right knee has been hurting for about 3 weeks."

HISTORY OF PRESENT ILLNESS
  58-year-old male presents with a 3-week history of right knee pain.
  Pain is described as a dull ache, rated 6/10, localized to the medial
  aspect. Worse with prolonged standing and stair climbing. Partially
  relieved by ibuprofen 400mg. Denies trauma, locking, or giving way.
  Reports occasional morning stiffness lasting approximately 15 minutes.
  No swelling noted by patient.

PAST MEDICAL HISTORY
  - Hypertension
  - Type 2 Diabetes Mellitus

MEDICATIONS
  - Metformin 1000mg twice daily
  - Lisinopril 20mg daily

ALLERGIES
  - Penicillin (rash)

SOCIAL HISTORY
  Non-smoker, occasional alcohol use. Retired construction worker.

FAMILY HISTORY
  Mother with osteoarthritis. Father with coronary artery disease.

REVIEW OF SYSTEMS
  Constitutional: Denies fever, weight loss.
  Cardiovascular: Denies chest pain, shortness of breath.
  Musculoskeletal: Right knee pain and stiffness as described in HPI.
  Remainder of review of systems negative.

PHYSICAL EXAMINATION
  Vitals: BP 138/82, HR 76, Temp 98.4F, BMI 29.3
  General: Well-appearing male in no acute distress.
  Right Knee:
    - No erythema or ecchymosis
    - Mild effusion noted
    - Tenderness to palpation along medial joint line
    - Full extension, flexion limited to 120 degrees (left 135)
    - Positive McMurray test medially
    - Negative Lachman, negative anterior/posterior drawer
    - Varus/valgus stress stable
  Gait: Antalgic, favoring right side.
  Neurovascular: Sensation intact. DP/PT pulses 2+ bilaterally.

DIAGNOSTIC DATA
  X-ray Right Knee (2 views): Medial joint space narrowing, small
  osteophytes on medial tibial plateau. No fracture or loose bodies.

ASSESSMENT
  1. Right knee osteoarthritis, medial compartment (Kellgren-Lawrence
     Grade II). Consistent with occupational loading history. Possible
     degenerative medial meniscus tear given positive McMurray.
  2. Hypertension - slightly elevated today, likely pain-related.
  3. Type 2 Diabetes Mellitus - stable per patient.

PLAN
  1. Right knee osteoarthritis:
     - Physical therapy 2x/week for 6 weeks (quad strengthening, ROM)
     - Topical diclofenac gel 1% three times daily to right knee
     - Discontinue oral ibuprofen (given DM and HTN)
     - MRI if no improvement in 6 weeks (evaluate meniscus)
     - Weight management counseling (goal BMI <25)
     - Consider intra-articular corticosteroid injection at follow-up
  2. Continue Lisinopril 20mg. Recheck BP at follow-up.
  3. Continue Metformin. Check HbA1c at next PCP visit.

  Follow-up: 6 weeks or sooner if symptoms worsen.
  Patient educated on activity modification, ice therapy, and when
  to seek urgent care. Patient verbalized understanding.
```

---

## 4. Project Structure

```
medical_scriber/
├── _plans/masterplan.md      # This file
├── app.py                   # Main Streamlit app (UI + orchestration)
├── transcriber.py           # Transcription logic (Deepgram + ElevenLabs)
├── note_generator.py        # Claude API note generation logic
├── config.py                # Shared config, constants, medical keyterms
├── requirements.txt         # Python dependencies
├── .env                     # API keys (not committed)
├── .gitignore               # Ignore .env, __pycache__, venv, etc.
└── sample_scripts/          # Sample consultation scripts for testing
    ├── ortho_knee_pain.md
    └── cardio_chest_pain.md
```

---

## 5. Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Streamlit UI (Browser)                  │
│                                                            │
│  ┌─────────────┐  ┌───────────────┐  ┌────────────────┐  │
│  │ Patient Info │  │ Audio Record  │  │ Consultation   │  │
│  │ (manual)     │  │ + Playback    │  │ Notes Display  │  │
│  └─────────────┘  └──────┬────────┘  └───────▲────────┘  │
│                          │                    │            │
│  ┌───────────────────────┼────────────────────┼─────────┐ │
│  │              Provider Toggle                │         │ │
│  │         [Deepgram] / [ElevenLabs]           │         │ │
│  └───────────────────────┼─────────────────────┼─────────┘│
│                          │                     │           │
│  ┌───────────────────────▼─────────────────────┤         │ │
│  │           Diarized Transcript Display        │         │ │
│  │           Doctor: "..."                      │         │ │
│  │           Patient: "..."                     │         │ │
│  └──────────────────────┬──────────────────────┘         │ │
└─────────────────────────┼────────────────────────────────┘ │
                          │
         ┌────────────────┼────────────────┐
         ▼                                 ▼
┌─────────────────┐              ┌─────────────────┐
│  Deepgram API   │     OR       │ ElevenLabs API  │
│  Nova-2 Medical │              │  Scribe v2      │
│  diarize=true   │              │  diarize=true   │
└────────┬────────┘              └────────┬────────┘
         │                                │
         └──────────┬─────────────────────┘
                    │ diarized transcript
                    ▼
           ┌─────────────────┐
           │   Claude API    │
           │   (Anthropic)   │
           │                 │
           │  Prompt:        │
           │  transcript +   │
           │  note template  │
           │  → JSON output  │
           └────────┬────────┘
                    │ structured notes (JSON)
                    ▼
           Rendered in Streamlit UI
           + Download as Markdown
```

---

## 6. Implementation Phases

Seven phases (0–6). Each phase has its own plan and tracker under `_plans/phaseN/`. See `tracker_master.md` for task-level status and the decisions log.

| Phase | Goal |
|-------|------|
| 0 | Project setup: repo, venv, deps, config, API keys |
| 1 | Audio recording + Deepgram transcription with diarization |
| 2 | ElevenLabs transcription + provider comparison |
| 3 | Speaker role mapping (Speaker 0/1 → Doctor/Patient) |
| 4 | Claude-powered consultation note generation |
| 5 | Patient info form, download, error handling, polish |
| 6 | End-to-end testing with realistic consultation scripts |

---

## 7. Future Improvements (Out of Scope for v1)

| Feature | Description |
|---------|-------------|
| **Real-time transcription** | Stream audio and show live transcript during consultation |
| **Local/private mode** | Replace APIs with local Whisper + pyannote (no data leaves machine) |
| **Persistence** | SQLite database to store past consultations and notes |
| **Editable notes** | Let doctor edit each field inline before downloading |
| **Multiple note templates** | SOAP, H&P, Progress Note, Procedure Note |
| **Specialty-specific prompts** | Tailor the Claude prompt per specialty (Ortho vs Cardio vs Neuro) |
| **React UI** | Replace Streamlit with React + FastAPI for a production-like interface |
| **PDF export** | Generate formatted PDF consultation notes |
| **HIPAA compliance** | BAA agreements, encryption at rest, audit logging |

---

## 8. Risk & Limitations

- **Not for real clinical use.** This is a learning project with no HIPAA compliance, no audit trail, and no clinical validation.
- **Diarization is imperfect.** All diarization systems can misattribute speakers, especially with overlapping speech, similar voices, or short utterances.
- **LLM hallucination risk.** Claude may occasionally infer or embellish details not present in the transcript. The prompt includes guardrails, but they are not foolproof.
- **Audio quality matters.** Transcription accuracy degrades significantly with background noise, distant microphones, or heavy accents. For testing, use a quiet environment with a close microphone.
- **Medical terminology.** Deepgram's medical model handles drug names and conditions well. ElevenLabs relies on `keyterms` prompting, which requires maintaining a curated term list.
