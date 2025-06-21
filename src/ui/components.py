from typing import Optional
from flet import (
    Column, Row, Text, TextField, ElevatedButton,
    ScrollMode, Divider, Icons, IconButton, Markdown, SnackBar, Container, AlertDialog, Page
)
import pyperclip

class ChatBubble(Container):
    def __init__(self, message: str, sender: str, page: Optional[Page] = None):
        """
        sender: "user" veya "ai"
        page: Flet Page objesi, clipboard ve snackbar için gereklidir
        """
        super().__init__()
        self.message = message
        self.sender = sender
        self.page = page

        is_user = sender == "user"
        alignment = "right" if is_user else "left"
        bg_color = "#DCF8C6" if is_user else "#E6E6E6"

        self.content = Row(
            alignment=alignment,
            controls=[
                Container(
                    content=Markdown(self.message, selectable=True),
                    bgcolor=bg_color,
                    padding=10,
                    border_radius=10,
                    width=400,
                    expand=False,
                ),
                IconButton(
                    icon=Icons.CONTENT_COPY,
                    tooltip="Copy",
                    on_click=self.copy_to_clipboard,
                ),
            ]
        )

        self.controls = [self.content]

    def copy_to_clipboard(self, e):
        try:
            pyperclip.copy(self.message)
            if self.page:
                self.page.snack_bar = SnackBar(Text("Copied to clipboard!"))
                self.page.snack_bar.open = True
                self.page.update()
        except Exception as err:
            if self.page:
                self.page.snack_bar = SnackBar(Text(f"Copy failed: {err}"))
                self.page.snack_bar.open = True
                self.page.update()


class ChatView(Column):
    def __init__(self, service: str, page: Page):
        """
        service: "gemini", "chatgpt" veya "copilot"
        page: Flet Page objesi
        """
        super().__init__(spacing=5, expand=True)
        self.page = page
        self.service = service
        self.chat_history = Column(scroll=ScrollMode.AUTO, expand=True)
        self.input_box = TextField(
            multiline=True,
            min_lines=2,
            max_lines=5,
            hint_text=f"Prompt for {service.capitalize()}...",
            expand=True
        )
        self.send_button = ElevatedButton(text="Send", on_click=self.send_prompt)
        self.status_bar = Row([
            Text(f"Service: {service}"),
            Divider(),
            Text("Tokens: 0"),
            Text(" | Latency: 0ms"),
        ])

        self.controls = [
            self.chat_history,
            Divider(),
            Row([self.input_box, self.send_button]),
            self.status_bar,
        ]

    def send_prompt(self, e):
        prompt = self.input_box.value.strip()
        if not prompt:
            return
        user_bubble = ChatBubble(message=prompt, sender="user", page=self.page)
        self.chat_history.controls.append(user_bubble)

        ai_bubble = ChatBubble(message="(response coming...)", sender="ai", page=self.page)
        self.chat_history.controls.append(ai_bubble)

        self.input_box.value = ""
        self.update()


class SettingsDialog:
    def __init__(self, page: Page):
        self.page = page

        self.api_key_gemini = TextField(label="Gemini API Key", password=True)
        self.api_key_chatgpt = TextField(label="ChatGPT API Key", password=True)
        self.api_key_copilot = TextField(label="Copilot API Key", password=True)

        self.dialog = AlertDialog(
            title=Text("Settings"),
            content=Column([
                self.api_key_gemini,
                self.api_key_chatgpt,
                self.api_key_copilot,
                Divider(),
                Text("Proxy, token limits and other settings will be added here."),
            ]),
            actions=[
                ElevatedButton(text="Save", on_click=self.save),
                ElevatedButton(text="Cancel", on_click=self.close),
            ],
        )

        self.page.overlay.append(self.dialog)

    def open_dialog(self):
        self.dialog.open = True
        self.page.update()

    def close(self, e=None):
        self.dialog.open = False
        self.page.update()

    def save(self, e):
        # TODO: Save API keys and settings logic
        self.close()
