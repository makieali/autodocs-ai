"""Health and info endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from autodocs_ai import __version__
from autodocs_ai.api.models import HealthResponse, ProviderInfo, TemplateInfo
from autodocs_ai.config import ProviderName, get_settings
from autodocs_ai.core.prompts import TEMPLATE_INSTRUCTIONS

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check API health status."""
    return HealthResponse(status="ok", version=__version__)


@router.get("/templates", response_model=list[TemplateInfo])
async def list_templates() -> list[TemplateInfo]:
    """List all available document templates."""
    return [
        TemplateInfo(name=name, description=desc)
        for name, desc in TEMPLATE_INSTRUCTIONS.items()
    ]


@router.get("/providers", response_model=list[ProviderInfo])
async def list_providers() -> list[ProviderInfo]:
    """List all available AI providers and their configuration status."""
    settings = get_settings()
    providers = [
        (ProviderName.OPENAI, bool(settings.openai_api_key)),
        (ProviderName.ANTHROPIC, bool(settings.anthropic_api_key)),
        (ProviderName.GEMINI, bool(settings.google_api_key)),
        (ProviderName.AZURE, bool(settings.azure_openai_api_key)),
        (ProviderName.OLLAMA, True),  # No key needed
    ]
    return [
        ProviderInfo(
            name=name.value,
            configured=configured,
            active=name == settings.provider,
        )
        for name, configured in providers
    ]
