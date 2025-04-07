from textual.widgets import RichLog

class InteractionLog(RichLog):
    def __init__(self, **kwargs):
        super().__init__(highlight=False, markup=True, wrap=True, **kwargs)
        self.border_title = "Conversation Log"
