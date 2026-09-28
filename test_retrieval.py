from app.services.embeddings import generate_embeddings
from app.services.pinecone_service import index


question = "What is the recommended maintenance interval?"


# Generate embedding for the question
question_embedding = generate_embeddings([question])[0]


# Search Pinecone
results = index.query(
    vector=question_embedding.tolist(),
    top_k=3,
    include_metadata=True,
)


print("\n========== SEARCH RESULTS ==========\n")

for match in results["matches"]:
    print("ID:", match["id"])
    print("Score:", match["score"])
    print("Document:", match["metadata"]["document"])
    print("Chunk:", match["metadata"]["chunk_index"])
    print("Text:")
    print(match["metadata"]["text"])
    print("------------------------------------")