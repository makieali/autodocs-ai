"""Excel and CSV content extractor."""

from __future__ import annotations

from pathlib import Path

from autodocs_ai.extractors.base import ExtractionError, FileExtractor


class ExcelExtractor(FileExtractor):
    """Extract text content from Excel and CSV files."""

    def supported_extensions(self) -> list[str]:
        return [".csv", ".xlsx", ".xls"]

    def extract(self, file_path: Path) -> str:
        try:
            import pandas as pd
        except ImportError:
            raise ExtractionError(
                "pandas is required for Excel/CSV extraction. "
                "Install with: pip install autodocs-ai[extractors]"
            )

        try:
            ext = file_path.suffix.lower()
            if ext == ".csv":
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            # Return as markdown table for AI consumption
            return df.to_markdown(index=False)
        except Exception as e:
            raise ExtractionError(f"Failed to extract {ext} file: {e}") from e
