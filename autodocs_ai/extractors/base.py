"""Base extractor interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class FileExtractor(ABC):
    """Abstract base class for file content extractors."""

    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions (e.g., ['.pdf', '.PDF'])."""

    @abstractmethod
    def extract(self, file_path: Path) -> str:
        """Extract text content from a file.

        Args:
            file_path: Path to the file to extract.

        Returns:
            Extracted text content.

        Raises:
            ExtractionError: If extraction fails.
        """


class ExtractionError(Exception):
    """Raised when file extraction fails."""
