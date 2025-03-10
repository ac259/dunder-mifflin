import sys
import os
import asyncio
from multi_agent_orchestrator.orchestrator import MultiAgentOrchestrator, OrchestratorConfig
from multi_agent_orchestrator.agents import Agent

# Add project root to sys.path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from common.mistral_agent import MistralAgent
from agents.jimster.big_tuna import JimsterAgent
from agents.schrute_bot.schrute_bot import SchruteBot
from common.mistral_classifier import MistralClassifier

class PamBot:
    def __init__(self):
        # Initialize Mistral LLM
        self.mistral = MistralAgent()
        self.schrute_bot = SchruteBot()
        self.jimster_agent = JimsterAgent()
        self.classifier = MistralClassifier()
        

        # Initialize Orchestrator
        self.DEFAULT_CONFIG = OrchestratorConfig(
                                                LOG_AGENT_CHAT=True,
                                                LOG_CLASSIFIER_CHAT=True,
                                                LOG_CLASSIFIER_RAW_OUTPUT=False,
                                                LOG_CLASSIFIER_OUTPUT=True,
                                                LOG_EXECUTION_TIMES=True,
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
        agents = [self.schrute_bot, self.jimster_agent]
        for agent in agents:
            print(f"Type: {type(agent)}, Value: {agent}")
        # Pass agents list to the classifier before adding them
        self.classifier.set_agents(agents)
        
        for agent in agents:
            self.orchestrator.add_agent(agent)
            print(f"✅ Registered agent: {agent.name}")

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
if __name__ == "__main__":
    pam = PamBot()
    user_input = "View Tasks"
    user_id = "ani"
    session_id = "session_456"
    # Run the asynchronous route_requests method
    response = asyncio.run(pam.route_requests(user_input, user_id, session_id))
    print(response)