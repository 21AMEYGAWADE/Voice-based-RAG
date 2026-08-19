import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is missing. Add it to backend/.env"
    )

LLM_MODEL = "gpt-5.6-luna"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TRANSCRIPTION_MODEL = "gpt-4o-transcribe"

TTS_MODEL = "gpt-4o-mini-tts"

TTS_VOICE = "marin"

CHROMA_PATH = "./chroma_db"

COLLECTION_NAME = "voice_rag_documents"

DOCUMENTS_PATH = "./documents"

TEMP_PATH = "./temp"