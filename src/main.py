# Directory structure:
#
# ai-hub/
# ├── src/
# │   ├── main.py
# │   ├── config.py
# │   ├── ui/
# │   │   ├── __init__.py
# │   │   ├── layout.py
# │   │   └── components.py
# │   ├── ai_clients/
# │   │   ├── __init__.py
# │   │   ├── base.py
# │   │   ├── gemini.py
# │   │   ├── chatgpt.py
# │   │   └── copilot.py
# │   ├── utils/
# │   │   ├── __init__.py
# │   │   ├── logger.py
# │   │   ├── errors.py
# │   │   ├── rate_limiter.py
# │   │   └── cache.py
# ├── tests/
# │   ├── test_ai_clients.py
# │   └── test_ui.py
# ├── requirements.txt
# ├── README.md
# └── pyproject.toml (optional)

# Let's proceed module by module. First, src/main.py:

# src/main.py
from flet import app, Page
from ui.layout import build_main_ui
from config import Config
import asyncio
import utils.logger


def main(page: Page) -> None:
    """Entry point for Flet app."""
    page.title = "AI Hub - Gemini, ChatGPT, Copilot"
    page.theme_mode = "light"
    page.window_resizable = True
    page.scroll = "auto"
    config = Config()
    page.session.set("config", config)

    # UI Layout
    build_main_ui(page)

if __name__ == "__main__":
    app(target=main)
