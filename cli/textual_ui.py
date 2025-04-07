import sys
import os
import asyncio
import logging

# Silence logs before any other imports
logging.basicConfig(level=logging.CRITICAL)

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Input, Static, ListView, ListItem, Label
from textual.reactive import reactive
from rich.text import Text

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
        for agent_name in ["pambot"] + agents:  # Ensure PamBot is listed first
            list_item = ListItem(Label(agent_name))
            list_item.data = agent_name  # Store agent name in data attribute
            self.list_view.append(list_item)

class TaskPanel(Static):
    agent = reactive("pambot")

    async def update_tasks(self, message):
        response = await self.app.pambot.route_requests(message, user_id="ui_user", session_id="ui_session")
        print("[UI] Response from PamBot:", response)  # Debug print
        output = getattr(response, "output", "No response.")
        self.update(Text.from_markup(output))

class CommandBox(Input):
    def __init__(self):
        super().__init__(placeholder="💬 Type a command (e.g. 'view tasks') and press Enter")
        self.can_focus = True
        self.focus()
        self.styles.height = 3
        self.styles.border = ("round", "blue")
        self.styles.margin = (0, 1)
        self.styles.padding = (0, 1)

class DunderAgentUI(App):

    async def on_ready(self):
        self.set_focus(self.command_box)
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

    async def on_mount(self):
        self.pambot = PamBot()
        if hasattr(self.pambot.orchestrator, 'list_agents'):
            agents = self.pambot.orchestrator.list_agents()
        else:
            agents = [a if isinstance(a, str) else getattr(a, 'name', str(a)) for a in self.pambot.orchestrator.agents]

        print("[UI] Agents loaded:", agents)
        self.agent_list.update_agents(agents or ["TestBot", "FakeAgent"])
        self.agent_list.list_view.index = 0
        self.task_panel.agent = "pambot"
        self.task_panel.update(Text.from_markup("👋 Welcome! Select an agent or enter a command below."))
        self.call_after_refresh(lambda: self.set_focus(self.command_box))

    async def on_list_view_selected(self, event: ListView.Selected):
        selected_agent = str(event.item.data)
        self.task_panel.agent = selected_agent
        self.task_panel.update(Text.from_markup(f"🔹 Selected agent: {selected_agent}"))

    async def on_input_submitted(self, event: Input.Submitted):
        command = event.value.strip()
        print("[UI] Command submitted:", command)
        response = await self.pambot.route_requests(command, user_id="ui_user", session_id="ui_session")
        output = getattr(response, "output", "No response.")
        self.task_panel.update(Text.from_markup(output))
        self.command_box.value = ""

if __name__ == "__main__":
    app = DunderAgentUI()
    app.run()