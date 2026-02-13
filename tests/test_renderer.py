"""Tests for document rendering engine."""

from __future__ import annotations

import pytest
from pathlib import Path

from autodocs_ai.config import RendererName
from autodocs_ai.core.renderer import (
    RenderError,
    render,
    render_html,
    render_markdown,
)


class TestRenderHTML:
    def test_writes_html_file(self, tmp_path: Path):
        source = "<html><body><h1>Test</h1></body></html>"
        output = tmp_path / "test.html"
        result = render_html(source, output)
        assert result == output
        assert output.exists()
        assert output.read_text() == source

    def test_creates_parent_dirs(self, tmp_path: Path):
        output = tmp_path / "sub" / "dir" / "test.html"
        render_html("<html></html>", output)
        assert output.exists()


class TestRenderMarkdown:
    def test_writes_markdown_file(self, tmp_path: Path):
        source = "# Hello\n\nThis is a test."
        output = tmp_path / "test.md"
        result = render_markdown(source, output)
        assert result == output
        assert output.exists()
        assert output.read_text() == source


class TestRenderDispatch:
    def test_dispatches_to_html(self, tmp_path: Path):
        output = tmp_path / "test.html"
        result = render("<html></html>", output, output_format="html")
        assert result == output

    def test_dispatches_to_markdown(self, tmp_path: Path):
        output = tmp_path / "test.md"
        result = render("# Test", output, output_format="markdown")
        assert result == output

    def test_unsupported_format_raises(self, tmp_path: Path):
        output = tmp_path / "test.xyz"
        with pytest.raises(RenderError, match="Unsupported"):
            render("content", output, output_format="xyz")


class TestRenderDocx:
    def test_renders_docx(self, tmp_path: Path):
        pytest.importorskip("docx")
        source = "# Title\n\nParagraph text.\n\n- Item 1\n- Item 2"
        output = tmp_path / "test.docx"
        result = render(source, output, output_format="docx")
        assert result == output
        assert output.exists()
        assert output.stat().st_size > 0
