from textual.containers import Vertical
from textual.widgets import Label, ListView, ListItem
from textual.app import ComposeResult

class AgentPanel(Vertical):
    def __init__(self):
        super().__init__()
        self.id = "sidebar"

    def compose(self) -> ComposeResult:
        yield Label("Agents", id="section-title")
        self.list_view = ListView(id="agent-list-view")
        yield self.list_view

    def update_agents(self, agents: list[str]):
        self.list_view.clear()
        all_agents = ["pambot"] + [a for a in agents if a != "pambot"]
        for name in all_agents:
            item = ListItem(Label(name))
            item.data = name
            self.list_view.append(item)