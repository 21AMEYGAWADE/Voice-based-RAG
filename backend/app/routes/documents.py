import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from app.config import DOCUMENTS_PATH

from app.rag.ingest import ingest_pdf


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


os.makedirs(
    DOCUMENTS_PATH,
    exist_ok=True
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_path = os.path.join(
        DOCUMENTS_PATH,
        file.filename
    )

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        result = ingest_pdf(
            file_path
        )

        return {
            "success": True,
            "message": "Document uploaded successfully.",
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )