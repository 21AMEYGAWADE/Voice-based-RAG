import chromadb

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


def retrieve_documents(
    query: str,
    number_of_results: int = 5
):

    results = collection.query(
        query_texts=[query],
        n_results=number_of_results
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    return documents, metadatas


def build_context(documents, metadatas):

    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        source = metadata.get(
            "source",
            "Unknown"
        )

        context_parts.append(
            f"Source: {source}\n{document}"
        )

    return "\n\n".join(context_parts)