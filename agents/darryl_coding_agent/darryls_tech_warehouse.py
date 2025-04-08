import ollama
from multi_agent_orchestrator.agents import Agent, AgentOptions, AgentCallbacks
from multi_agent_orchestrator.types import ConversationMessage
from typing import List, Optional, Dict

MODEL = "gemma3:1b"  # Default model

class DarrylBot(Agent):
    def __init__(self):
        """Initialize DarrylBot with a default model (Gemma 1B)."""
        options = AgentOptions(
            name="DarrylAgent",
            description=(
                "A helpful AI assistant that specializes in all programming tasks — "
                "including writing code, debugging, optimizing, generating code from prompts, "
                "explaining code, or answering technical questions."
            ),
            save_chat=True,
            callbacks=AgentCallbacks(),
            LOG_AGENT_DEBUG_TRACE=False
        )
        super().__init__(options)
        self.model = MODEL

    def set_model(self, model_name):
        """Switch between Gemma 1B and Gemma 4B."""
        if model_name in ["gemma3:1b", "gemma3:4b"]:
            self.model = model_name
        else:
            raise ValueError("Invalid model. Choose 'gemma3:1b' or 'gemma3:4b'.")

    async def process_request(
        self,
        input_text: str,
        user_id: str,
        session_id: str,
        chat_history: List[ConversationMessage],
        additional_params: Optional[Dict[str, str]] = None
    ) -> str:
        """Processes requests related to code generation and model switching."""
        message = input_text.strip()

        if message.lower().startswith("set model"):
            model_name = message.replace("set model", "").strip()
            try:
                self.set_model(model_name)
                return f"✅ DarrylBot now using model: {self.model}"
            except ValueError as e:
                return str(e)

        return await self.generate_code(message)

    def detect_language_from_prompt(self, prompt: str) -> str:
        known_languages = [
            "python", "javascript", "typescript", "java", "c++", "c", "c#", "ruby", "go", "rust",
            "kotlin", "swift", "bash", "sql", "html", "css", "php", "r"
        ]
        prompt_lower = prompt.lower()
        for lang in known_languages:
            if lang in prompt_lower:
                return lang
        return "text"

    async def generate_code(self, prompt):
        """Generate code using the selected model."""
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        content = response["message"]["content"] if "message" in response else "Error: No response."

        language = self.detect_language_from_prompt(prompt)

        return f"```{language}{content.strip()}```"

    async def debug_code(self, code_snippet):
        """Provide debugging suggestions for a given code snippet."""
        prompt = f"""Analyze and debug the following code:

                {code_snippet}

                Provide insights on potential issues and suggest fixes."""
        return await self.generate_code(prompt)

    async def optimize_code(self, code_snippet):
        """Optimize the given code snippet for efficiency and readability."""
        prompt = f"""Refactor and optimize the following code:

        {code_snippet}

        Ensure the updated code maintains functionality while improving efficiency and readability."""
        return await self.generate_code(prompt)
