import requests  # For API calls (or use xAI's SDK if available)

class GrokAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.x.ai/v1/grok"  # Hypothetical URL; check xAI docs

    def generate(self, prompt):
        # Make API call to Grok
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "prompt": prompt,
            "max_tokens": 150,  # Adjust as needed
            # Add "deepsearch": True here if supported and desired
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise error if request fails
        return response.json().get("text")  # Adjust based on actual API response