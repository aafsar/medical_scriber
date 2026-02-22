# Phase 0: Project Setup — Plan & Context

> **Goal:** Set up the project foundation — git repo, Python environment, dependencies, config files, and API key placeholders — so that Phase 1 development can begin immediately.

---

## Pre-Conditions

- Project directory exists at `medical_scriber/`
- Master plan written (`_plans/masterplan.md`)
- Master tracker written (`_plans/tracker_master.md`)
- Phase subdirectories created (`_plans/phase0/` through `_plans/phase6/`)
- Python available via pyenv (currently 3.13.1; will upgrade to 3.14.3)

---

## Python Version

**Target: Python 3.14.3** (latest stable release, Feb 2026).

The current pyenv installation only has up to 3.13.x. Before creating the virtual environment:
1. Update pyenv itself: `pyenv update` (or `brew upgrade pyenv` on macOS)
2. Install Python 3.14.3: `pyenv install 3.14.3`
3. Set it as the project-local version: `pyenv local 3.14.3`

This creates a `.python-version` file in the project root that pyenv uses automatically.

**Fallback:** If any dependency fails to install on 3.14, fall back to 3.13.4 (latest stable 3.13.x in pyenv). Python 3.14 is new and some packages may not have wheels yet.

---

## `.gitignore` Design

Must be created before `git init` so the initial commit is clean.

**What to exclude and why:**
- `__pycache__/`, `*.py[cod]` — Python bytecode, auto-generated
- `venv/`, `.venv/`, `env/` — virtual environment, large, machine-specific
- `.env`, `.env.local`, `.env.*.local` — API keys and secrets
- `.vscode/`, `.idea/` — IDE config, personal preference
- `.DS_Store`, `Thumbs.db` — OS junk files
- `*.wav`, `*.mp3`, `*.m4a`, `*.ogg`, `*.webm`, `*.flac` — audio test files, can be large
- `.streamlit/` — Streamlit cache/config
- `*.log` — log files

**What NOT to exclude:**
- `.claude/` — contains project-specific Claude Code settings
- `.python-version` — pyenv version file, should be shared
- `_plans/` — project documentation

---

## `.env` Design

Placeholder file for API keys. Not committed to git.

```
# AI Medical Scriber - API Keys
# Replace placeholder values with your actual API keys

DEEPGRAM_API_KEY=your_deepgram_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

**Where to get keys:**
- Deepgram: https://console.deepgram.com/signup ($200 free credits)
- ElevenLabs: https://elevenlabs.io/sign-up (~2.5 hrs/month free)
- Anthropic: https://console.anthropic.com/ (pay-as-you-go)

---

## `requirements.txt` Contents

From masterplan Section 9:

```
streamlit>=1.40.0
deepgram-sdk>=3.5.0
elevenlabs>=1.0.0
anthropic>=0.40.0
python-dotenv>=1.0.0
```

5 packages. All are top-level dependencies; pip handles transitive deps.

---

## `config.py` Design

Centralized configuration module. Loads API keys from `.env` via `python-dotenv`, defines model constants and medical keyterms.

**Structure:**
- **API Keys** — loaded from environment variables via `os.getenv()`
- **Model constants** — `DEEPGRAM_MODEL`, `ELEVENLABS_MODEL`, `CLAUDE_MODEL` — defined here so they can be changed in one place
- **Medical keyterms** — list of ~55 medical terms for ElevenLabs' `keyterms` parameter (up to 100 allowed). Covers:
  - Common conditions (hypertension, diabetes, COPD, etc.)
  - Common medications (metformin, lisinopril, etc.)
  - Orthopedic terms (meniscus, McMurray, Lachman, etc.)
  - Cardiology terms (echocardiogram, troponin, etc.)
  - General medical terms (bilateral, palpation, etc.)
  - Vitals/measurements (systolic, SpO2, HbA1c, etc.)
  - Procedures (MRI, arthroscopy, etc.)

```python
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Model configuration
DEEPGRAM_MODEL = "nova-2-medical"
ELEVENLABS_MODEL = "scribe_v2"
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# Medical keyterms for ElevenLabs (up to 100)
MEDICAL_KEYTERMS = [
    # Common conditions
    "hypertension", "diabetes mellitus", "osteoarthritis",
    "hyperlipidemia", "COPD", "atrial fibrillation",
    "coronary artery disease", "congestive heart failure",
    "gastroesophageal reflux", "hypothyroidism",
    # Common medications
    "metformin", "lisinopril", "atorvastatin",
    "amlodipine", "omeprazole", "levothyroxine",
    "metoprolol", "losartan", "gabapentin", "prednisone",
    "ibuprofen", "acetaminophen", "naproxen", "diclofenac",
    # Orthopedic terms
    "meniscus", "ligament", "ACL", "MCL",
    "rotator cuff", "sciatica", "stenosis",
    "osteophyte", "effusion", "crepitus",
    "McMurray", "Lachman", "antalgic",
    # Cardiology terms
    "echocardiogram", "ejection fraction", "troponin",
    "electrocardiogram", "stent", "angioplasty",
    "palpitations", "dyspnea", "syncope", "murmur",
    # General medical terms
    "bilateral", "contralateral", "ipsilateral",
    "proximal", "distal", "anterior", "posterior",
    "palpation", "auscultation", "percussion",
    # Vitals & measurements
    "systolic", "diastolic", "SpO2", "BMI",
    "hemoglobin A1c", "creatinine", "BUN",
    # Procedures
    "MRI", "CT scan", "X-ray", "ultrasound",
    "arthroscopy", "injection", "biopsy",
]
```

---

## `sample_scripts/` Directory

Empty placeholder directory. Will hold consultation scripts for Phase 6 end-to-end testing (ortho knee pain, cardio chest pain, multi-problem follow-up). Created now to match the planned project structure from the masterplan.

---

## API Key Verification

After obtaining keys and adding them to `.env`, a quick smoke test per provider:
1. **Deepgram:** Send a short audio clip, check for valid transcription response
2. **ElevenLabs:** Send a short audio clip, check for valid transcription response
3. **Anthropic:** Send a simple message prompt, check for valid response

This is a manual step — the user does it whenever they have keys ready.

---

## Git Strategy

Two commits for Phase 0:
1. **Initial commit** — `.gitignore`, `_plans/`, `.claude/settings.local.json`, `.python-version`
2. **Phase 0 commit** — `requirements.txt`, `config.py`, `sample_scripts/`

`.env` is never committed.

---

## Done Criteria

Phase 0 is complete when:
- Git repo initialized with clean commit history
- Python 3.14.3 venv created and activatable (or 3.13.4 fallback)
- All 5 dependencies installed and importable
- `.env` exists with placeholder keys
- `config.py` loads keys and defines all constants + keyterms
- `sample_scripts/` directory exists
- API keys obtained and verified (manual — user action, can be deferred)
