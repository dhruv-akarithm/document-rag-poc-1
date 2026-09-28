import uuid

from app.services.document_loader import extract_text
from app.services.chunker import chunk_text
from app.services.embeddings import generate_embeddings
from app.services.pinecone_service import upsert_chunks
from app.services.document_registry import (
    calculate_file_hash,
    is_document_indexed,
    register_document,
)


def ingest_document(
    file_path: str,
    document_name: str,
) -> dict:

    # Calculate unique hash for the document
    file_hash = calculate_file_hash(file_path)

    # Prevent duplicate indexing
    if is_document_indexed(file_hash):
        return {
            "status": "already_indexed",
            "chunk_count": 0,
        }

    # Extract text
    text = extract_text(file_path)

    if not text.strip():
        raise ValueError(
            f"No text could be extracted from {document_name}"
        )

    # Chunk document
    chunks = chunk_text(text)

    if not chunks:
        raise ValueError(
            f"No chunks were generated for {document_name}"
        )

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Generate unique document ID
    document_id = str(uuid.uuid4())

    # Upload to Pinecone
    count = upsert_chunks(
        document_name=document_name,
        document_id=document_id,
        chunks=chunks,
        embeddings=embeddings,
    )

    # Register successful ingestion
    register_document(
        file_hash=file_hash,
        document_name=document_name,
        chunk_count=count,
    )

    return {
        "status": "indexed",
        "chunk_count": count,
    }