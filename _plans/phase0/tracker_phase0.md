# Phase 0: Project Setup — Tracker

> **Last Updated:** 2026-02-21
> **Phase Status:** NOT STARTED

---

## Implementation Order

Tasks are listed in execution order. Dependencies noted where they exist.

| # | Task | Status | Depends On | Notes |
|---|------|--------|------------|-------|
| 0.1 | Update pyenv + install Python 3.14.3 | NOT STARTED | — | `pyenv update && pyenv install 3.14.3` |
| 0.2 | Set project Python version | NOT STARTED | 0.1 | `pyenv local 3.14.3` (creates `.python-version`) |
| 0.3 | Create `.gitignore` | NOT STARTED | — | See plan for full contents |
| 0.4 | Initialize git repo + initial commit | NOT STARTED | 0.2, 0.3 | Commits: `.gitignore`, `_plans/`, `.claude/`, `.python-version` |
| 0.5 | Create Python virtual environment | NOT STARTED | 0.2 | `python3 -m venv venv` |
| 0.6 | Create `requirements.txt` | NOT STARTED | — | 5 dependencies from masterplan |
| 0.7 | Install dependencies | NOT STARTED | 0.5, 0.6 | `pip install -r requirements.txt` |
| 0.8 | Create `.env` with placeholder keys | NOT STARTED | — | Not committed to git |
| 0.9 | Create `config.py` | NOT STARTED | 0.8 | Loads keys, defines model constants + keyterms |
| 0.10 | Create `sample_scripts/` directory | NOT STARTED | — | Empty placeholder for Phase 6 |
| 0.11 | Commit Phase 0 files | NOT STARTED | 0.6–0.10 | `requirements.txt`, `config.py`, `sample_scripts/` |
| 0.12 | Obtain API keys (manual) | NOT STARTED | — | Deepgram, ElevenLabs, Anthropic |
| 0.13 | Verify API keys work (manual) | NOT STARTED | 0.7, 0.8, 0.12 | Smoke test each provider |

**Status legend:** NOT STARTED | IN PROGRESS | DONE | BLOCKED | SKIPPED

---

## Files to Create

| File | Created | Committed |
|------|---------|-----------|
| `.python-version` | NOT STARTED | NOT STARTED |
| `.gitignore` | NOT STARTED | NOT STARTED |
| `requirements.txt` | NOT STARTED | NOT STARTED |
| `.env` | NOT STARTED | N/A (gitignored) |
| `config.py` | NOT STARTED | NOT STARTED |
| `sample_scripts/` | NOT STARTED | NOT STARTED |

---

## API Keys

| Service | Obtained | Added to `.env` | Verified |
|---------|----------|-----------------|----------|
| Deepgram | NO | NO | NO |
| ElevenLabs | NO | NO | NO |
| Anthropic | NO | NO | NO |

---

## Verification Checklist

Run after all tasks are done:

- [ ] `python3 --version` → 3.14.3
- [ ] `git log --oneline` → shows 2 commits
- [ ] `source venv/bin/activate` → no errors
- [ ] `pip list` → shows streamlit, deepgram-sdk, elevenlabs, anthropic, python-dotenv
- [ ] `.env` exists but `git status` does not show it
- [ ] `python -c "import config; print(config.CLAUDE_MODEL)"` → `claude-sonnet-4-20250514`
- [ ] `python -c "import config; print(len(config.MEDICAL_KEYTERMS))"` → ~55
- [ ] `ls sample_scripts/` → directory exists

---

## Issues

| # | Date | Issue | Resolution |
|---|------|-------|------------|
| | | | |

---

## Next

→ **Phase 1: Audio Recording + Deepgram Transcription**

Prerequisites from this phase: Deepgram API key verified, all dependencies installed, `config.py` ready.
