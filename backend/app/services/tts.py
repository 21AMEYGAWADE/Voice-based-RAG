from pathlib import Path

from openai import OpenAI

from app.config import (
    OPENAI_API_KEY,
    TTS_MODEL,
    TTS_VOICE
)


client = OpenAI(api_key=OPENAI_API_KEY)


def generate_speech(text: str, output_path: str):

    speech_file = Path(output_path)

    with client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=text,
        response_format="mp3"
    ) as response:

        response.stream_to_file(speech_file)

    return str(speech_file)