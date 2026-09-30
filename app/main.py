import shutil
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.ingestion_service import ingest_document
from app.services.rag_service import retrieve_context
from app.services.gemini_service import generate_answer
from app.services.model_registry import ModelRegistry
from app.services.model_manager import ModelManager


app = FastAPI(
    title="Document RAG Admin Panel",
    version="1.0.0",
)

model_registry = ModelRegistry()
model_manager = ModelManager()

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

class ModelSwitchRequest(BaseModel):
    role: str
    model_id: str

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

@app.get("/models")
async def get_models():

    return {
        "models": model_registry.get_all_models(),
        "active_roles": {
            "cheap_fast": model_registry.get_active_model(
                "cheap_fast"
            ),
            "powerful": model_registry.get_active_model(
                "powerful"
            ),
        },
    }

@app.post("/models/switch")
async def switch_model(
    request: ModelSwitchRequest
):

    if request.role not in [
        "cheap_fast",
        "powerful",
    ]:
        return {
            "success": False,
            "message": "Invalid model role.",
        }

    try:

        model_registry.set_active_model(
            role=request.role,
            model_id=request.model_id,
        )

        return {
            "success": True,
            "message": (
                f"Switched {request.role} "
                f"to {request.model_id}"
            ),
        }

    except ValueError as error:

        return {
            "success": False,
            "message": str(error),
        }

@app.get("/models/lifecycle")
async def model_lifecycle():

    models = model_registry.get_all_models()

    warnings = []

    for model_id, model in models.items():

        if model["status"] in [
            "deprecated",
            "shutdown",
        ]:

            warnings.append(
                {
                    "model": model_id,
                    "status": model["status"],
                    "replacement": model["replacement"],
                    "shutdown_date": model["shutdown_date"],
                    "pricing": model["pricing"],
                }
            )

    return {
        "warnings": warnings
    }

@app.get("/models/availability")
async def model_availability():

    results = []

    for model_id in model_registry.get_all_models():

        result = model_manager.check_model_availability(
            model_id
        )

        results.append(result)

    return {
        "models": results
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

    try:
        answer = generate_answer(
            question=question,
            context=context,
        )
    except RuntimeError:
        return {
            "answer": (
                "The configured AI models are currently unavailable. "
                "Please try again later."
            ),
            "sources": sources,
        }

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