from app.services.document_loader import extract_text
from app.services.chunker import chunk_text


file_path = "documents/product_manual.pdf"

text = extract_text(file_path)

chunks = chunk_text(text)

print(f"Number of chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\n========== CHUNK {i} ==========")
    print(chunk)