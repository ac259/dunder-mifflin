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

    def analyze_intent(self, message: str) -> str:
        prompt = f"Classify the intent of the following message into one of the predefined categories {self.intents}: \"{message}\""
        inputs = self.tokenizer(prompt, return_tensors='pt')
        outputs = self.model.generate(**inputs, max_length=50)
        intent = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return intent.strip().lower()