from textual.widgets import Input

class CommandBox(Input):
    def __init__(self, **kwargs):
        super().__init__(placeholder="Type a message...", **kwargs)