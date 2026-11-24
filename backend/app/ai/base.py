from abc import ABC, abstractmethod
from typing import Optional

class AIProvider(ABC):
    """
    Modular abstraction for AI operations.
    The core research engine operates independently of whether
    an AI provider is configured or available.
    """

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the AI backend is currently reachable and responding."""
        pass

    @abstractmethod
    async def generate_text(self, prompt: str, system_prompt: Optional[str] = None, max_tokens: int = 500) -> str:
        """Generate response text from a prompt."""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return provider name (e.g. 'Ollama (Local)', 'OpenAI', 'Gemini', 'Disabled')."""
        pass
