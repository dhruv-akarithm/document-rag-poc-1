# Document RAG POC

A basic Retrieval-Augmented Generation (RAG) application built with FastAPI, Sentence Transformers, Pinecone, and Gemini.

## Architecture

PDF
↓
Text Extraction
↓
Chunking
↓
Sentence Transformer Embeddings
↓
Pinecone Vector Database
↓
Semantic Retrieval
↓
Gemini
↓
Answer

## Features

- Upload one or multiple PDF documents
- Extract text from PDFs
- Split documents into chunks
- Generate embeddings using Sentence Transformers
- Store embeddings in Pinecone
- Retrieve relevant document chunks
- Generate answers using Gemini
- Display retrieved source documents
- Prevent duplicate document indexing

## Technologies

- Python
- FastAPI
- Sentence Transformers
- Pinecone
- Google Gemini API
- PyPDF
- Jinja2

## Requirements

- Python 3.11+
- Pinecone account
- Gemini API key

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/dhruv-akarithm/document-rag-poc-1.git
cd document-rag-poc
```

### 2. Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=document-rag
```

### 5. Start the application

```bash
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

## Usage

1. Upload one or more PDF documents.
2. The application extracts the text.
3. Documents are split into chunks.
4. Sentence Transformer generates embeddings.
5. Embeddings are stored in Pinecone.
6. Enter a question.
7. The question is converted into an embedding.
8. Pinecone retrieves relevant chunks.
9. Gemini generates an answer using the retrieved context.

## RAG Demonstration

The application demonstrates the difference before and after a document is uploaded.

**Before upload**

Ask a question about information that does not exist in the Pinecone knowledge base.

The application responds:

> I don't have enough information in the uploaded documents to answer that.

**After upload**

Upload the document containing the information and ask the exact same question again.

The system retrieves the relevant chunk from Pinecone and Gemini generates the answer using that context.

### Example

**Question:**

What is the warranty period of the Acme X500 printer?

**Before uploading the warranty document:**

I don't have enough information in the uploaded documents to answer that.

**After uploading the warranty document:**

The Acme X500 printer has a two-year limited warranty from the date of purchase.

## Notes

API keys are stored in environment variables and should never be committed to GitHub.

## Task 2 — Model Lifecycle Management

Task 2 extends the original RAG POC with a model management layer.

### Architecture

User/Admin Panel
        |
        v
FastAPI
        |
        +-------------------+
        |                   |
        v                   v
    RAG Service       Model Manager
        |                   |
        v                   v
    Pinecone          Model Registry
                            |
                    +-------+-------+
                    |               |
                    v               v
               Primary Model    Fallback Model

### Model Roles

#### Cheap / Fast Model

Used for:

- Routing
- OCR
- Basic tasks
- Lightweight processing

#### Powerful Model

Used for:

- Final answer generation
- Complex reasoning
- Hard accounting questions

### Model Registry

The model registry stores:

- Model ID
- Display name
- Role
- Capabilities
- Lifecycle status
- Pricing metadata
- Free-tier information
- Recommended replacement
- Shutdown date
- Fallback models

### Model Switching

Administrators can switch the active model from the admin panel without changing application code.

### Fallback

If the primary model encounters a fallback-safe failure such as temporary unavailability or rate limiting, the Model Manager attempts the configured fallback model.

### Lifecycle Management

Deprecated and shutdown models cannot be selected as active models.

The admin panel can display:

- Lifecycle status
- Recommended replacement
- Shutdown date
- Pricing information

### Availability

The application exposes model availability information through:

`GET /models/availability`

### Model Management APIs

- `GET /models`
- `POST /models/switch`
- `GET /models/lifecycle`
- `GET /models/availability`
