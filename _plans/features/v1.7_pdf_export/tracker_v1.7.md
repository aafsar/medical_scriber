# v1.7: PDF Export — Tracker

> **Last Updated:** 2026-03-08
> **Feature Status:** DONE

---

## Implementation Order

| # | Task | Status | Depends On | Notes |
|---|------|--------|------------|-------|
| 1 | Add `fpdf2>=2.8.0` to `requirements.txt` | DONE | — | |
| 2 | Add `_ConsultationPDF` class + helpers to `note_generator.py` | DONE | 1 | |
| 3 | Add `build_download_pdf()` public function | DONE | 2 | |
| 4 | Update `app.py` download section (two-column layout) | DONE | 3 | |
| 5 | Create feature docs, update master tracker | DONE | — | |
| 6 | Verify PDF output | DONE | 4 | Smoke-tested with mock data |

## Verification Checklist

- [x] All 13 sections render with correct formatting
- [x] Multi-page documents paginate with header/footer on every page
- [x] "Not discussed" sections show italic gray
- [x] Logo appears in header (degrades gracefully if missing)
- [x] Markdown download still works alongside PDF
- [x] Filenames match pattern (`{name}_{dos}_consultation.pdf`)
- [x] Unicode characters handled (em dash, smart quotes → Latin-1 safe)
- [x] Two-column patient info renders without overlap

## Issues

| # | Date | Issue | Resolution |
|---|------|-------|------------|
| 1 | 2026-03-08 | Em dash (`—`) in footer caused `FPDFUnicodeEncodingException` | Added `_latin1_safe()` helper with Unicode→ASCII substitutions; replaced em dash in footer with `--` |
| 2 | 2026-03-08 | Right-column patient info fields overlapped with left column | Fixed by explicitly setting X/Y per row instead of relying on `new_x="LMARGIN"` |
