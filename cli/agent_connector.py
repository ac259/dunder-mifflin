import sys
import os
from typing import Tuple

# Make sure we can import PamBot
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.pam_bot.agent_pam import PamBot

class AgentConnector:
    def __init__(self):
        self.pam = PamBot(log_verbose=False)
        self.user_id = "ani"
        self.session_id = f"session_{os.getpid()}"

    def call_agent(self, agent_id: str, query: str) -> Tuple[bool, str]:
        """
        Routes a user query to PamBot, which dispatches it to the appropriate agent.

        Args:
            agent_id (str): Currently unused, can be passed as context.
            query (str): The user's input text.

        Returns:
            Tuple of (success, response_text)
        """
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.pam.route_requests(query, self.user_id, self.session_id)
            )
            return True, result
        except Exception as e:
            return False, f"Error routing request: {e}"
