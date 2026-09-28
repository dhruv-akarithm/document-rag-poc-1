from app.services.document_loader import extract_text
from app.services.chunker import chunk_text
from app.services.embeddings import generate_embeddings
from app.services.pinecone_service import upsert_chunks


file_path = "documents/product_manual.pdf"

document_name = "product_manual.pdf"


# 1. Extract text
text = extract_text(file_path)

print("Text extracted.")


# 2. Create chunks
chunks = chunk_text(text)

print(f"Created {len(chunks)} chunk(s).")


# 3. Generate embeddings
embeddings = generate_embeddings(chunks)

print(f"Generated embeddings with shape: {embeddings.shape}")


# 4. Upload to Pinecone
count = upsert_chunks(
    document_name=document_name,
    chunks=chunks,
    embeddings=embeddings,
)

print(f"Uploaded {count} vector(s) to Pinecone.")