from app.services.document_loader import extract_text
from app.services.chunker import chunk_text
from app.services.embeddings import generate_embeddings


file_path = "documents/product_manual.pdf"

text = extract_text(file_path)

chunks = chunk_text(text)

embeddings = generate_embeddings(chunks)

print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)

print("\nFirst embedding:")
print(embeddings[0])