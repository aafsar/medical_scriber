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

### 2.2 Provider Evaluation Backlog

Beyond Deepgram and ElevenLabs (implemented in Phases 1–2), evaluate these providers for transcription and/or diarization quality on medical audio. Prioritize based on medical-specific features, free tier availability, and diarization support.

| Provider | Category | Notes |
|----------|----------|-------|
| **AssemblyAI** | Transcription + diarization | Universal-2 model, medical vocab, speaker labels |
| **OpenAI** | Transcription | Whisper API; no native diarization |
| **Google** | Transcription + diarization | Cloud Speech-to-Text; medical adaptation available |
| **AWS** | Transcription + diarization | Amazon Transcribe Medical; HIPAA-eligible |
| **Azure** | Transcription + diarization | Azure AI Speech; custom medical models |
| **Speechmatics** | Transcription + diarization | High accuracy claims; real-time and batch |
| **Cartesia** | Voice / TTS-focused | Evaluate if transcription API exists |
| **Livekit** | Real-time infra | WebRTC platform; may integrate with STT providers |
| **Pipecat** | Voice pipeline framework | Orchestration layer, not a provider itself |
| **Retell** | Voice agent platform | Built for conversational AI; evaluate STT component |
| **Rime** | TTS-focused | Evaluate if transcription API exists |
| **Vapi** | Voice agent platform | Orchestration layer; evaluate STT component |

**When to evaluate:** After Phase 6 baseline comparison (Deepgram vs ElevenLabs) is complete. Use the same test recordings and comparison framework to benchmark new providers.

### 2.3 LLM for Note Generation

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
├── _plans/
│   ├── masterplan.md            # This file (v1 design reference)
│   ├── tracker_master.md        # v1 feature progress dashboard
│   ├── features/                # Per-feature plan + tracker folders
│   │   └── TEMPLATE.md          # Plan + tracker templates
│   └── v0_archive/              # Completed v0 phase docs (read-only)
│       ├── README.md
│       ├── masterplan_v0.md
│       ├── tracker_master_v0.md
│       └── phase0/ ... phase6/
├── app.py                       # Main Streamlit app (UI + orchestration)
├── pages/
│   └── test_runner.py           # Automated test UI (dual-provider pipeline)
├── transcriber.py               # Transcription logic (Deepgram + ElevenLabs)
├── note_generator.py            # Claude API note generation logic
├── compare.py                   # Test comparison logic (term accuracy, reports)
├── config.py                    # Shared config, constants, medical keyterms
├── requirements.txt             # Python dependencies
├── .env                         # API keys (not committed)
├── .gitignore                   # Ignore .env, __pycache__, venv, etc.
├── sample_scripts/              # Sample consultation scripts for testing
│   ├── ortho_knee_pain.md
│   ├── cardio_chest_pain.md
│   └── multi_problem_followup.md
└── test_results/                # Saved test run outputs (gitignored)
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

## 6. Implementation History

**v0 (Phases 0–6):** Delivered the core pipeline — audio recording, dual-provider transcription (Deepgram + ElevenLabs), speaker diarization, Claude-powered note generation, and end-to-end testing. Completed 2026-03-07. ElevenLabs wins accuracy (95% vs 88%), Deepgram wins latency (26.6s vs 45.0s). See [`v0_archive/README.md`](v0_archive/README.md) for full phase docs and [`v0_archive/tracker_master_v0.md`](v0_archive/tracker_master_v0.md) for detailed results.

**v1:** Feature-based development (v1.1–v1.18). See Section 7 for the full roadmap and `tracker_master.md` for progress.

---

## 7. v1 Roadmap

Consolidated backlog for the next version, organized by priority. Items marked *(new)* were identified from Phase 6 testing gaps; the rest carry over from v0's future improvements list.

### Priority 1 — Deploy & Export

| # | Feature | Description | Source |
|---|---------|-------------|--------|
| v1.1 | **Deployment** | Deploy to Streamlit Community Cloud (free, trivial for Streamlit apps). Makes the app demable without local setup. | *(new)* |
| v1.7 | **PDF export** | Generate formatted PDF consultation notes in addition to Markdown. | v0 backlog |

### Priority 2 — Harden & Expand

| # | Feature | Description | Source |
|---|---------|-------------|--------|
| v1.2 | **Prompt iteration** | Tune the Claude note-generation prompt based on Phase 6 results — address formatting inconsistencies (prose vs numbered plans), improve sentinel value handling, reduce hallucination risk. | *(new)* |
| v1.3 | **Error recovery** | Allow retrying note generation from an existing transcript without re-transcribing. Save transcript to session state so the user can re-generate notes if the Claude API call fails. | *(new)* |
| v1.4 | **Cost tracking** | Log and display per-request API costs (transcription + note generation). Essential for comparing 12+ providers in the evaluation backlog. | *(new)* |
| v1.5 | **Recording consent notice** | Show a "This consultation will be recorded" prompt before recording starts. Good practice even for a toy project. | *(new)* |
| v1.6 | **Editable notes** | Let the doctor edit each note section inline before downloading. Critical for correcting LLM errors before the note leaves the app. | v0 backlog |
| v1.8 | **Persistence** | SQLite database to store past consultations and notes. Enable retrieval of previous encounters. | v0 backlog |
| v1.9 | **Note accuracy validation** | Systematically check whether generated notes are faithful to the transcript — detect missed findings, hallucinated details, wrong speaker attribution. Goes beyond Phase 6's term-matching. | *(new)* |
| v1.10 | **Longer consultation testing** | Test with 15–30 minute audio to verify transcription accuracy, token limits, and note quality don't degrade at realistic consultation lengths. | *(new)* |
| v1.11 | **Audio preprocessing** | Add noise reduction and volume normalization before sending audio to transcription APIs. Improves accuracy with varied recording setups. | *(new)* |
| v1.12 | **Multi-speaker support (>2)** | Handle consultations with nurses, family members, interpreters, or medical students — not just Doctor + Patient. | *(new)* |

### Priority 3 — Advanced / Architectural

| # | Feature | Description | Source |
|---|---------|-------------|--------|
| v1.13 | **Multiple note templates** | SOAP, H&P, Progress Note, Procedure Note — let the user choose the output format. | v0 backlog |
| v1.14 | **Specialty-specific prompts** | Tailor the Claude prompt per specialty (Ortho vs Cardio vs Neuro) for better note quality. | v0 backlog |
| v1.15 | **Real-time transcription** | Stream audio and show a live transcript during the consultation. | v0 backlog |
| v1.16 | **Local/private mode** | Replace APIs with local Whisper + pyannote so no data leaves the machine. | v0 backlog |
| v1.17 | **React UI** | Replace Streamlit with React + FastAPI for a production-like interface. | v0 backlog |
| v1.18 | **HIPAA compliance** | BAA agreements with API providers, encryption at rest, audit logging. | v0 backlog |

---

## 8. Risk & Limitations

- **Not for real clinical use.** This is a learning project with no HIPAA compliance, no audit trail, and no clinical validation.
- **Diarization is imperfect.** All diarization systems can misattribute speakers, especially with overlapping speech, similar voices, or short utterances.
- **LLM hallucination risk.** Claude may occasionally infer or embellish details not present in the transcript. The prompt includes guardrails, but they are not foolproof.
- **Audio quality matters.** Transcription accuracy degrades significantly with background noise, distant microphones, or heavy accents. For testing, use a quiet environment with a close microphone.
- **Medical terminology.** Deepgram's medical model handles drug names and conditions well. ElevenLabs relies on `keyterms` prompting, which requires maintaining a curated term list.
