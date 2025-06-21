# src/ai_clients/gemini.py
import httpx
import time
from .base import AIClient, AIResponse
from config import Config
from utils.logger import logger


class GeminiClient(AIClient):
    """Google Gemini API client wrapper."""

    def __init__(self) -> None:
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.config = Config()
        self.api_key = self.config.get_api_key("gemini")

    async def send_message(self, prompt: str, **params) -> AIResponse:
        if not self.api_key:
            return AIResponse(text="Gemini API key missing.", error="APIKeyMissing")

        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.base_url}?key={self.api_key}",
                    headers=headers,
                    json=payload
                )
                elapsed = int((time.time() - start) * 1000)
                if response.status_code == 200:
                    result = response.json()
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    return AIResponse(text=text, latency_ms=elapsed)
                else:
                    logger.warning(f"Gemini API error {response.status_code}: {response.text}")
                    return AIResponse(text="[Error] Gemini response failed.", error=str(response.status_code))
        except Exception as e:
            logger.error(f"Gemini exception: {e}")
            return AIResponse(text="[Exception] Gemini request failed.", error=str(e))
