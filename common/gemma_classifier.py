from multi_agent_orchestrator.classifiers import Classifier, ClassifierResult
from common.gemma_agent import GemmaAgent
from typing import List, Optional, Dict
from multi_agent_orchestrator.types import ConversationMessage
from multi_agent_orchestrator.agents import Agent
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

class GemmaClassifier(Classifier):
    def __init__(self):
        super().__init__()
        self.gemma_agent = GemmaAgent()  # Uses Ollama under the hood
        self.agents: List[Agent] = []

    def set_agents(self, agents: List[Agent]):
        if isinstance(agents, dict):
            agents = list(agents.values())

        if not all(isinstance(agent, Agent) for agent in agents):
            raise TypeError(f"Expected a list of Agent objects, but got {type(agents)} with values: {agents}")

        self.agents = agents
        logger.info(f"✅ Agents set in GemmaClassifier: {self.agents}")
        for agent in self.agents:
            logger.debug(f"- {agent.name}: {agent.description}")

    def get_agents_descriptions(self) -> str:
        if not self.agents:
            return "No agents available."

        return "\n".join([
            f"- {agent.name}: {agent.description}"
            for agent in self.agents
        ])

    async def classify(self, user_input: str, chat_history: List[ConversationMessage]) -> ClassifierResult:
        prompt = f"""
        You are a classifier that routes user inputs to the most suitable agent.

        Match the user's request to the correct agent name based on the examples.

        Respond with ONLY the agent name (e.g., DarrylAgent or SchruteBot), no extra text or explanation.

        Examples:
        # Code/Dev Tasks → DarrylAgent
        - "write code to sort a list" → DarrylAgent
        - "generate code for a web scraper" → DarrylAgent
        - "debug this script" → DarrylAgent

        # Task Management → SchruteBot
        - "add a task to meet client" → SchruteBot
        - "complete proposal follow-up task" → SchruteBot

        # Pranks → JimsterAgent
        - "create a prank task for Dwight" → JimsterAgent

        # Research/Summary → OscarAgent
        - "summarize financial trends after 90 day tariff pause" → OscarAgent
        - "research Tesla's performance after SEC update" → OscarAgent
        - "get search insights on Microsoft layoffs" → OscarAgent
        - "summarize latest news on interest rates and banks" → OscarAgent

        Available agents and their descriptions:
        {self.get_agents_descriptions()}

        User input: "{user_input}"
        Which agent should handle this?
        """

        try:
            response = self.gemma_agent.generate_response(prompt).strip()
            logger.info(f"[GemmaClassifier] 🤖 Model raw response: '{response}'")
        except Exception as e:
            logger.error(f"[GemmaClassifier] ❌ Failed to get LLM response: {e}")
            return ClassifierResult(selected_agent=None, confidence=0.0)

        # Normalize response
        normalized = response.lower().replace(" ", "").replace(".", "")
        logger.info(f"[GemmaClassifier] Normalized response: '{normalized}'")

        for agent in self.agents:
            agent_key = agent.name.lower().replace(" ", "")
            logger.info(f"[GemmaClassifier] Comparing to agent: '{agent_key}'")
            if agent_key == normalized:
                logger.info(f"[GemmaClassifier] ✅ Matched agent: {agent.name}")
                return ClassifierResult(selected_agent=agent, confidence=1.0)

        logger.warning(f"[GemmaClassifier] ❌ No agent matched LLM response: '{response}'")
        return ClassifierResult(selected_agent=None, confidence=0.0)

    async def process_request(
        self,
        input_text: str,
        user_id: str,
        session_id: str,
        chat_history: List[ConversationMessage],
        additional_params: Optional[Dict[str, str]] = None
    ) -> ClassifierResult:
        return await self.classify(input_text, chat_history)
