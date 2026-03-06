import json

import anthropic

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
