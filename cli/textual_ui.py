import sys
import os
import asyncio
import logging

# Configure logging (optional: adjust level or add file output)
logging.basicConfig(level=logging.CRITICAL)

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Input, ListView, ListItem, Label, RichLog, TextArea
from textual.reactive import reactive
from rich.text import Text

# --- Project Path Setup ---
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Agent Import ---
try:
    from agents.pam_bot.agent_pam import PamBot
except ImportError as e:
    print("Fatal Error: Could not import PamBot from agents.pam_bot.agent_pam.", file=sys.stderr)
    print(f"Reason: {e}", file=sys.stderr)
    sys.exit(1)

# --- Custom Widgets ---

class AgentList(Container):
    def compose(self) -> ComposeResult:
        yield Label("Agents", id="section-title")
        self.list_view = ListView(id="agent-list-view")
        yield self.list_view

    def on_mount(self) -> None:
        pass

    def update_agents(self, agents: list[str]):
        self.list_view.clear()
        all_display_agents = ["pambot"] + [a for a in agents if a != "pambot"]
        for agent_name in all_display_agents:
            list_item = ListItem(Label(agent_name))
            list_item.data = agent_name
            self.list_view.append(list_item)

class InteractionLog(RichLog):
    def __init__(self, **kwargs):
        super().__init__(highlight=False, markup=True, wrap=True, **kwargs)
        self.border_title = "Conversation Log"

class CommandBox(Input):
    def __init__(self, **kwargs):
        super().__init__(placeholder="💬 Type your message to Pam and press Enter...", **kwargs)

# --- Main App ---

class DunderAgentUI(App):
    CSS_PATH = "textual_ui.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+l", "clear_log", "Clear Log"),
    ]

    selected_agent = reactive("pambot")

    def __init__(self):
        super().__init__()
        self.pambot = PamBot()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main-container"):
            with Vertical(id="sidebar"):
                self.agent_list = AgentList()
                yield self.agent_list
            self.interaction_log = InteractionLog(id="interaction-log")
            yield self.interaction_log
        self.command_box = CommandBox(id="command-box")
        yield self.command_box
        yield Footer()

    def detect_code(self, text: str) -> tuple[str, tuple[str, str] | None]:
        """Detects and extracts code blocks or infers them from structure."""
        import re
        match = re.search(r"```(\w+)?\n(.*?)```", text, re.DOTALL)
        if match:
            lang = match.group(1) or "text"
            code = match.group(2).strip()
            cleaned = re.sub(r"```.*?```", "", text, flags=re.DOTALL).strip()
            return cleaned, (lang, code)
        if any(kw in text for kw in ["def ", "class ", "{", "}", ";", "import ", "from ", "return "]):
            return "", ("python", text.strip())
        return text, None

    async def on_mount(self) -> None:
        agents = []
        try:
            if hasattr(self.pambot, 'orchestrator'):
                orchestrator = self.pambot.orchestrator
                if hasattr(orchestrator, 'list_agents') and callable(orchestrator.list_agents):
                    agents = orchestrator.list_agents()
                elif hasattr(orchestrator, 'agents'):
                    agents = [
                        a if isinstance(a, str) else getattr(a, 'name', str(a))
                        for a in orchestrator.agents
                    ]
                else:
                    self.log.warning("Orchestrator found, but has no 'list_agents' method or 'agents' attribute.")
                    agents = ["UnknownAgent"]
            else:
                self.log.warning("PamBot instance has no 'orchestrator' attribute.")
                agents = ["NoOrchestrator"]

            if not isinstance(agents, list):
                self.log.warning(f"Agent list retrieved was not a list ({type(agents)}), using fallback.")
                agents = ["FallbackAgent"]

        except Exception as e:
            self.log.error(f"Error getting agent list from orchestrator: {e}")
            agents = ["ErrorAgent"]

        self.agent_list.update_agents(agents)
        self.set_focus(self.command_box)
        self.interaction_log.write(Text("👋 Welcome to the Dunder Mifflin Agent Interface!", style="bold green"))
        self.interaction_log.write("Type your requests for Pam in the box below.")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        agent_name = str(event.item.data)
        self.selected_agent = agent_name
        self.log.info(f"Agent selected in list: {agent_name}")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        if not command:
            return

        self.interaction_log.write(Text(f"👤 You: {command}", style="bold blue"))
        self.command_box.disabled = True
        self.command_box.placeholder = "⏳ Pam is processing..."

        try:
            response = await self.pambot.route_requests(
                message=command,
                user_id="tui_user",
                session_id="tui_session_0"
            )
            output = getattr(response, "output", "*No response text found.*")
            cleaned, code_block = self.detect_code(str(output))

            if code_block:
                lang, code = code_block
                self.interaction_log.write(Text("🤖 Pam wrote some code:", style="bold magenta"))
                textarea = TextArea(code, language=lang, read_only=True, id="code-output")
                textarea.styles.height = 12
                await self.mount(textarea, after=self.interaction_log)
            else:
                self.interaction_log.write(Text(f"🤖 Pam: {cleaned}", style="bold magenta"))

        except Exception as e:
            self.log.error(f"Error during agent request: {e}")
            self.interaction_log.write(Text(f"❌ Error processing command: {e}", style="bold red"))

        finally:
            self.command_box.value = ""
            self.command_box.disabled = False
            self.command_box.placeholder = "💬 Type your message to Pam and press Enter..."
            self.set_focus(self.command_box)

    def action_quit(self) -> None:
        self.exit()

    def action_clear_log(self) -> None:
        self.interaction_log.clear()
        self.interaction_log.write(Text("🧹 Log cleared.", style="italic"))
        self.set_focus(self.command_box)

if __name__ == "__main__":
    app = DunderAgentUI()
    app.run()
