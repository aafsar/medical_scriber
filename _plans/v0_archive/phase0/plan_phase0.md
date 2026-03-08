# Phase 0: Project Setup — Plan & Context

> **Goal:** Set up the project foundation — git repo, Python environment, dependencies, config files, and API key placeholders — so that Phase 1 development can begin immediately.
>
> **Outcome:** Completed 2026-02-22. Python 3.14.3, all deps installed, private GitHub repo live. See `tracker_phase0.md` for status.

---

## Pre-Conditions

- Project directory exists at `medical_scriber/`
- Master plan written (`_plans/masterplan.md`)
- Master tracker written (`_plans/tracker_master.md`)
- Phase subdirectories created (`_plans/phase0/` through `_plans/phase6/`)
- Python available via pyenv

---

## Python Version

**Target: Python 3.14.3** (latest stable release, Feb 2026). Set via `pyenv local 3.14.3` which creates a `.python-version` file in the project root.

**Fallback:** 3.13.4 if dependencies don't support 3.14 yet (not needed — all 5 deps have 3.14 wheels).

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

Placeholder file for API keys. Not committed to git (gitignored). Contains `DEEPGRAM_API_KEY`, `ELEVENLABS_API_KEY`, `ANTHROPIC_API_KEY`.

**Where to get keys:**
- Deepgram: https://console.deepgram.com/signup ($200 free credits)
- ElevenLabs: https://elevenlabs.io/sign-up (~2.5 hrs/month free)
- Anthropic: https://console.anthropic.com/ (pay-as-you-go)

---

## `requirements.txt` Contents

5 top-level dependencies from masterplan Section 9: `streamlit`, `deepgram-sdk`, `elevenlabs`, `anthropic`, `python-dotenv`. See `requirements.txt` for pinned versions.

---

## `config.py` Design

Centralized configuration module. See `config.py` for full implementation.

**Structure:**
- **API Keys** — loaded from `.env` via `python-dotenv` / `os.getenv()`
- **Model constants** — `DEEPGRAM_MODEL`, `ELEVENLABS_MODEL`, `CLAUDE_MODEL` — defined here so they can be changed in one place
- **Medical keyterms** — 71 terms for ElevenLabs' `keyterms` parameter (up to 100 allowed). Covers conditions, medications, orthopedic/cardiology terms, vitals, and procedures

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

