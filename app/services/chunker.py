import re


def chunk_text(text: str) -> list[str]:
    """
    Split extracted document text into sentence-level chunks.

    This is intentionally simple for the POC so that
    specific questions can retrieve focused information.
    """

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    # Split on sentence-ending punctuation
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text,
    )

    chunks = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    return chunks