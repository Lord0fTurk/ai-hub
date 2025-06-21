from flet import (
    Page, Tabs, Tab, IconButton, Icons,
    AppBar, Container, Text
)
from ui.components import ChatView, SettingsDialog


def build_main_ui(page: Page) -> None:
    """Constructs the main layout of the app."""

    # Chat sekmeleri
    chat_tabs = Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            Tab(text="Gemini", content=ChatView(service="gemini", page=page)),
            Tab(text="ChatGPT", content=ChatView(service="chatgpt", page=page)),
            Tab(text="Copilot", content=ChatView(service="copilot", page=page)),
        ],
        expand=1,
    )

    settings_dialog = SettingsDialog(page)

    page.dialog = settings_dialog

    app_bar = AppBar(
        title=Text("AI Hub"),
        actions=[
            IconButton(
                icon=Icons.LIGHT_MODE,
                tooltip="Toggle Theme",
                on_click=lambda e: toggle_theme(page)
            ),
            IconButton(
                icon=Icons.SETTINGS,
                tooltip="Settings",
                on_click=lambda e: settings_dialog.open_dialog()
            ),
        ]
    )

    page.appbar = app_bar
    page.add(Container(content=chat_tabs, expand=True))


def toggle_theme(page: Page) -> None:
    """Toggles between light and dark theme modes."""
    page.theme_mode = "dark" if page.theme_mode == "light" else "light"
    page.update()
