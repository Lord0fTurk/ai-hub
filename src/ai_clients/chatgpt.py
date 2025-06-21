# src/ai_clients/chatgpt.py
import httpx
import time
from .base import AIClient, AIResponse
from config import Config
from utils.logger import logger


class ChatGPTClient(AIClient):
    """OpenAI ChatGPT API client wrapper."""

    def __init__(self) -> None:
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.config = Config()
        self.api_key = self.config.get_api_key("chatgpt")
        self.model = "gpt-4"

    async def send_message(self, prompt: str, **params) -> AIResponse:
        if not self.api_key:
            return AIResponse(text="ChatGPT API key missing.", error="APIKeyMissing")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": params.get("temperature", 0.7),
            "max_tokens": params.get("max_tokens", 1024),
        }

        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )
                elapsed = int((time.time() - start) * 1000)
                if response.status_code == 200:
                    result = response.json()
                    message = result["choices"][0]["message"]["content"]
                    tokens = result.get("usage", {}).get("total_tokens", 0)
                    return AIResponse(text=message, tokens_used=tokens, latency_ms=elapsed)
                else:
                    logger.warning(f"ChatGPT API error {response.status_code}: {response.text}")
                    return AIResponse(text="[Error] ChatGPT response failed.", error=str(response.status_code))
        except Exception as e:
            logger.error(f"ChatGPT exception: {e}")
            return AIResponse(text="[Exception] ChatGPT request failed.", error=str(e))
