"""OpenAI provider implementation."""

from __future__ import annotations

from autodocs_ai.config import Settings
from autodocs_ai.providers.base import AIProvider, GenerationResult


class OpenAIProvider(AIProvider):
    """Provider for OpenAI's Chat Completions API."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = None

    def validate_config(self) -> None:
        if not self.settings.openai_api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable."
            )

    def _get_client(self):
        if self._client is None:
            try:
                from openai import AsyncOpenAI
            except ImportError:
                raise ImportError(
                    "openai package is required. Install with: pip install autodocs-ai[openai]"
                )
            self.validate_config()
            self._client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        return self._client

    async def generate(self, system_prompt: str, user_prompt: str) -> GenerationResult:
        client = self._get_client()
        response = await client.chat.completions.create(
            model=self.settings.openai_model,
            messages=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=self.settings.max_tokens,
        )
        choice = response.choices[0]
        usage = None
        if response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        return GenerationResult(
            content=choice.message.content or "",
            model=self.settings.openai_model,
            provider="openai",
            usage=usage,
        )
