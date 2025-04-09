from crawl4ai import Crawl4AI
from common.mistral_agent import MistralAgent

class DueDiligenceTool:
    def __init__(self):
        self.crawler = Crawl4AI()
        self.mistral = MistralAgent()

    def deep_research(self, query: str, max_results: int = 5) -> str:
        """
        Perform a deep research on the given query by crawling and summarizing results.
        Returns a summary with a professional tone, as if written by Oscar from The Office.
        """
        try:
            results = self.crawler.search(query=query, max_results=max_results)
        except Exception as e:
            return f"There was an error while performing the research: {e}"

        if not results:
            return "No substantial results were found. Might I suggest refining your query?"

        content = "\n\n".join([
            f"{res.get('title', 'Untitled')}\n{res.get('content', '')}" for res in results if 'content' in res
        ])

        prompt = f"""
        You are Oscar Martinez from The Office. You are intelligent, precise, and sometimes condescending in a subtle way.
        Summarize the following information in a professional and informative tone, with occasional hints of intellectual superiority:

        {content}

        Summary:
        """
        
        summary = self.mistral.generate_response(prompt)
        return summary.strip()
