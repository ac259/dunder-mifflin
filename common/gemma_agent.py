import ollama

class GemmaAgent:
    def __init__(self, model_name='gemma3:4b'):
        self.model_name = model_name

    def generate_response(self, user_input):
        """Generate a response using the Gemma 3 4B model via Ollama."""
        response = ollama.chat(model=self.model_name, messages=[
            {'role': 'user', 'content': user_input},
        ])
        return response['message']['content']

# Example usage
if __name__ == "__main__":
    agent = GemmaAgent()
    user_input = "Why is the sky blue?"
    response = agent.generate_response(user_input)
    print(response)
