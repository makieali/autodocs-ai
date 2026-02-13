"""Configuration management using Pydantic Settings."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProviderName(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    AZURE = "azure"
    OLLAMA = "ollama"


class RendererName(str, Enum):
    TYPST = "typst"
    LATEX = "latex"


class OutputFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    MARKDOWN = "markdown"


class TemplateName(str, Enum):
    RESUME = "resume"
    INVOICE = "invoice"
    PROPOSAL = "proposal"
    REPORT = "report"
    RESEARCH_PAPER = "research_paper"
    COVER_LETTER = "cover_letter"
    MEETING_NOTES = "meeting_notes"
    PROJECT_CHARTER = "project_charter"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AUTODOCS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # AI Provider
    provider: ProviderName = ProviderName.OPENAI

    # OpenAI
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", alias="OPENAI_MODEL")

    # Anthropic
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(
        default="claude-sonnet-4-20250514", alias="ANTHROPIC_MODEL"
    )

    # Google Gemini
    google_api_key: Optional[str] = Field(default=None, alias="GOOGLE_API_KEY")
    gemini_model: str = Field(default="gemini-2.0-flash", alias="GEMINI_MODEL")

    # Azure OpenAI
    azure_openai_api_key: Optional[str] = Field(default=None, alias="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: Optional[str] = Field(default=None, alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_deployment: Optional[str] = Field(
        default=None, alias="AZURE_OPENAI_DEPLOYMENT"
    )
    azure_openai_api_version: str = Field(
        default="2024-06-01", alias="AZURE_OPENAI_API_VERSION"
    )

    # Ollama
    ollama_host: str = Field(default="http://localhost:11434", alias="OLLAMA_HOST")
    ollama_model: str = Field(default="llama3.1", alias="OLLAMA_MODEL")

    # Rendering
    renderer: RendererName = RendererName.TYPST

    # Output
    output_dir: Path = Path("./output")

    # API server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_key: Optional[str] = None

    # Document generation
    language: str = "english"
    max_tokens: int = 4096


def get_settings(**overrides: object) -> Settings:
    """Get application settings with optional overrides."""
    return Settings(**overrides)  # type: ignore[arg-type]
