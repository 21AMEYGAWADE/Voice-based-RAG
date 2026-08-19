from openai import OpenAI

from app.config import OPENAI_API_KEY, TRANSCRIPTION_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


def transcribe_audio(file_path: str) -> str:

    with open(file_path, "rb") as audio_file:

        transcript = client.audio.transcriptions.create(
            model=TRANSCRIPTION_MODEL,
            file=audio_file
        )

    return transcript.text