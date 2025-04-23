# from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()


# llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     groq_api_key = os.getenv("GROK_API_KEY")
#     # other params...
# )

# print(llm.invoke("Hi how are you"))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel, Field
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from agentdry.formatters.openai_format_check import transform_schema, parse_response

from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


async def run():
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:

            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            
            # print(tools)
            
            tools = [
                {
                    'type' : 'function',
                    'function' : {
                        "name" : tool.name,
                        "description": tool.description,
                        "parameters": transform_schema(tool.inputSchema),
                    }
                }
                for tool in tools.tools
            ]
            
            # print(tools)
            
            response = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": "Can you multiply the first prime number and the last two digit number",
                            }
                        ],
                        model = "llama-3.3-70b-versatile",
                        temperature = 0,
                        tools = tools)
        # Check for a function call
            # if response[0]
            result = parse_response(response)
            # print(result)
            if type(result)==dict:
                print("Calling MCP tool", result["function_name"])
                result = await session.call_tool(result['function_name'], arguments=result['function_args'])
                print(result.content[0].text)
            else:
                print(result)
                
            


if __name__ == "__main__":
    asyncio.run(run())