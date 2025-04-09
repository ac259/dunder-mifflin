import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
import ollama

class DueDiligenceTool:
    def __init__(self):
        self.model = "gemma3:1b"

    def generate_response(self, prompt: str) -> str:
        try:
            response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
            return response['message']['content']
        except Exception as e:
            return f"Error generating response: {e}"

    async def search(self, query: str, max_results: int = 5) -> str:
        output_lines = ["**Search Results:**\n"]
        try:
            async with AsyncWebCrawler() as crawler:
                results = await crawler.search(query=query, max_results=max_results)

                if not results:
                    return "No results were found for your query."

                for i, res in enumerate(results):
                    title = res.get('title', 'Untitled')
                    url = res.get('url', '#')
                    output_lines.append(f"{i+1}. **[{title}]({url})**")

        except AttributeError:
            return "Error: AsyncWebCrawler may not support direct 'search'."
        except Exception as e:
            return f"Error during search: {e}"

        return "\n".join(output_lines)

    async def summarize_search_results(self, query: str, max_results: int = 3) -> str:
        results_content = []
        try:
            async with AsyncWebCrawler() as crawler:
                search_results = await crawler.search(query=query, max_results=max_results)

                if not search_results:
                    return "No substantial results found to summarize."

                for res in search_results:
                    title = res.get('title', 'Untitled')
                    content = res.get('content')
                    url = res.get('url')
                    if content and content.strip():
                        results_content.append(f"**Source Title:** {title}\n**URL:** {url}\n**Content:**\n{content}\n---")
                    elif url:
                        results_content.append(f"**Source Title:** {title}\n**URL:** {url}\n**Content:** [Content not directly available]\n---")

        except Exception as e:
            return f"Error summarizing search results: {e}"

        if not results_content:
            return "No suitable content found for summarization."

        full_content = "\n\n".join(results_content)
        prompt = f"""
        You are Oscar Martinez from The Office. Provide a clear, professional summary of the following information:

        {full_content}

        Summary:
        """
        return self.generate_response(prompt).strip()

    async def deep_crawl_url(self, url: str, max_depth: int = 1, max_pages: int = 10) -> str:
        crawled_content = []

        config = CrawlerRunConfig(
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=max_depth,
                max_pages=max_pages,
                include_external=False,
            ),
            scraping_strategy=LXMLWebScrapingStrategy(),
            verbose=False
        )

        try:
            async with AsyncWebCrawler() as crawler:
                results = await crawler.arun(url, config=config)

            if not results:
                return f"No pages successfully crawled from {url}."

            for i, result in enumerate(results):
                content = result.markdown if hasattr(result, 'markdown') and result.markdown else result.content
                if content and content.strip():
                    crawled_content.append(f"**URL ({i+1}):** {result.url}\n**Content Snippet:**\n{content[:500]}...\n---")
                else:
                    crawled_content.append(f"**URL ({i+1}):** {result.url}\n**Content:** [No substantial content]\n---")

        except Exception as e:
            return f"Error during deep crawl: {e}"

        if not crawled_content:
            return f"Deep crawl completed, but no usable content extracted from {url}."

        full_crawled_text = "\n\n".join(crawled_content)
        prompt = f"""
        You are Oscar Martinez from The Office. Provide a professional and concise summary of the deep crawl findings:

        {full_crawled_text}

        Summary:
        """
        return self.generate_response(prompt).strip()