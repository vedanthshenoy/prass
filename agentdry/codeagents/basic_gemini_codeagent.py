import os
import sys
import warnings
from dotenv import load_dotenv
from smolagents import ToolCollection, CodeAgent, LiteLLMModel, Tool
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from langchain_core.prompts import ChatPromptTemplate
import subprocess
import asyncio
# Set UTF-8 encoding environment variable for PowerShell
os.environ["PYTHONUTF8"] = "1"

warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*")

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    sys.exit(1)

async def main():
    # This is for gemini model
    model = LiteLLMModel(
        model_id="gemini/gemini-2.0-flash",
        api_key=gemini_api_key,
    )
    
    with ToolCollection.from_mcp({"url": "http://127.0.0.1:8000/sse"}, trust_remote_code=True) as tool_collection:
        agent = CodeAgent(tools=[*tool_collection.tools], add_base_tools=True, model=model)     
        input_data = "What is 5+6"
        result = agent.run(input_data)  # Add await here
        print(result)
        return result

if __name__ == "__main__":
    asyncio.run(main())
    # print(result)

