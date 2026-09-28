from app.services.document_loader import extract_text


file_path = "documents/product_manual.pdf"

text = extract_text(file_path)

print("========== EXTRACTED TEXT ==========")
print(text)
print("=====================================")