"""Tests for AI provider system."""

from __future__ import annotations

import pytest

from autodocs_ai.config import ProviderName, Settings
from autodocs_ai.providers import get_provider
from autodocs_ai.providers.base import AIProvider, GenerationResult
from autodocs_ai.providers.openai_provider import OpenAIProvider
from autodocs_ai.providers.anthropic_provider import AnthropicProvider
from autodocs_ai.providers.gemini_provider import GeminiProvider
from autodocs_ai.providers.azure_provider import AzureProvider
from autodocs_ai.providers.ollama_provider import OllamaProvider


def _make_settings(**kwargs) -> Settings:
    """Create settings with defaults for testing (ignores .env file)."""
    defaults: dict = {
        "provider": "openai",
        "openai_api_key": "test-key",
    }
    defaults.update(kwargs)
    return Settings(_env_file=None, **defaults)


class TestGetProvider:
    def test_returns_openai_provider(self):
        settings = _make_settings(provider="openai")
        provider = get_provider(settings)
        assert isinstance(provider, OpenAIProvider)

    def test_returns_anthropic_provider(self):
        settings = _make_settings(provider="anthropic")
        provider = get_provider(settings)
        assert isinstance(provider, AnthropicProvider)

    def test_returns_gemini_provider(self):
        settings = _make_settings(provider="gemini")
        provider = get_provider(settings)
        assert isinstance(provider, GeminiProvider)

    def test_returns_azure_provider(self):
        settings = _make_settings(provider="azure")
        provider = get_provider(settings)
        assert isinstance(provider, AzureProvider)

    def test_returns_ollama_provider(self):
        settings = _make_settings(provider="ollama")
        provider = get_provider(settings)
        assert isinstance(provider, OllamaProvider)

    def test_all_providers_are_ai_provider(self):
        for name in ProviderName:
            settings = _make_settings(provider=name.value)
            provider = get_provider(settings)
            assert isinstance(provider, AIProvider)


class TestProviderValidation:
    def test_openai_requires_api_key(self):
        settings = _make_settings(openai_api_key="")
        provider = OpenAIProvider(settings)
        with pytest.raises(ValueError, match="API key"):
            provider.validate_config()

    def test_anthropic_requires_api_key(self):
        settings = _make_settings(anthropic_api_key="")
        provider = AnthropicProvider(settings)
        with pytest.raises(ValueError, match="API key"):
            provider.validate_config()

    def test_gemini_requires_api_key(self):
        settings = _make_settings(google_api_key="")
        provider = GeminiProvider(settings)
        with pytest.raises(ValueError, match="API key"):
            provider.validate_config()

    def test_azure_requires_api_key(self):
        settings = _make_settings(azure_openai_api_key="")
        provider = AzureProvider(settings)
        with pytest.raises(ValueError, match="API key"):
            provider.validate_config()

    def test_azure_requires_endpoint(self):
        settings = _make_settings(
            azure_openai_api_key="key",
            azure_openai_endpoint="",
        )
        provider = AzureProvider(settings)
        with pytest.raises(ValueError, match="endpoint"):
            provider.validate_config()

    def test_azure_requires_deployment(self):
        settings = _make_settings(
            azure_openai_api_key="key",
            azure_openai_endpoint="https://example.openai.azure.com",
            azure_openai_deployment="",
        )
        provider = AzureProvider(settings)
        with pytest.raises(ValueError, match="deployment"):
            provider.validate_config()

    def test_ollama_requires_nothing(self):
        settings = _make_settings()
        provider = OllamaProvider(settings)
        provider.validate_config()  # Should not raise


class TestGenerationResult:
    def test_creation(self):
        result = GenerationResult(
            content="Hello, world!",
            model="gpt-4o",
            provider="openai",
            usage={"total_tokens": 100},
        )
        assert result.content == "Hello, world!"
        assert result.model == "gpt-4o"
        assert result.provider == "openai"
        assert result.usage == {"total_tokens": 100}

    def test_default_usage_is_none(self):
        result = GenerationResult(
            content="test",
            model="test",
            provider="test",
        )
        assert result.usage is None
