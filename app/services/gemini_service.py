import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(question: str, context: str) -> str:

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question ONLY using the provided document context.

If the answer cannot be found in the context, say:
"I don't have enough information in the uploaded documents to answer that."

Do not use outside knowledge.

Document context:
----------------
{context}
----------------

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text