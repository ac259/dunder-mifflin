import sys
import os
import asyncio
import ollama
from typing import List, Optional, Dict
from multi_agent_orchestrator.agents import Agent, AgentOptions, AgentCallbacks
from multi_agent_orchestrator.types import ConversationMessage

# Ensure root path is added for module resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from tools.due_diligence_tool import DueDiligenceTool

MODEL = "gemma3:1b"

class OscarAgent(Agent):
    def __init__(self):
        options = AgentOptions(
            name="OscarAgent",
            description=(
                "A precise AI assistant modeled after Oscar Martinez. Capabilities include summarizing search results, "
                "and deep crawling URLs to extract structured insights."
            ),
            save_chat=True,
            callbacks=AgentCallbacks(),
            LOG_AGENT_DEBUG_TRACE=False
        )
        super().__init__(options)
        self.model = MODEL
        self.research_tool = DueDiligenceTool()

    async def handle_search_request(self, query: str) -> str:
        return await self.research_tool.search(query) #"Search functionality is currently unavailable. Please use summarization or deep crawl features."

    async def handle_summarize_request(self, query: str) -> str:
        if not query or not query.strip():
            return "A specific query is required for summarized research."
        return await self.research_tool.summarize_search_results(query.strip())

    async def handle_deep_crawl_request(self, url: str) -> str:
        if not url or not url.strip().startswith(('http://', 'https://')):
            return "Please provide a valid URL (starting with http:// or https://) for the deep crawl."
        return await self.research_tool.deep_crawl_url(url.strip())

    async def process_request(
        self,
        input_text: str,
        user_id: str,
        session_id: str,
        chat_history: List[ConversationMessage],
        additional_params: Optional[Dict[str, str]] = None
    ) -> str:
        message = input_text.strip()

        if message.lower().startswith("set model"):
            model_name = message.replace("set model", "").strip()
            try:
                self.model = model_name
                return f"✅ OscarAgent now using model: {self.model}"
            except ValueError as e:
                return str(e)

        # Default behavior: summarize the query
        return await self.handle_summarize_request(message)


# Optional test runner
async def run_tests():
    agent = OscarAgent()
    print("\n🔍 SEARCH TEST:")
    print(await agent.handle_search_request("White Lotus"))

    print("\n📄 SUMMARY TEST:")
    print(await agent.handle_summarize_request("future of renewable energy"))

    # print("\n🕸️ DEEP CRAWL TEST:")
    # print(await agent.handle_deep_crawl_request("https://www.nrel.gov"))

if __name__ == '__main__':
    asyncio.run(run_tests())
