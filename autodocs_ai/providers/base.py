"""Abstract base class for AI providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GenerationResult:
    """Result from an AI generation call."""

    content: str
    model: str
    provider: str
    usage: dict | None = None


class AIProvider(ABC):
    """Abstract base class that all AI providers must implement."""

    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> GenerationResult:
        """Generate text from a system prompt and user prompt.

        Args:
            system_prompt: The system-level instruction for the AI.
            user_prompt: The user's request/content.

        Returns:
            GenerationResult with the generated content.
        """

    @abstractmethod
    def validate_config(self) -> None:
        """Validate that the provider is properly configured.

        Raises:
            ValueError: If required configuration is missing.
        """
