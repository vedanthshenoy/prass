from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model = "gemini-2.0-flash",
                   api_key = os.getenv("GEMINI_API_KEY"),
                   openai_proxy = "https://generativelanguage.googleapis.com/v1beta/openai/")

async def run():
    async with MultiServerMCPClient(
        {
            "math": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        print(client)
        # agent = create_react_agent(model, client.get_tools())
        # math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
        # print(math_response)
        
if __name__ == "__main__":
    asyncio.run(run())
    