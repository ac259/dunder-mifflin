import asyncio
import json
import os
import argparse
import sys
import logging
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer


# Add project root to sys.path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from common.web_scraper import WebScraper  # Web search module
from common.pdf_generator import PDFGenerator  # PDF generation module

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PamBot:
    def __init__(self):
        self.results = {}
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../common/qwen2.5_32b_instruct"))
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype="auto", device_map="auto")
        self.scraper = WebScraper()

    def generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        # model card for the qwen model indicates 8k max output length
        outputs = self.model.generate(**inputs, max_length=5000, temperature=0.7)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def generate_research_topics(self, query):
        """Generates research topics based on the user query using the LLM."""
        prompt = f"""
        Generate a structured JSON response with 5 subtopics for the following research query:
        Query: {query}
        Format:
        {{ "subtopics": ["topic1", "topic2", "topic3", "topic4", "topic5"] }}
        """
        response = self.generate_response(prompt)
        try:
            response_json = json.loads(response)
            return response_json.get("subtopics", [])
        except json.JSONDecodeError:
            logger.error("Error parsing JSON response from LLM.")
            return []

    async def research_topic(self, topic):
        """Conducts web search and content extraction for a single topic."""
        logger.info(f"🔍 Searching the web for: {topic}")
        search_results = self.scraper.search(topic)
        if not search_results:
            return []

        results = []
        for result in search_results:
            extracted_content = self.scraper.extract(result['url'])
            if extracted_content:
                result['content'] = extracted_content[0].get('content', 'No extracted content available.')
            else:
                result['content'] = result.get('snippet', 'No additional content found.')
            results.append(result)
        return results

    async def research_task(self, query):
        """Conducts research by generating topics, performing web searches, extracting content, and summarizing results."""
        logger.info(f"🎨 Pam is brainstorming search topics for: {query}")
        research_topics = self.generate_research_topics(query)
        logger.info(f"Research topics are: {research_topics}")

        if not research_topics:
            logger.warning("😕 No relevant research topics generated.")
            return None

        # Parallelize web searches and content extractions
        all_results = await asyncio.gather(*[self.research_topic(topic) for topic in research_topics])
        all_results = [item for sublist in all_results for item in sublist]  # Flatten the list

        if not all_results:
            logger.warning("😕 No relevant results found.")
            return None

        summary = self.summarize_results(all_results)
        structured_summary = self.refine_summary(summary, query)
        self.results[query] = structured_summary

        pdf_path = self.generate_pdf(query, structured_summary)
        logger.info(f"✅ Research done! Download your report here: {pdf_path}")

        return structured_summary

    def summarize_results(self, results):
        """Summarizes the research findings into a digestible format using LLM."""
        content = "\n".join([f"- {res['title']}: {res['content']}" for res in results[:10]])
        prompt = f"""
        Summarize the following research findings into a coherent and structured format:
        {content}
        Provide a summary with an introduction, key findings, and conclusion.
        """
        return self.llm.generate_response(prompt)

    def refine_summary(self, summary, query):
        """Uses LLM to further improve and structure the summary."""
        prompt = f"""
        Organize and enhance the readability of the following research summary for the query "{query}":
        {summary}
        Structure it with sections like Introduction, Key Findings, and Conclusion.
        """
        return self.llm.generate_response(prompt)

    def generate_pdf(self, topic, content):
        """Generates a PDF report from the research findings."""
        filename = f"{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf_path = os.path.join("reports", filename)

        # Preprocess content to ensure proper formatting
        formatted_content = content.replace('\n', '<br>')  # Simple replacement for line breaks

        pdf_generator = PDFGenerator()
        pdf_generator.create_pdf(title=f"Research Report: {topic}", content=formatted_content, output_path=pdf_path)

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