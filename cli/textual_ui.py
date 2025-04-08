import sys
import os
import asyncio
import logging
import re

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Input, ListView, ListItem, Label, RichLog, TextArea, LoadingIndicator, Button
from textual.reactive import reactive
from rich.text import Text

# --- Project Path Setup ---
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from cli.widgets.agent_panel import AgentPanel
from cli.widgets.code_response_box import CodeResponseBox
from cli.widgets.interaction_log import InteractionLog
from cli.widgets.command_box import CommandBox
from textual.containers import Horizontal

from agents.pam_bot.agent_pam import PamBot

class DunderAgentUI(App):
    CSS_PATH = "textual_ui.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("ctrl+l", "clear_log", "Clear Log"),
        ("tab", "toggle_sidebar", "Toggle Agent Panel"),
    ]

    def __init__(self):
        super().__init__()
        self.pambot = PamBot()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main-container"):
            self.agent_panel = AgentPanel()
            yield self.agent_panel
            self.interaction_log = InteractionLog(id="interaction-log")
            yield self.interaction_log
        self.command_box = CommandBox(id="command-box")
        yield self.command_box
        yield Footer()

    async def on_mount(self) -> None:
        import logging
        logging.basicConfig(level=logging.DEBUG)
        agents = []
        try:
            orchestrator = getattr(self.pambot, 'orchestrator', None)
            if orchestrator:
                if callable(getattr(orchestrator, 'list_agents', None)):
                    agents = orchestrator.list_agents()
                elif hasattr(orchestrator, 'agents'):
                    agents = [a if isinstance(a, str) else getattr(a, 'name', str(a)) for a in orchestrator.agents]
                else:
                    agents = ["UnknownAgent"]
            else:
                agents = ["NoOrchestrator"]
            if not isinstance(agents, list):
                agents = ["FallbackAgent"]
        except Exception as e:
            self.log.error(f"Error getting agent list: {e}")
            agents = ["ErrorAgent"]

        self.agent_panel.update_agents(agents)
        self.set_focus(self.command_box)
        self.interaction_log.write(Text("Welcome to the Dunder Mifflin Agent Interface!", style="bold green"))
        self.interaction_log.write("Type your requests for Pam below.")

    def detect_code(self, text: str) -> tuple[str, tuple[str, str] | None]:
        match = re.search(r"```(\w+)?\n(.*?)```", text, re.DOTALL)
        if match:
            lang = match.group(1) or "text"
            code = match.group(2).strip()
            cleaned = re.sub(r"```.*?```", "", text, flags=re.DOTALL).strip()
            return cleaned, (lang, code)
        if any(kw in text for kw in ["def ", "class ", "{", "}", ";", "import ", "from ", "return"]):
            return "", ("python", text.strip())
        return text, None

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        command = event.value.strip()
        if not command:
            return

        self.interaction_log.write(Text(f"You: {command}", style="bold #cccccc"))
        self.command_box.value = ""
        self.command_box.disabled = True

        self.loading = LoadingIndicator()
        await self.mount(self.loading, after=self.command_box)

        try:
            response = await self.pambot.route_requests(
                message=command,
                user_id="tui_user",
                session_id="tui_session_0"
            )
            selected_agent = getattr(response, "agent", None)
            if selected_agent:
                agent_colors = {
                    "DarrylAgent": "bold cyan",
                    "SchruteBot": "bold green",
                    "PamBot": "bold magenta"
                }
                agent_style = agent_colors.get(selected_agent, "bold yellow")
                self.interaction_log.write(Text(f"🧠 Pam routed this to: {selected_agent}", style=agent_style))
            output = getattr(response, "output", "*No response text found.*")

            if output.startswith("INFO:"):
                output = re.sub(r"INFO:.*", "", output)

            cleaned, code_block = self.detect_code(str(output))

            if code_block:
                lang, code = code_block
                self.interaction_log.write(Text("🤖 Pam wrote some code:", style="bold magenta"))
                textarea = TextArea(code, language=lang, read_only=True, id="code-output", classes=f"language-{lang}")
                textarea.styles.height = 12
                await self.mount(textarea, after=self.interaction_log)
            else:
                self.interaction_log.write(Text.from_ansi(str(output)))

        except Exception as e:
            self.log.error(f"Error during agent request: {e}")
            self.interaction_log.write(Text(f"Error processing command: {e}", style="bold red"))

        finally:
            await self.loading.remove()
            self.command_box.disabled = False
            self.command_box.placeholder = "Type a message..."
            self.set_focus(self.command_box)

    def action_quit(self) -> None:
        self.exit()

    def action_clear_log(self) -> None:
        self.interaction_log.clear()
        self.interaction_log.write(Text("Log cleared.", style="italic"))
        self.set_focus(self.command_box)

    def action_toggle_sidebar(self) -> None:
        self.agent_panel.styles.display = "block" if self.agent_panel.styles.display == "none" else "none"

if __name__ == "__main__":
    app = DunderAgentUI()
    app.run()
