# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import sys, asyncio
from google.genai import types
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

from mcp import ClientSession
from mcp.client.sse import sse_client

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


async def run():
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:

            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            # print(tools)
            
            tools = types.Tool(function_declarations=[
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                }
                for tool in tools.tools
            ])
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",  # Or your preferred model supporting function calling
                contents="Can you add 2 and 3",
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    tools=[tools],
                ),  # Example other config
            )
        # Check for a function call
            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                print(f"Function to call: {function_call.name}")
                print(f"Arguments: {function_call.args}")
                result = await session.call_tool(function_call.name, arguments=function_call.args)
                print(result.content[0].text)
                # In a real app, you would call your function here:
                # result = await session.call_tool(function_call.args, arguments=function_call.args)
                # sent new request with function call
            else:
                print("No function call found in the response.")
                print(response.text)
                
            


asyncio.run(run())
# if __name__ == "__main__":
#     try:
#         result = asyncio.run(main())
#         print(result)
#     except Exception as e:
#         print(e)