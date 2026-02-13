"""Request and response models for the API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateDocumentRequest(BaseModel):
    """Request body for document generation."""

    prompt: str = Field(..., description="The prompt describing the document to generate.")
    template: str | None = Field(None, description="Document template name.")
    output_format: str = Field("pdf", description="Output format: pdf, docx, html, markdown.")
    input_content: str | None = Field(None, description="Additional input content to incorporate.")
    language: str | None = Field(None, description="Document language (default: english).")
    renderer: str | None = Field(None, description="Rendering engine: typst or latex.")
    provider: str | None = Field(None, description="AI provider override.")


class GenerateDocumentResponse(BaseModel):
    """Response from document generation."""

    output_path: str
    output_format: str
    model: str
    provider: str
    usage: dict | None = None


class TemplateInfo(BaseModel):
    """Information about a template."""

    name: str
    description: str


class ProviderInfo(BaseModel):
    """Information about an AI provider."""

    name: str
    configured: bool
    active: bool


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    version: str
