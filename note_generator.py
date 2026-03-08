import json
from pathlib import Path

import anthropic
from fpdf import FPDF

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL

NOTE_SECTIONS = (
    ("patient_information", "Patient Information"),
    ("chief_complaint", "Chief Complaint"),
    ("history_of_present_illness", "History of Present Illness"),
    ("past_medical_history", "Past Medical History"),
    ("medications", "Medications"),
    ("allergies", "Allergies"),
    ("social_history", "Social History"),
    ("family_history", "Family History"),
    ("review_of_systems", "Review of Systems"),
    ("physical_examination", "Physical Examination"),
    ("diagnostic_data", "Diagnostic Data"),
    ("assessment", "Assessment"),
    ("plan", "Plan"),
)

PATIENT_INFO_FIELDS = (
    ("name", "Name"),
    ("date_of_birth", "Date of Birth"),
    ("date_of_service", "Date of Service"),
    ("referring_physician", "Referring Physician"),
    ("specialty", "Specialty"),
)

SYSTEM_PROMPT = """\
You are a medical scribe assistant. Your job is to extract structured \
consultation notes from a doctor-patient conversation transcript.

RULES:
1. ONLY include information explicitly stated in the transcript. \
Never infer, assume, or fabricate any clinical details.
2. For any section not discussed in the conversation, use exactly: "Not discussed"
3. For patient information fields not provided, use exactly: "Not provided"
4. Do not add differential diagnoses, recommendations, or clinical reasoning \
that the doctor did not explicitly state.
5. Use the doctor's exact wording for assessment and plan whenever possible.
6. Preserve medical terminology as spoken.

OUTPUT FORMAT:
Return a single JSON object with these keys (all values are strings):

{
  "patient_information": {
    "name": "...",
    "date_of_birth": "...",
    "date_of_service": "...",
    "referring_physician": "...",
    "specialty": "..."
  },
  "chief_complaint": "...",
  "history_of_present_illness": "...",
  "past_medical_history": "...",
  "medications": "...",
  "allergies": "...",
  "social_history": "...",
  "family_history": "...",
  "review_of_systems": "...",
  "physical_examination": "...",
  "diagnostic_data": "...",
  "assessment": "...",
  "plan": "..."
}

Return ONLY the JSON object. No markdown fences, no extra text.\
"""


def generate_notes(transcript: str, patient_info: dict | None = None) -> dict:
    """Generate structured consultation notes from a diarized transcript.

    Args:
        transcript: LLM-formatted transcript (Doctor: "..." / Patient: "...").
        patient_info: Optional dict with patient metadata (name, DOB, etc.).

    Returns:
        Dict matching the consultation note JSON schema.

    Raises:
        ValueError: If API key is missing or transcript is empty.
        RuntimeError: If API call or response parsing fails.
    """
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_anthropic_key_here":
        raise ValueError("ANTHROPIC_API_KEY is not set")
    if not transcript or not transcript.strip():
        raise ValueError("Transcript is empty")

    user_message = _build_user_message(transcript, patient_info)

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4096,
            temperature=0.0,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
    except Exception as e:
        raise RuntimeError(f"Claude API error: {e}") from e

    text = response.content[0].text
    note = _parse_response(text)
    return _validate_note(note)


def _build_user_message(transcript: str, patient_info: dict | None) -> str:
    parts = []
    if patient_info:
        lines = []
        for key, label in PATIENT_INFO_FIELDS:
            value = patient_info.get(key, "")
            if value:
                lines.append(f"- {label}: {value}")
        if lines:
            parts.append("## Patient Information\n" + "\n".join(lines))
    parts.append("## Transcript\n" + transcript)
    return "\n\n".join(parts)


def _parse_response(text: str) -> dict:
    # Try raw JSON first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try stripping markdown fences
    stripped = text.strip()
    if stripped.startswith("```"):
        # Remove opening fence (```json or ```)
        first_newline = stripped.index("\n")
        stripped = stripped[first_newline + 1:]
        # Remove closing fence
        if stripped.endswith("```"):
            stripped = stripped[:-3].strip()
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass

    raise RuntimeError(f"Failed to parse Claude response as JSON: {text[:200]}")


def build_download_markdown(notes: dict) -> str:
    """Serialize a consultation note dict into a readable Markdown string."""
    lines = ["CONSULTATION NOTE", "=================", ""]
    for key, label in NOTE_SECTIONS:
        value = notes.get(key, "Not discussed")
        heading = label.upper()
        if key == "patient_information":
            lines.append(heading)
            info = value if isinstance(value, dict) else {}
            for field_key, field_label in PATIENT_INFO_FIELDS:
                field_val = info.get(field_key, "Not provided")
                lines.append(f"  {field_label}: {field_val}")
        else:
            lines.append(heading)
            lines.append(value)
        lines.append("")
    return "\n".join(lines)


# --- PDF Export ---

_PDF_TEAL = (47, 111, 107)
_PDF_GRAY = (136, 136, 136)
_PDF_BLACK = (0, 0, 0)
_DEFAULT_LOGO = Path(__file__).parent / "assets" / "Angy_logo_color.png"

# Unicode → Latin-1 replacements for built-in Helvetica
_UNICODE_SUBS = {
    "\u2014": "--",   # em dash
    "\u2013": "-",    # en dash
    "\u2018": "'",    # left single quote
    "\u2019": "'",    # right single quote
    "\u201c": '"',    # left double quote
    "\u201d": '"',    # right double quote
    "\u2026": "...",  # ellipsis
    "\u2022": "-",    # bullet
}


def _latin1_safe(text: str) -> str:
    """Replace common Unicode chars that Helvetica can't render."""
    for char, replacement in _UNICODE_SUBS.items():
        text = text.replace(char, replacement)
    # Catch-all: replace any remaining non-Latin-1 chars with '?'
    return text.encode("latin-1", "replace").decode("latin-1")


class _ConsultationPDF(FPDF):
    """FPDF subclass with branded header and footer on every page."""

    def __init__(self, logo_path: Path | None = None):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.logo_path = logo_path
        self._logo_ok = logo_path is not None and logo_path.exists()
        self._logo_aspect = None
        if self._logo_ok:
            try:
                from PIL import Image
                with Image.open(logo_path) as img:
                    w, h = img.size
                    self._logo_aspect = w / h
            except Exception:
                self._logo_ok = False
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        start_y = self.get_y()
        logo_h = 12
        # Title (left-aligned)
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(*_PDF_TEAL)
        self.set_xy(self.l_margin, start_y)
        self.cell(120, 12, "CONSULTATION NOTE", align="L")
        # Logo (right-aligned to margin)
        if self._logo_ok:
            try:
                logo_w = logo_h * self._logo_aspect
                self.image(str(self.logo_path), x=self.w - self.r_margin - logo_w, y=start_y, h=logo_h)
            except Exception:
                self._logo_ok = False
        self.set_y(start_y + 15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*_PDF_GRAY)
        self.set_x(self.l_margin)
        self.cell(0, 5, "Generated by Angy Voice  |  AI-assisted -- verify all content", align="L")
        self.set_xy(self.l_margin, self.get_y() - 5)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", align="R")


def _render_patient_info(pdf: _ConsultationPDF, info: dict):
    """Render patient info as a two-column block."""
    left_fields = [("name", "Name"), ("date_of_birth", "Date of Birth"), ("date_of_service", "Date of Service")]
    right_fields = [("referring_physician", "Referring Physician"), ("specialty", "Specialty")]

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*_PDF_TEAL)
    pdf.cell(0, 7, "PATIENT INFORMATION", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*_PDF_TEAL)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(3)

    col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 2
    start_y = pdf.get_y()

    # Left column
    pdf.set_xy(pdf.l_margin, start_y)
    for key, label in left_fields:
        val = _latin1_safe(info.get(key, "Not provided"))
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*_PDF_BLACK)
        pdf.cell(28, 5, f"{label}:")
        pdf.set_font("Helvetica", "", 9)
        if val == "Not provided":
            pdf.set_text_color(*_PDF_GRAY)
        pdf.cell(col_w - 28, 5, val, new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*_PDF_BLACK)

    left_end_y = pdf.get_y()

    # Right column
    right_x = pdf.l_margin + col_w
    right_y = start_y
    for key, label in right_fields:
        val = _latin1_safe(info.get(key, "Not provided"))
        pdf.set_xy(right_x, right_y)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*_PDF_BLACK)
        pdf.cell(35, 5, f"{label}:")
        pdf.set_font("Helvetica", "", 9)
        if val == "Not provided":
            pdf.set_text_color(*_PDF_GRAY)
        pdf.cell(col_w - 35, 5, val)
        pdf.set_text_color(*_PDF_BLACK)
        right_y += 5

    pdf.set_y(max(left_end_y, right_y) + 2)
    pdf.set_draw_color(*_PDF_GRAY)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(4)


def _render_section(pdf: _ConsultationPDF, title: str, body: str):
    """Render a clinical section: teal header + body text."""
    # Section header
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*_PDF_TEAL)
    pdf.cell(0, 7, title.upper(), new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*_PDF_TEAL)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(2)

    # Body text
    if body == "Not discussed":
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(*_PDF_GRAY)
    else:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*_PDF_BLACK)
    pdf.multi_cell(0, 5, _latin1_safe(body), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)


def build_download_pdf(notes: dict, logo_path: Path | None = None) -> bytes:
    """Generate a PDF consultation note. Returns raw PDF bytes."""
    if logo_path is None:
        logo_path = _DEFAULT_LOGO

    info = notes.get("patient_information", {})
    if not isinstance(info, dict):
        info = {}

    pdf = _ConsultationPDF(logo_path=logo_path)
    pdf.alias_nb_pages()
    pdf.add_page()

    # Patient info block
    _render_patient_info(pdf, info)

    # Clinical sections (skip patient_information, already rendered)
    for key, label in NOTE_SECTIONS:
        if key == "patient_information":
            continue
        value = notes.get(key, "Not discussed")
        _render_section(pdf, label, value)

    return bytes(pdf.output())


def _validate_note(note: dict) -> dict:
    for key, _ in NOTE_SECTIONS:
        if key == "patient_information":
            if key not in note or not isinstance(note[key], dict):
                note[key] = {}
            for field_key, _ in PATIENT_INFO_FIELDS:
                if field_key not in note[key]:
                    note[key][field_key] = "Not provided"
        elif key not in note:
            note[key] = "Not discussed"
    return note
