"""Google Gemini provider implementation."""

from __future__ import annotations

from autodocs_ai.config import Settings
from autodocs_ai.providers.base import AIProvider, GenerationResult


class GeminiProvider(AIProvider):
    """Provider for Google Gemini's generate_content API."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = None

    def validate_config(self) -> None:
        if not self.settings.google_api_key:
            raise ValueError(
                "Google API key is required. Set GOOGLE_API_KEY environment variable."
            )

    def _get_client(self):
        if self._client is None:
            try:
                from google import genai
            except ImportError:
                raise ImportError(
                    "google-genai package is required. Install with: pip install autodocs-ai[gemini]"
                )
            self.validate_config()
            self._client = genai.Client(api_key=self.settings.google_api_key)
        return self._client

    async def generate(self, system_prompt: str, user_prompt: str) -> GenerationResult:
        client = self._get_client()
        combined_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = await client.aio.models.generate_content(
            model=self.settings.gemini_model,
            contents=combined_prompt,
        )
        content = response.text or ""
        usage = None
        if response.usage_metadata:
            usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count,
                "completion_tokens": response.usage_metadata.candidates_token_count,
                "total_tokens": response.usage_metadata.total_token_count,
            }
        return GenerationResult(
            content=content,
            model=self.settings.gemini_model,
            provider="gemini",
            usage=usage,
        )
