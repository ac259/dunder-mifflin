import ollama
from multi_agent_orchestrator.agents import Agent, AgentOptions, AgentCallbacks
from multi_agent_orchestrator.types import ConversationMessage
from typing import List, Optional, Dict

MODEL = "gemma-1b" # Default model

class DarrylBot(Agent):
    def __init__(self):
        """Initialize DarrylBot with a default model (Gemma 1B)."""
        options = AgentOptions(
            name="DarrylAgent",
            description="A Coding assistant specializing in writing, debugging code",
            save_chat=True,
            callbacks=AgentCallbacks(),
            LOG_AGENT_DEBUG_TRACE=False
        )
        super().__init__(options)
        self.model = MODEL
    
    def set_model(self, model_name):
        """Switch between Gemma 1B and Gemma 4B."""
        if model_name in ["gemma-1b", "gemma-4b"]:
            self.model = model_name
        else:
            raise ValueError("Invalid model. Choose 'gemma-1b' or 'gemma-4b'.")
    
    async def process_request(
        self,
        input_text: str,
        user_id: str,
        session_id: str,
        chat_history: List[ConversationMessage],
        additional_params: Optional[Dict[str, str]] = None
    ) -> str:
        """Processes requests related to code generation, debugging, and optimization."""
        message = input_text.lower().strip()
        
        if message.startswith("generate code"):
            prompt = message.replace("generate code", "").strip()
            return await self.generate_code(prompt)
        
        elif message.startswith("debug code"):
            code_snippet = message.replace("debug code", "").strip()
            return await self.debug_code(code_snippet)
        
        elif message.startswith("optimize code"):
            code_snippet = message.replace("optimize code", "").strip()
            return await self.optimize_code(code_snippet)
        
        elif message.startswith("set model"):
            model_name = message.replace("set model", "").strip()
            try:
                self.set_model(model_name)
                return f"✅ DarrylBot now using model: {self.model}"
            except ValueError as e:
                return str(e)
        
        return "❌ Command not recognized. Try 'generate code', 'debug code', or 'optimize code'."
    
    async def generate_code(self, prompt):
        """Generate code using the selected model."""
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "Error: No response.")
    
    async def debug_code(self, code_snippet):
        """Provide debugging suggestions for a given code snippet."""
        prompt = f"""Analyze and debug the following code:
        
        {code_snippet}
        
        Provide insights on potential issues and suggest fixes."""
        return self.generate_code(prompt)
    
    async def optimize_code(self, code_snippet):
        """Optimize the given code snippet for efficiency and readability."""
        prompt = f"""Refactor and optimize the following code:
        
        {code_snippet}
        
        Ensure the updated code maintains functionality while improving efficiency and readability."""
        return self.generate_code(prompt)
