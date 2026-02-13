"""File content extractors."""

from __future__ import annotations

from pathlib import Path

from autodocs_ai.extractors.base import ExtractionError, FileExtractor
from autodocs_ai.extractors.excel import ExcelExtractor
from autodocs_ai.extractors.pdf import PDFExtractor
from autodocs_ai.extractors.text import TextExtractor
from autodocs_ai.extractors.word import WordExtractor

# Registry of all extractors
_EXTRACTORS: list[FileExtractor] = [
    PDFExtractor(),
    ExcelExtractor(),
    WordExtractor(),
    TextExtractor(),  # Keep last — it's the most permissive
]


def extract_file(file_path: Path) -> str:
    """Extract text content from a file using the appropriate extractor.

    Args:
        file_path: Path to the file to extract.

    Returns:
        Extracted text content.

    Raises:
        ExtractionError: If no extractor supports the file type or extraction fails.
    """
    ext = file_path.suffix.lower()

    for extractor in _EXTRACTORS:
        if ext in extractor.supported_extensions():
            return extractor.extract(file_path)

    # Fall back to text extractor for unknown extensions
    try:
        return TextExtractor().extract(file_path)
    except Exception:
        raise ExtractionError(
            f"No extractor found for file type '{ext}'. "
            f"Supported types: {get_supported_extensions()}"
        )


def get_supported_extensions() -> list[str]:
    """Get all supported file extensions."""
    extensions = []
    for extractor in _EXTRACTORS:
        extensions.extend(extractor.supported_extensions())
    return sorted(set(extensions))


__all__ = [
    "ExtractionError",
    "FileExtractor",
    "extract_file",
    "get_supported_extensions",
]
