from app.services.rag_service import retrieve_context
from app.services.gemini_service import generate_answer


question = "What is the maximum paper capacity of the Acme X500 printer?"


# 1. Retrieve relevant chunks
chunks = retrieve_context(question)


# 2. Check whether anything relevant was found
if not chunks:
    print("No relevant information found in Pinecone.")
else:

    # 3. Combine retrieved chunks
    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    print("========== RETRIEVED CONTEXT ==========")
    print(context)

    # 4. Send context + question to Gemini
    answer = generate_answer(
        question=question,
        context=context,
    )

    print("\n========== GEMINI ANSWER ==========")
    print(answer)