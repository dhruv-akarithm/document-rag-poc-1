from app.services.embeddings import generate_embeddings
from app.services.pinecone_service import index


MIN_SIMILARITY_SCORE = 0.60


def retrieve_context(
    question: str,
    top_k: int = 3,
) -> list[dict]:

    question_embedding = generate_embeddings([question])[0]

    results = index.query(
        vector=question_embedding.tolist(),
        top_k=top_k,
        include_metadata=True,
    )

    relevant_chunks = []

    for match in results["matches"]:
        if match["score"] >= MIN_SIMILARITY_SCORE:
            relevant_chunks.append(
                {
                    "score": match["score"],
                    "document": match["metadata"]["document"],
                    "chunk_index": match["metadata"]["chunk_index"],
                    "text": match["metadata"]["text"],
                }
            )

    return relevant_chunks