# v1.1: Streamlit Community Cloud Deployment — Plan & Context
> **Goal:** Deploy the app to Streamlit Community Cloud so it's accessible via a public URL.
> **Outcome:** [filled after completion]
> **Priority:** 1
> **Depends on:** None
---

## Pre-Conditions
- App fully functional locally (v0 Phases 0–6 complete)
- GitHub repo exists (`aafsar/medical_scriber`)
- All files needed for the app to run must be committed (several were untracked)

## Design Decisions

### Secret Management
The app loads API keys from `.env` via `os.getenv()`. Streamlit Cloud uses `st.secrets` instead. Rather than choosing one or the other, `config.py` uses a helper that tries `st.secrets` first and falls back to `os.getenv()`. This keeps local `.env` workflow intact while supporting Streamlit Cloud's Secrets dashboard.

### .gitignore Update
The entire `.streamlit/` directory was gitignored, which prevented `config.toml` (theme colors) from being committed. Changed to only ignore `.streamlit/secrets.toml` so the theme config deploys with the app.

### Untracked Files
Several files listed as Active in the files inventory were never committed:
- `assets/Angy_logo_color.png` — logo used in sidebar and PDF export
- `compare.py` — test comparison logic
- `pages/test_runner.py` — test runner page
- `_plans/feature_workflow.md` — development workflow doc

These are all committed as part of this feature.

### Python Version
Local Python is 3.14.3. Streamlit Cloud may not support it. If deployment fails, a `runtime.txt` with `python-3.12` will be added. Not pre-adding it since it may not be needed.

## Files Changed

| File | Changes |
|------|---------|
| `.gitignore` | `.streamlit/` → `.streamlit/secrets.toml` |
| `config.py` | Add `_get_secret()` helper, `st.secrets` fallback |
| `.streamlit/config.toml` | Now committed (was gitignored) |
| `assets/Angy_logo_color.png` | Now committed (was untracked) |
| `compare.py` | Now committed (was untracked) |
| `pages/test_runner.py` | Now committed (was untracked) |
| `_plans/feature_workflow.md` | Now committed (was untracked) |
