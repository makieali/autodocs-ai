"""AI provider implementations."""

from __future__ import annotations

from autodocs_ai.config import ProviderName, Settings
from autodocs_ai.providers.base import AIProvider, GenerationResult


def get_provider(settings: Settings) -> AIProvider:
    """Create an AI provider instance based on settings.

    Args:
        settings: Application settings containing provider configuration.

    Returns:
        An AIProvider instance for the configured provider.

    Raises:
        ValueError: If the provider is unknown.
    """
    if settings.provider == ProviderName.OPENAI:
        from autodocs_ai.providers.openai_provider import OpenAIProvider

        return OpenAIProvider(settings)
    elif settings.provider == ProviderName.ANTHROPIC:
        from autodocs_ai.providers.anthropic_provider import AnthropicProvider

        return AnthropicProvider(settings)
    elif settings.provider == ProviderName.GEMINI:
        from autodocs_ai.providers.gemini_provider import GeminiProvider

        return GeminiProvider(settings)
    elif settings.provider == ProviderName.AZURE:
        from autodocs_ai.providers.azure_provider import AzureProvider

        return AzureProvider(settings)
    elif settings.provider == ProviderName.OLLAMA:
        from autodocs_ai.providers.ollama_provider import OllamaProvider

        return OllamaProvider(settings)
    else:
        raise ValueError(f"Unknown provider: {settings.provider}")


__all__ = ["AIProvider", "GenerationResult", "get_provider"]
