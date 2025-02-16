import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables from .env file
load_dotenv()

class WebScraper:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY is not set. Please set it in a .env file.")
        self.client = TavilyClient(api_key=api_key)

    def search(self, query, max_results=5):
        """Performs a search using Tavily's API."""
        try:
            response = self.client.search(query, max_results=max_results)
            return response.get('results', [])
        except Exception as e:
            print(f"⚠️ Error during Tavily search: {e}")
            return []

    def extract(self, url):
        """Extracts content from a given URL using Tavily's API."""
        try:
            response = self.client.extract(urls=[url])
            return response.get('results', [])
        except Exception as e:
            print(f"⚠️ Error during Tavily extract: {e}")
            return []
