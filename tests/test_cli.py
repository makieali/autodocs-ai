"""Tests for the CLI interface."""

from __future__ import annotations

from typer.testing import CliRunner

from autodocs_ai import __version__
from autodocs_ai.cli import app

runner = CliRunner()


class TestCLIBasic:
    def test_version_flag(self):
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert __version__ in result.stdout

    def test_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "autodocs-ai" in result.stdout

    def test_generate_help(self):
        result = runner.invoke(app, ["generate", "--help"])
        assert result.exit_code == 0
        assert "prompt" in result.stdout.lower()

    def test_serve_help(self):
        result = runner.invoke(app, ["serve", "--help"])
        assert result.exit_code == 0
        assert "host" in result.stdout.lower()

    def test_setup_help(self):
        result = runner.invoke(app, ["setup", "--help"])
        assert result.exit_code == 0

    def test_check_runs(self):
        result = runner.invoke(app, ["check"])
        assert result.exit_code == 0
        assert "Python" in result.stdout

    def test_templates_command(self):
        result = runner.invoke(app, ["templates"])
        assert result.exit_code == 0
        assert "resume" in result.stdout.lower()
        assert "invoice" in result.stdout.lower()


class TestCLIGenerate:
    def test_generate_requires_prompt(self):
        result = runner.invoke(app, ["generate"])
        assert result.exit_code != 0

    def test_generate_with_json_flag_on_error(self):
        # Should fail gracefully with --json flag (no API key configured)
        result = runner.invoke(app, ["generate", "test prompt", "--json"])
        # Will fail because no provider is configured, but should not crash
        assert result.exit_code == 1
