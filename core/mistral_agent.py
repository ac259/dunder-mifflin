from gpt4all import GPT4All

MODEL_NAME = "mistral-7b-instruct-v0.1.Q4_0.gguf"  # Replace with your downloaded model

class MistralAgent:
    def __init__(self):
        self.llm = GPT4All(MODEL_NAME)

    def generate_response(self, user_input):
        """Generate a response using Mistral 7B."""
        prompt = f"""
        You are an intelligent assistant. Respond in a helpful and insightful manner.

        User: {user_input}
        Assistant:"""

        response = self.llm.generate(prompt, max_tokens=100)
        return response
