"""Plain text and Markdown content extractor."""

from __future__ import annotations

from pathlib import Path

from autodocs_ai.extractors.base import ExtractionError, FileExtractor


class TextExtractor(FileExtractor):
    """Extract content from text-based files."""

    def supported_extensions(self) -> list[str]:
        return [
            ".txt",
            ".md",
            ".markdown",
            ".rst",
            ".py",
            ".js",
            ".ts",
            ".java",
            ".go",
            ".rs",
            ".c",
            ".cpp",
            ".h",
            ".hpp",
            ".rb",
            ".php",
            ".sh",
            ".yaml",
            ".yml",
            ".toml",
            ".json",
            ".xml",
            ".html",
            ".css",
            ".sql",
            ".r",
            ".R",
        ]

    def extract(self, file_path: Path) -> str:
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            try:
                return file_path.read_text(encoding="latin-1")
            except Exception as e:
                raise ExtractionError(f"Failed to read text file: {e}") from e
        except Exception as e:
            raise ExtractionError(f"Failed to read text file: {e}") from e
