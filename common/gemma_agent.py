import ollama

class GemmaAgent:
    def __init__(self, model_name='gemma3:1b'):
        self.model_name = model_name

    def set_model(self, model_name):
        """Set the model to be used by the agent."""
        self.model_name = model_name

    def generate_response(self, user_input):
        """Generate a response using the specified Gemma model via Ollama."""
        response = ollama.chat(model=self.model_name, messages=[
            {'role': 'user', 'content': user_input},
        ])
        return response['message']['content']

# Example usage
if __name__ == "__main__":
    agent = GemmaAgent()
    user_input = "Why is the sky blue?"
    
    # Using gemma3:1b model
    agent.set_model('gemma3:1b')
    response_1b = agent.generate_response(user_input)
    print(f"Response from gemma3:1b: {response_1b}")
