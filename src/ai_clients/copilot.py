# src/ai_clients/copilot.py
import httpx
import time
from .base import AIClient, AIResponse
from config import Config
from utils.logger import logger


class CopilotClient(AIClient):
    """Microsoft Copilot (Azure OpenAI) API client wrapper."""

    def __init__(self) -> None:
        self.config = Config()
        self.api_key = self.config.get_api_key("copilot")
        self.endpoint = self.config._data.get(self.config.profile, {}).get("copilot_endpoint")
        self.deployment = self.config._data.get(self.config.profile, {}).get("copilot_deployment", "gpt-4")

    async def send_message(self, prompt: str, **params) -> AIResponse:
        if not self.api_key or not self.endpoint:
            return AIResponse(text="Copilot API key or endpoint missing.", error="APIKeyMissing")

        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version=2024-03-01-preview"

        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": params.get("temperature", 0.7),
            "max_tokens": params.get("max_tokens", 1024),
            "stream": False
        }

        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, headers=headers, json=payload)
                elapsed = int((time.time() - start) * 1000)
                if response.status_code == 200:
                    result = response.json()
                    message = result["choices"][0]["message"]["content"]
                    tokens = result.get("usage", {}).get("total_tokens", 0)
                    return AIResponse(text=message, tokens_used=tokens, latency_ms=elapsed)
                else:
                    logger.warning(f"Copilot API error {response.status_code}: {response.text}")
                    return AIResponse(text="[Error] Copilot response failed.", error=str(response.status_code))
        except Exception as e:
            logger.error(f"Copilot exception: {e}")
            return AIResponse(text="[Exception] Copilot request failed.", error=str(e))
