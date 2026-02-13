"""Word document content extractor."""

from __future__ import annotations

from pathlib import Path

from autodocs_ai.extractors.base import ExtractionError, FileExtractor


class WordExtractor(FileExtractor):
    """Extract text content from Word (.docx) files."""

    def supported_extensions(self) -> list[str]:
        return [".docx"]

    def extract(self, file_path: Path) -> str:
        try:
            from docx import Document
        except ImportError:
            raise ExtractionError(
                "python-docx is required for Word extraction. "
                "Install with: pip install autodocs-ai[extractors]"
            )

        try:
            doc = Document(str(file_path))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n\n".join(paragraphs)
        except Exception as e:
            raise ExtractionError(f"Failed to extract Word document: {e}") from e
