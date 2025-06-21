# tests/test_ui.py
import pytest
from flet import Page
from ui.components import ChatView, SettingsDialog

def test_chatview_initial_state():
    chat_view = ChatView(service="chatgpt")
    assert chat_view.service == "chatgpt"
    assert chat_view.input_box.value == ""
    assert len(chat_view.controls) >= 4  # chat_history, divider, row, status_bar

def test_settings_dialog_visibility():
    page = Page()
    settings = SettingsDialog(page=page)
    assert settings.visible is False
    settings.open_dialog()
    assert settings.visible is True
    settings.close_dialog()
    assert settings.visible is False
