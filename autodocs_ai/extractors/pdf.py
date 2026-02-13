"""PDF content extractor."""

from __future__ import annotations

from pathlib import Path

from autodocs_ai.extractors.base import ExtractionError, FileExtractor


class PDFExtractor(FileExtractor):
    """Extract text content from PDF files."""

    def supported_extensions(self) -> list[str]:
        return [".pdf"]

    def extract(self, file_path: Path) -> str:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ExtractionError(
                "PyPDF2 is required for PDF extraction. "
                "Install with: pip install autodocs-ai[extractors]"
            )

        try:
            reader = PdfReader(str(file_path))
            pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
            return "\n\n".join(pages)
        except Exception as e:
            raise ExtractionError(f"Failed to extract PDF: {e}") from e
