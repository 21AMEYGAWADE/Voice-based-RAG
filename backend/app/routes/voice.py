import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from fastapi.responses import FileResponse

from app.config import TEMP_PATH

from app.services.speech import transcribe_audio

from app.services.tts import generate_speech

from app.services.llm import generate_answer

from app.rag.retriever import (
    retrieve_documents,
    build_context
)


router = APIRouter(
    prefix="/api/voice",
    tags=["Voice"]
)


os.makedirs(
    TEMP_PATH,
    exist_ok=True
)


@router.post("/ask")
async def ask_voice(
    file: UploadFile = File(...)
):

    input_filename = (
        f"{uuid.uuid4()}_input.webm"
    )

    output_filename = (
        f"{uuid.uuid4()}_response.mp3"
    )

    input_path = os.path.join(
        TEMP_PATH,
        input_filename
    )

    output_path = os.path.join(
        TEMP_PATH,
        output_filename
    )

    try:

        audio_bytes = await file.read()

        with open(
            input_path,
            "wb"
        ) as audio_file:

            audio_file.write(
                audio_bytes
            )

        # -------------------------
        # STEP 1
        # Speech → Text
        # -------------------------

        question = transcribe_audio(
            input_path
        )

        if not question.strip():

            raise HTTPException(
                status_code=400,
                detail="Could not understand the audio."
            )

        # -------------------------
        # STEP 2
        # Retrieve
        # -------------------------

        documents, metadatas = (
            retrieve_documents(question)
        )

        # -------------------------
        # STEP 3
        # Context
        # -------------------------

        context = build_context(
            documents,
            metadatas
        )

        # -------------------------
        # STEP 4
        # LLM
        # -------------------------

        answer = generate_answer(
            question,
            context
        )

        # -------------------------
        # STEP 5
        # Text → Speech
        # -------------------------

        generate_speech(
            answer,
            output_path
        )

        sources = list(
            {
                metadata.get(
                    "source",
                    "Unknown"
                )
                for metadata in metadatas
            }
        )

        return {
            "success": True,
            "question": question,
            "answer": answer,
            "sources": sources,
            "audio_url": (
                f"/api/voice/audio/"
                f"{output_filename}"
            )
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/audio/{filename}")
async def get_audio(
    filename: str
):

    file_path = os.path.join(
        TEMP_PATH,
        filename
    )

    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=404,
            detail="Audio not found."
        )

    return FileResponse(
        file_path,
        media_type="audio/mpeg"
    )