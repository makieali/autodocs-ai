"""Azure OpenAI provider implementation."""

from __future__ import annotations

from autodocs_ai.config import Settings
from autodocs_ai.providers.base import AIProvider, GenerationResult


class AzureProvider(AIProvider):
    """Provider for Azure OpenAI Service."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = None

    def validate_config(self) -> None:
        if not self.settings.azure_openai_api_key:
            raise ValueError(
                "Azure OpenAI API key is required. Set AZURE_OPENAI_API_KEY environment variable."
            )
        if not self.settings.azure_openai_endpoint:
            raise ValueError(
                "Azure OpenAI endpoint is required. Set AZURE_OPENAI_ENDPOINT environment variable."
            )
        if not self.settings.azure_openai_deployment:
            raise ValueError(
                "Azure OpenAI deployment is required. "
                "Set AZURE_OPENAI_DEPLOYMENT environment variable."
            )

    def _get_client(self):
        if self._client is None:
            try:
                from openai import AsyncAzureOpenAI
            except ImportError:
                raise ImportError(
                    "openai package is required. Install with: pip install autodocs-ai[openai]"
                )
            self.validate_config()
            self._client = AsyncAzureOpenAI(
                api_key=self.settings.azure_openai_api_key,
                azure_endpoint=self.settings.azure_openai_endpoint,
                api_version=self.settings.azure_openai_api_version,
            )
        return self._client

    async def generate(self, system_prompt: str, user_prompt: str) -> GenerationResult:
        client = self._get_client()
        response = await client.chat.completions.create(
            model=self.settings.azure_openai_deployment,
            messages=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_completion_tokens=self.settings.max_tokens,
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
            model=self.settings.azure_openai_deployment or "azure",
            provider="azure",
            usage=usage,
        )
