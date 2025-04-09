import ollama
from multi_agent_orchestrator.agents import Agent, AgentOptions, AgentCallbacks
from multi_agent_orchestrator.types import ConversationMessage
from typing import List, Optional, Dict

from tools.due_diligence_tool import DueDiligenceTool

MODEL = "gemma3:1b"  # Default model

class OscarAgent(Agent):
    def __init__(self):
        """Initialize OscarAgent with a default model and research capability."""
        options = AgentOptions(
            name="OscarAgent",
            description=(
                "A precise and research-driven AI assistant modeled after Oscar from The Office."
                " Specializes in verifying facts, conducting deep research, and responding in a professional tone."
            ),
            save_chat=True,
            callbacks=AgentCallbacks(),
            LOG_AGENT_DEBUG_TRACE=False
        )
        super().__init__(options)
        self.model = MODEL
        self.research_tool = DueDiligenceTool()

    def handle_research_request(self, message: str) -> str:
        """
        Handles incoming research requests by passing the query to Oscar's research tool.
        The response is a professional, well-reasoned summary of findings.
        """
        if not message or not message.strip():
            return "I'm going to need a more specific query. I can't work with vague prompts."

        print("🔍 Oscar is conducting a detailed investigation...")
        summary = self.research_tool.deep_research(message.strip())
        return f"🗂️ **Oscar's Findings:**\n\n{summary}\n\n---\n\n*Powered by [crawl4ai](https://github.com/unclecode/crawl4ai)*"

# Optional test case
if __name__ == '__main__':
    oscar = OscarAgent()
    topic = "How LLMs impact enterprise productivity"
    print(oscar.handle_research_request(topic))
