import os

from dotenv import load_dotenv
from pinecone import Pinecone


load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY is not set")

if not PINECONE_INDEX_NAME:
    raise ValueError("PINECONE_INDEX_NAME is not set")


pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(PINECONE_INDEX_NAME)

def upsert_chunks(
    document_name: str,
    document_id: str,
    chunks: list[str],
    embeddings,
):
    vectors = []

    for i, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        vector_id = f"{document_id}_{i}"

        vectors.append(
            {
                "id": vector_id,
                "values": embedding.tolist(),
                "metadata": {
                    "document": document_name,
                    "document_id": document_id,
                    "chunk_index": i,
                    "text": chunk,
                },
            }
        )

    index.upsert(vectors=vectors)

    return len(vectors)