from multi_agent_orchestrator.classifiers import Classifier, ClassifierResult
from common.mistral_agent import MistralAgent
from typing import List, Optional, Dict
from multi_agent_orchestrator.types import ConversationMessage


class MistralClassifier(Classifier):
    def __init__(self):
        super().__init__()
        self.mistral_agent = MistralAgent()  # Initialize your Mistral agent here

    async def classify(self, user_input, chat_history):
        # Prepare a prompt for the Mistral model to determine the appropriate agent
        prompt = f"""
        You are a classifier that assigns user inputs to the most suitable agent based on their expertise.
        Available agents and their descriptions:
        {self.get_agents_descriptions()}
        
        User input: "{user_input}"
        
        Which agent is best suited to handle this input? Provide only the agent's name.
        """

        # Use the Mistral agent to generate a response
        response = self.mistral_agent.generate_response(prompt).strip()

        # Find the agent that matches the response
        for agent in self.agents:
            if agent.name.lower() == response.lower():
                return ClassifierResult(selected_agent=agent, confidence=1.0)

        # If no matching agent is found, return a default response
        return ClassifierResult(selected_agent=None, confidence=0.0)

    def get_agents_descriptions(self):
        # Helper method to format agents' descriptions for the prompt
        descriptions = ""
        for agent in self.agents:
            descriptions += f"- {agent.name}: {agent.description}\n"
        return descriptions

    async def process_request(
        self,
        input_text: str,
        user_id: str,
        session_id: str,
        chat_history: List[ConversationMessage],
        additional_params: Optional[Dict[str, str]] = None
    ) -> ClassifierResult:
            """
            Process the incoming request to classify the user input and select the appropriate agent.

            Args:
                input_text (str): The user's input text.
                user_id (str): The unique identifier for the user.
                session_id (str): The unique identifier for the session.
                chat_history (List[ConversationMessage]): The conversation history.
                additional_params (Optional[Dict[str, str]]): Additional parameters for processing.

            Returns:
                ClassifierResult: The result of the classification, including the selected agent and confidence score.
            """
            # Use the classify method to determine the appropriate agent
            classification_result = await self.classify(input_text, chat_history)
            return classification_result