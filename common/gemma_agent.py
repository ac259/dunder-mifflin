import requests

class GemmaAgent:
    def __init__(self, model="gemma:1b", base_url="http://localhost:11434/api/generate"):
        self.model = model
        self.base_url = base_url
        self.intents = ["greeting", "question", "command", "farewell"]

    def generate_response(self, user_input: str) -> str:
        """
        Generates a helpful response using the Gemma 1B model via Ollama.
        """
        prompt = f"""You are a helpful, concise, and intelligent assistant. You answer clearly, avoid unnecessary repetition, and provide insightful responses.

        If a user asks a question, respond with clarity.
        If a user gives a command, acknowledge and assist.
        If the message is ambiguous, ask for clarification.

        User: {user_input}
        Assistant:"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()
        return response.json()["response"].strip()

    def analyze_intent(self, message: str) -> str:
        """
        Classifies the user's message into a known intent category.
        """
        prompt = f"""You are a system that identifies user intent. Given a message, classify it into one of the following categories: {', '.join(self.intents)}.

        Respond with only the intent label, nothing else.

        Message: "{message}"
        Intent:"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()
        intent = response.json()["response"].strip().lower()

        return intent if intent in self.intents else "unknown_intent"
