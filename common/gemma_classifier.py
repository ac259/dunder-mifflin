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
        logger.debug(f"✅ Agents set in GemmaClassifier: {self.agents}")
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
        You are a classifier that assigns user inputs to the most suitable agent based on their expertise.

        Here are example mappings:
        - "write code to sort a list" → DarrylAgent
        - "give me python code for binary search" → DarrylAgent
        - "how do I write a REST API in FastAPI?" → DarrylAgent
        - "debug this script" → DarrylAgent
        - "generate code" → DarrylAgent
        - "assign a task to Jim" → SchruteBot
        - "view my task list" → SchruteBot
        - "mark the client proposal as complete" → SchruteBot
        - "daily report" → SchruteBot
        - "give me a dwight quote" → SchruteBot
        - "who won the NBA finals?" → Use a general factual agent if available

        Available agents and their descriptions:
        {self.get_agents_descriptions()}

        User input: "{user_input}"

        Which agent is best suited to handle this input? Provide only the agent's name.
        """
        response = self.gemma_agent.generate_response(prompt).strip()

        for agent in self.agents:
            if agent.name.lower() == response.lower():
                return ClassifierResult(selected_agent=agent, confidence=1.0)

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
