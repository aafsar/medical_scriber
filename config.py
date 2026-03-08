import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


def _get_secret(key: str) -> str | None:
    """Try st.secrets first (Streamlit Cloud), fall back to .env."""
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.getenv(key)


# API Keys
DEEPGRAM_API_KEY = _get_secret("DEEPGRAM_API_KEY")
ELEVENLABS_API_KEY = _get_secret("ELEVENLABS_API_KEY")
ANTHROPIC_API_KEY = _get_secret("ANTHROPIC_API_KEY")

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

SPECIALTIES = (
    "Cardiology",
    "Dermatology",
    "Endocrinology",
    "Gastroenterology",
    "Hematology / Oncology",
    "Infectious Disease",
    "Internal Medicine",
    "Nephrology",
    "Neurology",
    "Obstetrics & Gynecology",
    "Ophthalmology",
    "Orthopedic Surgery",
    "Otolaryngology (ENT)",
    "Pulmonology",
    "Rheumatology",
    "Urology",
)
