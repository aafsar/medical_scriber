from dataclasses import dataclass

from deepgram import DeepgramClient
from elevenlabs import ElevenLabs

from config import (
    DEEPGRAM_API_KEY,
    DEEPGRAM_MODEL,
    ELEVENLABS_API_KEY,
    ELEVENLABS_MODEL,
    MEDICAL_KEYTERMS,
)


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


def _group_words_into_utterances(words: list) -> list[Utterance]:
    """Group consecutive words with the same speaker_id into Utterance objects.

    Filters out spacing/audio_event tokens. Words with speaker_id=None are
    assigned to the previous speaker (or speaker 0 if at the start).
    """
    if not words:
        return []

    utterances: list[Utterance] = []
    current_speaker: int | None = None
    current_words: list[str] = []
    current_start: float = 0.0
    current_end: float = 0.0

    for word in words:
        if word.type != "word":
            continue

        # Parse speaker_id ("speaker_0" -> 0), fall back to previous or 0
        if word.speaker_id is not None:
            speaker = int(word.speaker_id.split("_")[-1])
        elif current_speaker is not None:
            speaker = current_speaker
        else:
            speaker = 0

        # Speaker changed — close current utterance, start new one
        if speaker != current_speaker and current_words:
            utterances.append(Utterance(
                speaker=current_speaker,
                text=" ".join(current_words),
                start=current_start,
                end=current_end,
            ))
            current_words = []

        if not current_words:
            current_start = word.start or 0.0
            current_speaker = speaker

        current_words.append(word.text)
        current_end = word.end or current_start

    # Flush the last utterance
    if current_words:
        utterances.append(Utterance(
            speaker=current_speaker,
            text=" ".join(current_words),
            start=current_start,
            end=current_end,
        ))

    return utterances


def format_transcript_for_llm(
    utterances: list[Utterance], speaker_map: dict[int, str]
) -> str:
    lines = []
    for u in utterances:
        role = speaker_map.get(u.speaker, f"Speaker {u.speaker}")
        lines.append(f'{role}: "{u.text}"')
    return "\n".join(lines)


def transcribe_elevenlabs(audio_bytes: bytes) -> list[Utterance]:
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY is not set")

    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        result = client.speech_to_text.convert(
            model_id=ELEVENLABS_MODEL,
            file=audio_bytes,
            language_code="en",
            diarize=True,
            num_speakers=2,
            timestamps_granularity="word",
            tag_audio_events=False,
            keyterms=MEDICAL_KEYTERMS,
        )
    except Exception as e:
        raise RuntimeError(f"ElevenLabs API error: {e}") from e

    return _group_words_into_utterances(result.words or [])
