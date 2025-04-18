import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
import ollama
from duckduckgo_search import DDGS
from itertools import islice

class DueDiligenceTool:
    def __init__(self):
        self.summarization_model = "gemma3:1b"

    async def _generate_response_async(self, prompt: str) -> str:
        try:
            response = await asyncio.to_thread(
                ollama.chat,
                model=self.summarization_model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
        except Exception as e:
            print(f"Error generating Ollama response: {e}")
            return f"Error generating summary: {e}"

    async def get_crawled_results(self, query: str, max_results: int = 5):
        """
        Performs a DuckDuckGo search and uses Crawl4AI to extract content from each result.
        Returns a list of (title, url, content).
        """
        results = []
        fetch_config = CrawlerRunConfig(
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=0,
                max_pages=1,
                include_external=False
            ),
            scraping_strategy=LXMLWebScrapingStrategy(),
            verbose=False
        )

        try:
            with DDGS() as ddgs:
                ddgs_text_gen = ddgs.text(query, region='wt-wt', safesearch='Moderate')
                async with AsyncWebCrawler() as crawler:
                    for result in islice(ddgs_text_gen, max_results):
                        title = result.get('title', 'Untitled')
                        url = result.get('href', '#')

                        try:
                            crawl_results = await crawler.arun(url, config=fetch_config)
                            page = crawl_results[0] if crawl_results else None
                            content = getattr(page, 'markdown', None) or getattr(page, 'html', None) or "[No content]"
                        except Exception as e:
                            print(f"Error fetching content from {url}: {e}")
                            content = "[Error fetching content]"

                        results.append((title, url, content.strip()[:1500]))
        except Exception as e:
            print(f"Search failed: {e}")

        return results

    async def search(self, query: str, max_results: int = 5) -> str:
        entries = await self.get_crawled_results(query, max_results)
        if not entries:
            return "No search results found."

        output_lines = [f"**Search Results for '{query}':**"]
        for i, (title, url, content) in enumerate(entries):
            output_lines.append(f"{i+1}. **[{title}]({url})** > {content[:500]}...")

        return "\n".join(output_lines)

    async def summarize_search_results(self, query: str, max_urls_to_summarize: int = 3) -> str:
        entries = await self.get_crawled_results(query, max_urls_to_summarize)
        if not entries:
            return "No usable content found to generate a summary."

        sources_block = "\n\n".join([
            f"### {title}\nURL: {url}\n\n{content}" for title, url, content in entries
        ])

        prompt = f"""You are Oscar Martinez from The Office. Using the following sources, write a clear, professional research summary in Markdown. Include:

            - An executive summary
            - Bullet-point insights
            - Source highlights
            - A final witty remark from Oscar

            ### Sources:
            {sources_block}

            ### Markdown Summary:
        """

        return await self._generate_response_async(prompt)

    async def deep_crawl_url(self, url: str, max_depth: int = 1, max_pages: int = 5) -> str:
        print(f"Starting deep crawl for URL: {url} with max_depth={max_depth}, max_pages={max_pages}")
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

            print(f"Deep crawl finished. Found {len(results)} pages.")
            if not results:
                return f"Deep crawl initiated for {url}, but no pages were successfully crawled or yielded content."

            for i, result in enumerate(results):
                content = getattr(result, 'markdown', None) or getattr(result, 'html', None) or ""
                if content and content.strip():
                    crawled_content.append(f"**Crawled URL ({i+1}):** {result.url}\n**Depth:** {result.metadata.get('depth', 'N/A')}\n**Content Snippet:**\n{content[:1000]}...\n---")
                else:
                    crawled_content.append(f"**Crawled URL ({i+1}):** {result.url}\n**Depth:** {result.metadata.get('depth', 'N/A')}\n**Content:** [No substantial content extracted]\n---")

        except Exception as e:
            print(f"Error during deep crawl of {url}: {e}")
            if "BrowserType.launch" in str(e):
                return f"Error during deep crawl: Browser context issue. Ensure Playwright is installed correctly (`playwright install`). Details: {e}"
            return f"An error occurred during the deep crawl: {e}"

        if not crawled_content:
            return f"Deep crawl completed for {url}, but no usable content was extracted."

        full_crawled_text = "\n\n".join(crawled_content)
        prompt = f"""
            You are Oscar Martinez from The Office. Provide a professional and concise Markdown summary based *only* on the following findings from a deep crawl of the website starting at {url}. Focus on the key information extracted.

            **Collected Content Snippets:**
            {full_crawled_text}

            **Markdown Summary of Deep Crawl Findings:**
            """
        return await self._generate_response_async(prompt)
