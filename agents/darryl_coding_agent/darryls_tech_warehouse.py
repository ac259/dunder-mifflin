import ollama

class DarrylBot:
    def __init__(self, model="gemma-1b"):
        """Initialize DarrylBot with a default model (Gemma 1B)."""
        self.model = model
    
    def set_model(self, model_name):
        """Switch between Gemma 1B and Gemma 4B."""
        if model_name in ["gemma-1b", "gemma-4b"]:
            self.model = model_name
        else:
            raise ValueError("Invalid model. Choose 'gemma-1b' or 'gemma-4b'.")
    
    def generate_code(self, prompt):
        """Generate code using the selected model."""
        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "Error: No response.")
    
    def debug_code(self, code_snippet):
        """Provide debugging suggestions for a given code snippet."""
        prompt = f"""Analyze and debug the following code:
        
        {code_snippet}
        
        Provide insights on potential issues and suggest fixes."""
        return self.generate_code(prompt)
    
    def optimize_code(self, code_snippet):
        """Optimize the given code snippet for efficiency and readability."""
        prompt = f"""Refactor and optimize the following code:
        
        {code_snippet}
        
        Ensure the updated code maintains functionality while improving efficiency and readability."""
        return self.generate_code(prompt)
