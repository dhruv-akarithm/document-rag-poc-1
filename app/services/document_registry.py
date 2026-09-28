import hashlib
import json
from pathlib import Path


REGISTRY_FILE = Path("uploads/document_registry.json")


def calculate_file_hash(file_path: str) -> str:
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def load_registry() -> dict:
    if not REGISTRY_FILE.exists():
        return {}

    with open(REGISTRY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_registry(registry: dict):
    REGISTRY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        REGISTRY_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            registry,
            file,
            indent=2,
        )


def is_document_indexed(file_hash: str) -> bool:
    registry = load_registry()

    return file_hash in registry


def register_document(
    file_hash: str,
    document_name: str,
    chunk_count: int,
):
    registry = load_registry()

    registry[file_hash] = {
        "document": document_name,
        "chunk_count": chunk_count,
    }

    save_registry(registry)