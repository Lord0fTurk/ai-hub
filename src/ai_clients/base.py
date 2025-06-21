# src/ai_clients/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class AIResponse:
    """Dataclass for normalized AI response."""
    text: str
    tokens_used: Optional[int] = None
    latency_ms: Optional[int] = None
    error: Optional[str] = None


class AIClient(ABC):
    """Abstract base class for AI clients."""

    @abstractmethod
    async def send_message(self, prompt: str, **params) -> AIResponse:
        """Send prompt and return normalized AI response."""
        pass
