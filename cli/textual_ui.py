import sys
import os

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label
from textual.reactive import reactive

# Ensure project root is in sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.pam_bot.agent_pam import PamBot  # Hook into real agent logic

class AgentList(Static):
    def compose(self) -> ComposeResult:
        yield Label("Agents", id="section-title")
        self.list_view = ListView()
        yield self.list_view

    def update_agents(self, agents):
        self.list_view.clear()
        for agent_name in agents:
            self.list_view.append(ListItem(Label(agent_name)))

class TaskPanel(Static):
    agent = reactive("SchruteBot")

    def update_tasks(self, message):
        response = self.app.pambot.route_request(message)
        self.update(response or "No response.")

class CommandBox(Input):
    def __init__(self):
        super().__init__(placeholder="Type a command (e.g. /add 'task')...")

class DunderAgentUI(App):
    CSS_PATH = "textual_ui.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("tab", "focus_next", "Next"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container():
            with Vertical(id="sidebar"):
                self.agent_list = AgentList()
                yield self.agent_list
            self.task_panel = TaskPanel()
            yield self.task_panel
        self.command_box = CommandBox()
        yield self.command_box
        yield Footer()

    def on_mount(self):
        self.pambot = PamBot()
        # Adjusted to handle list of strings instead of objects with .name
        agents = self.pambot.orchestrator.list_agents() if hasattr(self.pambot.orchestrator, 'list_agents') else []
        self.agent_list.update_agents(agents)
        self.agent_list.list_view.index = 0
        if agents:
            self.task_panel.agent = agents[0]
            self.task_panel.update_tasks(f"view tasks")

    def on_list_view_selected(self, event: ListView.Selected):
        selected_agent = str(event.item.label.renderable)
        self.task_panel.agent = selected_agent
        self.task_panel.update_tasks(f"view tasks")

    def on_input_submitted(self, event: Input.Submitted):
        command = event.value.strip()
        response = self.pambot.route_request(command)
        self.task_panel.update(response)
        self.command_box.value = ""

if __name__ == "__main__":
    app = DunderAgentUI()
    app.run()
