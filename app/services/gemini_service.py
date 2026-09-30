from app.services.model_manager import ModelManager


model_manager = ModelManager()


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

    return model_manager.generate(
        role="powerful",
        prompt=prompt,
    )