import aiohttp
import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TAVILY_SEARCH_URL = "https://api.tavily.com/search"
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # Load API key from .env file

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not set. Please set it in a .env file.")

class WebScraper:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {TAVILY_API_KEY}",
            "Content-Type": "application/json"
        }
    
    async def fetch(self, session, url, payload):
        """Fetches search results asynchronously from Tavily."""
        try:
            async with session.post(url, headers=self.headers, json=payload, timeout=10) as response:
                return await response.json()
        except Exception as e:
            print(f"⚠️ Failed to fetch {url}: {e}")
            return None
    
    async def scrape_results(self, query):
        """Performs a Tavily API search and extracts results."""
        payload = {"query": query, "num_results": 10}
        async with aiohttp.ClientSession() as session:
            json_response = await self.fetch(session, TAVILY_SEARCH_URL, payload)
            if not json_response or "results" not in json_response:
                return []
            
            results = []
            for item in json_response["results"]:
                results.append({"title": item["title"], "url": item["url"], "snippet": item.get("snippet", "No snippet available")})
            
            return results
    
    async def async_search(self, query):
        """Public method to trigger the search."""
        return await self.scrape_results(query)

# Example usage
if __name__ == "__main__":
    scraper = WebScraper()
    results = asyncio.run(scraper.async_search("Latest AI trends"))
    print(results)
