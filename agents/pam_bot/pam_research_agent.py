import asyncio
import json
import os
import argparse
import sys
from datetime import datetime

# Add project root to sys.path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from common.web_scraper import WebScraper  # Web search module
from common.pdf_generator import PDFGenerator  # PDF generation module
from common.mistral_agent import MistralAgent  # Mistral-7B Agent

class PamBot:
    def __init__(self):
        self.results = {}
        self.llm = MistralAgent()
        self.scraper = WebScraper()

    def generate_research_topics(self, query):
        """Generates research topics based on the user query using the LLM."""
        prompt = f"""
        Generate a structured JSON response with 5 subtopics for the following research query:
        Query: {query}
        Format:
        {{ "subtopics": ["topic1", "topic2", "topic3", "topic4", "topic5"] }}
        """
        response = self.llm.generate_response(prompt)
        try:
            response_json = json.loads(response)
            return response_json.get("subtopics", [])
        except json.JSONDecodeError:
            print("Error parsing JSON response from LLM.")
            return []

    async def research_task(self, query):
        """Conducts research by generating topics, performing web searches, extracting content, and summarizing results."""
        print(f"🎨 Pam is brainstorming search topics for: {query}")
        research_topics = self.generate_research_topics(query)
        print(f"Research topics are: {research_topics}")

        if not research_topics:
            print("😕 No relevant research topics generated.")
            return None

        all_results = []
        for topic in research_topics:
            print(f"🔍 Searching the web for: {topic}")
            search_results = self.scraper.search(topic)
            if search_results:
                for result in search_results:
                    extracted_content = self.scraper.extract(result['url'])
                    if extracted_content:
                        result['content'] = extracted_content[0].get('content', 'No extracted content available.')
                    else:
                        result['content'] = result.get('snippet', 'No additional content found.')
                    all_results.append(result)

        if not all_results:
            print("😕 No relevant results found.")
            return None

        summary = self.summarize_results(all_results)
        structured_summary = self.refine_summary(summary, query)
        self.results[query] = structured_summary

        pdf_path = self.generate_pdf(query, structured_summary)
        print(f"✅ Research done! Download your report here: {pdf_path}")

        return structured_summary

    def summarize_results(self, results):
        """Summarizes the research findings into a digestible format."""
        summary = "\n".join([f"- {res['title']}: {res['content']}" for res in results[:10]])
        return summary

    def refine_summary(self, summary, query):
        """Uses LLM to improve and structure the summary."""
        prompt = f"""
        Organize and enhance the readability of the following research summary:
        Query: {query}
        Summary: {summary}
        Return a structured and well-formatted version of the summary.
        """
        return self.llm.generate_response(prompt)

    def generate_pdf(self, topic, content):
        """Generates a PDF report from the research findings."""
        filename = f"{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf_path = os.path.join("reports", filename)

        pdf_generator = PDFGenerator()
        pdf_generator.create_pdf(title=f"Research Report: {topic}", content=content, output_path=pdf_path)

        return pdf_path

    async def handle_research_request(self, query):
        """Handles incoming research requests asynchronously."""
        return await self.research_task(query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PamBot Research Agent")
    parser.add_argument("query", type=str, help="Research query to process")
    args = parser.parse_args()

    pambot = PamBot()
    asyncio.run(pambot.handle_research_request(args.query))
