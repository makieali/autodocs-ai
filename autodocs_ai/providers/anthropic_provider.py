"""Anthropic Claude provider implementation."""

from __future__ import annotations

from autodocs_ai.config import Settings
from autodocs_ai.providers.base import AIProvider, GenerationResult


class AnthropicProvider(AIProvider):
    """Provider for Anthropic's Messages API."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = None

    def validate_config(self) -> None:
        if not self.settings.anthropic_api_key:
            raise ValueError(
                "Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable."
            )

    def _get_client(self):
        if self._client is None:
            try:
                from anthropic import AsyncAnthropic
            except ImportError:
                raise ImportError(
                    "anthropic package is required. Install with: pip install autodocs-ai[anthropic]"
                )
            self.validate_config()
            self._client = AsyncAnthropic(api_key=self.settings.anthropic_api_key)
        return self._client

    async def generate(self, system_prompt: str, user_prompt: str) -> GenerationResult:
        client = self._get_client()
        response = await client.messages.create(
            model=self.settings.anthropic_model,
            max_tokens=self.settings.max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )
        content = ""
        for block in response.content:
            if block.type == "text":
                content += block.text
        usage = {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
        return GenerationResult(
            content=content,
            model=self.settings.anthropic_model,
            provider="anthropic",
            usage=usage,
        )
