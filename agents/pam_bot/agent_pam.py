import sys
import os
import asyncio
import logging
from multi_agent_orchestrator.orchestrator import MultiAgentOrchestrator, OrchestratorConfig
from multi_agent_orchestrator.agents import Agent

# Add project root to sys.path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from common.mistral_agent import MistralAgent
from agents.jimster.big_tuna import JimsterAgent
from agents.schrute_bot.schrute_bot import SchruteBot
from agents.darryl_coding_agent.darryls_tech_warehouse import DarrylBot
from common.mistral_classifier import MistralClassifier

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)  # You can set this dynamically later

# Optional: only if not already configured elsewhere
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

class PamBot:
    def __init__(self, log_verbose: bool = True):
        # Initialize Mistral LLM
        self.mistral = MistralAgent()
        self.schrute_bot = SchruteBot()
        self.jimster_agent = JimsterAgent()
        self.darryl_agent = DarrylBot()
        self.classifier = MistralClassifier()
        

        self.DEFAULT_CONFIG = OrchestratorConfig(
            LOG_AGENT_CHAT=log_verbose,
            LOG_CLASSIFIER_CHAT=log_verbose,
            LOG_CLASSIFIER_RAW_OUTPUT=False,
            LOG_CLASSIFIER_OUTPUT=log_verbose,
            LOG_EXECUTION_TIMES=log_verbose,
            MAX_RETRIES=3,
            MAX_MESSAGE_PAIRS_PER_AGENT=50,
            USE_DEFAULT_AGENT_IF_NONE_IDENTIFIED=True,
            CLASSIFICATION_ERROR_MESSAGE="Oops! We couldn't process your request. Please try again.",
            NO_SELECTED_AGENT_MESSAGE="I'm sorry, I couldn't determine how to handle your request. Could you please rephrase it?",
            GENERAL_ROUTING_ERROR_MSG_MESSAGE="An error occurred while processing your request. Please try again later."
        )

        self.orchestrator = MultiAgentOrchestrator(options=self.DEFAULT_CONFIG, classifier=self.classifier)
        self.register_agents()

    # Register agents    
    def register_agents(self):
        """Registers all available agents."""
        agents = [self.schrute_bot, 
                  self.jimster_agent,
                  self.darryl_agent
                  ]
        for agent in agents:
            logger.debug(f"Type: {type(agent)}, Value: {agent}")
        # Pass agents list to the classifier before adding them
        self.classifier.set_agents(agents)
        
        for agent in agents:
            self.orchestrator.add_agent(agent)
            logger.debug(f"✅ Registered agent: {agent.name}")

    async def route_requests(self, message: str, user_id: str, session_id: str):
        """Routes the user message to the appropriate agent."""
        # Call the orchestrator's route_request method
        response = await self.orchestrator.route_request(
            user_input=message,
            user_id=user_id,
            session_id=session_id
        )
        return response

# Example usage
# if __name__ == "__main__":
    # pam = PamBot()
    # user_input = "Generate code in python to create an agent that can integrate with MCP + Git."
    # user_id = "ani"
    # session_id = "session_456"
    # # Run the asynchronous route_requests method
    # response = asyncio.run(pam.route_requests(user_input, user_id, session_id))
    # print(response)