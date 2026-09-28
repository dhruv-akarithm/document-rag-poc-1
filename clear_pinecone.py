from app.services.pinecone_service import index


index.delete(delete_all=True)

print("All vectors deleted from Pinecone.")