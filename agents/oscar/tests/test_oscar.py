import asyncio
from tools.due_diligence_tool import DueDiligenceTool
from agents.oscar.agent_oscar import OscarAgent  # Adjust path if needed

async def test_tool():
    tool = DueDiligenceTool()

    print("\n🔍 Testing: Simple Search")
    result = await tool.search("electric vehicles 2025 outlook")
    print(result)

    print("\n📄 Testing: Summarized Search")
    result = await tool.summarize_search_results("latest in robotics for manufacturing")
    print(result)

    print("\n🕵️ Testing: Deep Crawl")
    result = await tool.deep_crawl_url("https://www.bostondynamics.com")
    print(result)

async def test_agent():
    agent = OscarAgent()

    print("\n🧠 Testing Agent: Search Handler")
    print(await agent.handle_search_request("how does solar panel efficiency work"))

    print("\n🧠 Testing Agent: Summarize Handler")
    print(await agent.handle_summarize_request("state of AI adoption in finance"))

    print("\n🧠 Testing Agent: Deep Crawl Handler")
    print(await agent.handle_deep_crawl_request("https://openai.com"))

if __name__ == "__main__":
    asyncio.run(test_tool())
    asyncio.run(test_agent())
