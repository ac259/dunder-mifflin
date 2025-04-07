#!/usr/bin/env python3
import os
import sys
import time
import readline
import random
import logging
import textwrap
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from cli.agent_connector import AgentConnector

logging.getLogger().setLevel(logging.CRITICAL)

# === Terminal Colors ===
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

AGENT_COLORS = {
    "SchruteBot": Colors.YELLOW,
    "JimsterAgent": Colors.BLUE,
    "DarrylAgent": Colors.GREEN,
}

TYPING_CHARS = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]

class DunderMifflinCLI:
    def __init__(self):
        self.connector = AgentConnector()
        self.current_agent = "pam"
        self.session_id = f"session_{int(time.time())}"
        self.history = []

    def print_logo(self):
        logo = f"""
        {Colors.BLUE}
        ╔═════════════════════════════════════════════════════════════════════╗
        ║                                                                     ║
        ║  ██████╗ ██╗   ██╗███╗   ██╗██████╗ ███████╗██████╗                 ║
        ║  ██╔══██╗██║   ██║████╗  ██║██╔══██╗██╔════╝██╔══██╗                ║
        ║  ██║  ██║██║   ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝                ║
        ║  ██║  ██║██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗                ║
        ║  ██████╔╝╚██████╔╝██║ ╚████║██████╔╝███████╗██║  ██║                ║
        ║  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝                ║
        ║                                                                     ║
        ║  ███╗   ███╗██╗███████╗███████╗██╗     ██╗███╗   ██╗                ║
        ║  ████╗ ████║██║██╔════╝██╔════╝██║     ██║████╗  ██║                ║
        ║  ██╔████╔██║██║█████╗  █████╗  ██║     ██║██╔██╗ ██║                ║
        ║  ██║╚██╔╝██║██║██╔══╝  ██╔══╝  ██║     ██║██║╚██╗██║                ║
        ║  ██║ ╚═╝ ██║██║██║     ██║     ███████╗██║██║ ╚████║                ║
        ║  ╚═╝     ╚═╝╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝╚═╝  ╚═══╝                ║
        ║                                                                     ║
        ║  {Colors.BOLD}DUNDER MIFFLIN TERMINAL{Colors.ENDC}{Colors.BLUE}                            ║
        ║  {Colors.ENDC}Unlimited paper in a paperless world                           {Colors.BLUE}║
        ╚═════════════════════════════════════════════════════════════════════╝
        {Colors.ENDC}
        """
        print(logo)

    def typing_animation(self, agent="Agent"):
        color = AGENT_COLORS.get(agent, Colors.ENDC)
        for _ in range(15):
            sys.stdout.write(f"\r{color}{agent} is thinking {random.choice(TYPING_CHARS)}{Colors.ENDC}")
            sys.stdout.flush()
            time.sleep(0.05)
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()

    def format_response(self, text):
        """Format agent response for terminal display."""
        text = text.encode().decode("unicode_escape")

        if "```" in text:
            parts = re.split(r"```(?:\w+)?", text)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    # Format non-code text
                    for line in part.strip().split("\n"):
                        # Highlight bold
                        line = re.sub(r"\*\*(.*?)\*\*", f"{Colors.BOLD}\\1{Colors.ENDC}", line)
                        print(textwrap.fill(line, width=80))
                    print()
                else:
                    print(f"{Colors.CYAN}```python{Colors.ENDC}")
                    print(f"{Colors.GREEN}{part.strip()}{Colors.ENDC}")
                    print(f"{Colors.CYAN}```{Colors.ENDC}\n")
        else:
            for line in text.strip().split("\n"):
                line = re.sub(r"\*\*(.*?)\*\*", f"{Colors.BOLD}\\1{Colors.ENDC}", line)
                print(textwrap.fill(line, width=80))


    def run(self):
        self.print_logo()
        print(f"{Colors.GREEN}Type '/agents' to list characters, '/use [agent]', or just ask something...{Colors.ENDC}\n")

        while True:
            try:
                prompt = f"{Colors.BOLD}[{self.current_agent.upper()}]{Colors.ENDC} > "
                query = input(prompt).strip()

                if not query:
                    continue

                if query.startswith("/"):
                    if query == "/exit":
                        print(f"{Colors.YELLOW}Goodbye! Remember: identity theft is not a joke.{Colors.ENDC}")
                        break
                    elif query == "/agents":
                        print(f"{Colors.BOLD}Available agents:{Colors.ENDC}")
                        for aid, color in AGENT_COLORS.items():
                            print(f"  {color}{aid}{Colors.ENDC}")
                        continue
                    elif query.startswith("/use "):
                        new_agent = query.split("/use ")[1].lower()
                        if new_agent in ["schrute", "jim", "darryl"]:
                            self.current_agent = new_agent
                            print(f"👔 Switched to: {new_agent.capitalize()}")
                        else:
                            print(f"{Colors.RED}Unknown agent: {new_agent}{Colors.ENDC}")
                        continue
                    elif query == "/history":
                        for entry in self.history:
                            print(f"\n📝 You: {entry['query']}")
                            print(f"🤖 {entry['agent']}:")
                            self.format_response(entry['response'])
                        continue
                    else:
                        print(f"{Colors.RED}Unknown command.{Colors.ENDC}")
                        continue

                self.typing_animation(self.current_agent)

                success, response = self.connector.call_agent(self.current_agent, query)
                if not success:
                    print(f"{Colors.RED}Error: {response}{Colors.ENDC}")
                else:
                    output = getattr(response, "output", response)
                    self.history.append({
                        "agent": self.current_agent.capitalize(),
                        "query": query,
                        "response": output
                    })
                    print(f"\n{AGENT_COLORS.get(self.current_agent.capitalize(), Colors.ENDC)}")
                    self.format_response(output)
                    print(Colors.ENDC + "\n" + "─" * 80)

            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Interrupted. Use /exit to quit.{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")

def main():
    cli = DunderMifflinCLI()
    cli.run()

if __name__ == "__main__":
    main()
