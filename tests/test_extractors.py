"""Tests for file content extractors."""

from __future__ import annotations

import pytest
from pathlib import Path

from autodocs_ai.extractors import extract_file, get_supported_extensions
from autodocs_ai.extractors.base import ExtractionError
from autodocs_ai.extractors.text import TextExtractor


class TestTextExtractor:
    def test_extracts_text_file(self, tmp_path: Path):
        file = tmp_path / "test.txt"
        file.write_text("Hello, world!")
        result = TextExtractor().extract(file)
        assert result == "Hello, world!"

    def test_extracts_markdown(self, tmp_path: Path):
        file = tmp_path / "test.md"
        file.write_text("# Title\n\nContent here.")
        result = TextExtractor().extract(file)
        assert "# Title" in result

    def test_extracts_code_file(self, tmp_path: Path):
        file = tmp_path / "test.py"
        file.write_text("def hello():\n    print('hello')")
        result = TextExtractor().extract(file)
        assert "def hello" in result

    def test_supported_extensions(self):
        ext = TextExtractor()
        exts = ext.supported_extensions()
        assert ".txt" in exts
        assert ".md" in exts
        assert ".py" in exts
        assert ".json" in exts


class TestExtractFile:
    def test_extracts_text_file(self, tmp_path: Path):
        file = tmp_path / "test.txt"
        file.write_text("test content")
        result = extract_file(file)
        assert result == "test content"

    def test_extracts_markdown_file(self, tmp_path: Path):
        file = tmp_path / "readme.md"
        readme_content = "# README\n\nThis is a readme."
        file.write_text(readme_content)
        result = extract_file(file)
        assert result == readme_content

    def test_extracts_csv_file(self, tmp_path: Path):
        pytest.importorskip("pandas")
        file = tmp_path / "data.csv"
        file.write_text("name,age\nAlice,30\nBob,25")
        result = extract_file(file)
        assert "Alice" in result
        assert "Bob" in result

    def test_unknown_extension_falls_back_to_text(self, tmp_path: Path):
        file = tmp_path / "data.custom"
        file.write_text("custom format content")
        result = extract_file(file)
        assert result == "custom format content"


class TestSupportedExtensions:
    def test_returns_sorted_unique_list(self):
        exts = get_supported_extensions()
        assert len(exts) == len(set(exts))
        assert exts == sorted(exts)

    def test_includes_common_types(self):
        exts = get_supported_extensions()
        assert ".txt" in exts
        assert ".md" in exts
        assert ".csv" in exts
        assert ".pdf" in exts
        assert ".docx" in exts
