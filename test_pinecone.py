import os

from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")

pc = Pinecone(api_key=api_key)

index = pc.Index(index_name)

print("Connected to Pinecone!")
print("Index:", index_name)
print("Stats:", index.describe_index_stats())