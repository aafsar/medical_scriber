from dataclasses import dataclass

from deepgram import DeepgramClient

from config import DEEPGRAM_API_KEY, DEEPGRAM_MODEL


@dataclass
class Utterance:
    speaker: int
    text: str
    start: float
    end: float


def transcribe_deepgram(audio_bytes: bytes) -> list[Utterance]:
    if not DEEPGRAM_API_KEY:
        raise ValueError("DEEPGRAM_API_KEY is not set")

    try:
        client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
        response = client.listen.v1.media.transcribe_file(
            request=audio_bytes,
            model=DEEPGRAM_MODEL,
            diarize=True,
            utterances=True,
            smart_format=True,
            punctuate=True,
        )
    except Exception as e:
        raise RuntimeError(f"Deepgram API error: {e}") from e

    raw_utterances = response.results.utterances
    if not raw_utterances:
        return []

    return [
        Utterance(
            speaker=u.speaker or 0,
            text=u.transcript or "",
            start=u.start or 0.0,
            end=u.end or 0.0,
        )
        for u in raw_utterances
    ]
