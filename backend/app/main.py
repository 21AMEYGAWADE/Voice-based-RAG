from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.routes.documents import router as document_router

from app.routes.voice import router as voice_router


app = FastAPI(
    title="Voice RAG API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    document_router
)

app.include_router(
    voice_router
)


@app.get("/")
def root():

    return {
        "message": "Voice RAG API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }