from textual.containers import Vertical, Horizontal
from textual.widgets import TextArea, Button
from textual.app import ComposeResult
import pyperclip


class CodeResponseBox(Vertical):
    def __init__(self, code: str, language: str = "python"):
        super().__init__()
        self.code = code
        self.language = language

    def compose(self) -> ComposeResult:
        self.text_area = TextArea(
            self.code,
            language=self.language,
            read_only=True,
            id="code-output",
            classes=f"language-{self.language}"
        )
        self.text_area.styles.height = 12
        yield self.text_area

        with Horizontal(id="code-controls"):
            yield Button("Copy", id="copy-button")
            yield Button("Edit", id="edit-button")

    def on_mount(self) -> None:
        self.app.log.info(f"CodeResponseBox mounted with language: {self.language}")
        self.app.log.info(f"TextArea styles: {self.text_area.styles}")
        self.app.log.info(f"TextArea classes: {self.text_area.classes}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "copy-button":
            try:
                pyperclip.copy(self.text_area.value)
                self.app.bell()
                self.app.log.info("✅ Code copied to clipboard.")
            except Exception as e:
                self.app.log.error(f"Clipboard error: {e}")

        elif event.button.id == "edit-button":
            self.text_area.read_only = False
            self.text_area.focus()