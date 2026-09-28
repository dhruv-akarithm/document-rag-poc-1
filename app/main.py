import shutil
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.ingestion_service import ingest_document
from app.services.rag_service import retrieve_context
from app.services.gemini_service import generate_answer


app = FastAPI(
    title="Document RAG Admin Panel",
    version="1.0.0",
)


BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.post("/upload")
async def upload_documents(
    files: list[UploadFile] = File(...)
):
    results = []

    for file in files:

        if not file.filename.lower().endswith(".pdf"):
            results.append(
                {
                    "filename": file.filename,
                    "status": "error",
                    "message": "Only PDF files are supported.",
                }
            )
            continue

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        try:

            result = ingest_document(
                file_path=str(file_path),
                document_name=file.filename,
            )

            if result["status"] == "already_indexed":
                results.append(
                    {
                        "filename": file.filename,
                        "status": "already_indexed",
                        "message": "Document is already indexed.",
                    }
                )
            else:
                results.append(
                    {
                        "filename": file.filename,
                        "status": "success",
                        "message": (
                            f"Uploaded and indexed "
                            f"{result['chunk_count']} chunk(s)."
                        ),
                    }
                )

        except Exception as e:

            results.append(
                {
                    "filename": file.filename,
                    "status": "error",
                    "message": str(e),
                }
            )

    return {
        "results": results
    }


@app.post("/ask")
async def ask_question(question: str):
    question = question.strip()

    if not question:
        return {
            "answer": "Please enter a question.",
            "sources": [],
        }

    chunks = retrieve_context(question)

    if not chunks:
        return {
            "answer": (
                "I don't have enough information in "
                "the uploaded documents to answer that."
            ),
            "sources": [],
        }

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    answer = generate_answer(
        question=question,
        context=context,
    )

    sources = [
        {
            "document": chunk["document"],
            "chunk": chunk["chunk_index"],
            "score": round(chunk["score"], 4),
        }
        for chunk in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }