# tests/test_ai_clients.py
import pytest
import asyncio
from ai_clients.gemini import GeminiClient
from ai_clients.chatgpt import ChatGPTClient
from ai_clients.copilot import CopilotClient

@pytest.mark.asyncio
async def test_gemini_send_message(monkeypatch):
    client = GeminiClient()
    monkeypatch.setattr(client, "api_key", "dummy_key")

    async def fake_send_message(prompt, **params):
        return client.send_message.__func__(client, prompt, **params)

    response = await client.send_message("Hello Gemini")
    assert response.text is not None

@pytest.mark.asyncio
async def test_chatgpt_send_message(monkeypatch):
    client = ChatGPTClient()
    monkeypatch.setattr(client, "api_key", "dummy_key")

    response = await client.send_message("Hello ChatGPT")
    assert response.text is not None

@pytest.mark.asyncio
async def test_copilot_send_message(monkeypatch):
    client = CopilotClient()
    monkeypatch.setattr(client, "api_key", "dummy_key")
    monkeypatch.setattr(client.config._data[client.config.profile], "copilot_endpoint", "https://dummy.endpoint")

    response = await client.send_message("Hello Copilot")
    assert response.text is not None
