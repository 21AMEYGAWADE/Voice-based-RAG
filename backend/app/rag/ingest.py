import os

import chromadb

from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)

from app.config import (
    CHROMA_PATH,
    COLLECTION_NAME
)


embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)


def extract_pdf_text(file_path: str):

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def create_chunks(text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_text(text)


def ingest_pdf(file_path: str):

    filename = os.path.basename(file_path)

    text = extract_pdf_text(file_path)

    if not text.strip():

        raise ValueError(
            "No readable text found in the PDF."
        )

    chunks = create_chunks(text)

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        chunk_id = f"{filename}-{index}"

        ids.append(chunk_id)

        documents.append(chunk)

        metadatas.append({
            "source": filename,
            "chunk": index
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    return {
        "filename": filename,
        "chunks": len(chunks)
    }