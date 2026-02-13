"""Ollama provider implementation for local models."""

from __future__ import annotations

from autodocs_ai.config import Settings
from autodocs_ai.providers.base import AIProvider, GenerationResult


class OllamaProvider(AIProvider):
    """Provider for Ollama local models."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = None

    def validate_config(self) -> None:
        # Ollama doesn't need API keys, just a running server
        pass

    def _get_client(self):
        if self._client is None:
            try:
                from ollama import AsyncClient
            except ImportError:
                raise ImportError(
                    "ollama package is required. Install with: pip install autodocs-ai[ollama]"
                )
            self._client = AsyncClient(host=self.settings.ollama_host)
        return self._client

    async def generate(self, system_prompt: str, user_prompt: str) -> GenerationResult:
        client = self._get_client()
        response = await client.chat(
            model=self.settings.ollama_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.get("message", {}).get("content", "")
        usage = None
        if "eval_count" in response:
            usage = {
                "eval_count": response.get("eval_count"),
                "prompt_eval_count": response.get("prompt_eval_count"),
            }
        return GenerationResult(
            content=content,
            model=self.settings.ollama_model,
            provider="ollama",
            usage=usage,
        )
