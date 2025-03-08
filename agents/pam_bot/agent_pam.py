import sys
import os
from multi_agent_orchestrator.orchestrator import MultiAgentOrchestrator, OrchestratorConfig
from multi_agent_orchestrator.agents import Agent
from common.mistral_agent import MistralAgent

# Add project root to sys.path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


class PamBot:
    def __init__(self):
        # Initialize Mistral LLM
        self.mistral = MistralAgent()

        # Initialize Orchestrator
        self.DEFAULT_CONFIG = OrchestratorConfig()
        self.orchestrator = MultiAgentOrchestrator()

        # Register agents
        self.orchestrator.add_agent(Agent(name='SchruteBot', handle=self.handle_task_request))
        self.orchestrator.add_agent(Agent(name='JimsterAgent', handle=self.handle_prank_request))

    def route_request(self, message: str):
        # Use Mistral to determine intent
        intent = self.mistral.analyze_intent(message)

        # Delegate to the appropriate agent
        response = self.orchestrator.delegate(intent, message)
        return response

    def handle_task_request(self, message: str):
        # Logic to handle task-related requests
        return "Task handled."

    def handle_prank_request(self, message: str):
        # Logic to handle prank-related requests
        return "Prank executed."

# Example usage
if __name__ == "__main__":
    pam = PamBot()
    user_input = "Add task to simplify pam bot."
    print(pam.route_request(user_input))
