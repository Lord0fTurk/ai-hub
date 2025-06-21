# test_dialog.py
from flet import Page, app, Text, AlertDialog, ElevatedButton, Column

def main(page: Page):
    page.title = "Dialog Test"

    dialog = AlertDialog(
        title=Text("Test Dialog"),
        content=Text("Bu bir test mesajıdır."),
        actions=[
            ElevatedButton(text="Kapat", on_click=lambda e: close_dialog())
        ]
    )

    def open_dialog(e):
        dialog.open = True
        page.update()

    def close_dialog(e=None):
        dialog.open = False
        page.update()

    open_button = ElevatedButton(text="Ayarları Aç", on_click=open_dialog)

    page.add(Column([open_button, dialog]))

app(target=main)
