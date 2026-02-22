# Phase 0: Project Setup — Tracker

> **Last Updated:** 2026-02-22
> **Phase Status:** DONE (API keys pending)

---

## Implementation Order

Tasks are listed in execution order. Dependencies noted where they exist.

| # | Task | Status | Depends On | Notes |
|---|------|--------|------------|-------|
| 0.1 | Update pyenv + install Python 3.14.3 | DONE | — | pyenv 2.6.1→2.6.23, Python 3.14.3 installed |
| 0.2 | Set project Python version | DONE | 0.1 | `pyenv local 3.14.3` → `.python-version` created |
| 0.3 | Create `.gitignore` | DONE | — | All planned entries included |
| 0.4 | Initialize git repo + initial commit | DONE | 0.2, 0.3 | Commit `1c4baeb` |
| 0.5 | Create Python virtual environment | DONE | 0.2 | `python3 -m venv venv` on 3.14.3 |
| 0.6 | Create `requirements.txt` | DONE | — | 5 dependencies |
| 0.7 | Install dependencies | DONE | 0.5, 0.6 | All installed on 3.14.3, no fallback needed |
| 0.8 | Create `.env` with placeholder keys | DONE | — | Not committed (gitignored) |
| 0.9 | Create `config.py` | DONE | 0.8 | 71 keyterms (plan said ~55, expanded) |
| 0.10 | Create `sample_scripts/` directory | DONE | — | `.gitkeep` added for git tracking |
| 0.11 | Commit Phase 0 files | DONE | 0.6–0.10 | Commit `5713057` |
| 0.12 | Obtain API keys (manual) | NOT STARTED | — | Deepgram, ElevenLabs, Anthropic |
| 0.13 | Verify API keys work (manual) | NOT STARTED | 0.7, 0.8, 0.12 | Smoke test each provider |

**Status legend:** NOT STARTED | IN PROGRESS | DONE | BLOCKED | SKIPPED

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

- [x] `python3 --version` → 3.14.3
- [x] `git log --oneline` → shows 2 commits
- [x] `source venv/bin/activate` → no errors
- [x] `pip list` → shows streamlit, deepgram-sdk, elevenlabs, anthropic, python-dotenv
- [x] `.env` exists but `git status` does not show it
- [x] `python -c "import config; print(config.CLAUDE_MODEL)"` → `claude-sonnet-4-20250514`
- [x] `python -c "import config; print(len(config.MEDICAL_KEYTERMS))"` → 71
- [x] `ls sample_scripts/` → directory exists

---

## Installed Versions

| Package | Version |
|---------|---------|
| streamlit | 1.54.0 |
| deepgram-sdk | 5.3.2 |
| elevenlabs | 2.36.1 |
| anthropic | 0.83.0 |
| python-dotenv | 1.2.1 |

---

## GitHub

- **Repo:** https://github.com/aafsar/medical_scriber (private)
- **Pushed:** 2 commits on `main`

---

## Issues

| # | Date | Issue | Resolution |
|---|------|-------|------------|
| 1 | 2026-02-22 | pyenv 2.6.1 didn't have 3.14.3 | Upgraded pyenv to 2.6.23 via `brew upgrade pyenv` |

---

## Next

→ **Phase 1: Audio Recording + Deepgram Transcription**

Prerequisites from this phase: Deepgram API key verified, all dependencies installed, `config.py` ready.
