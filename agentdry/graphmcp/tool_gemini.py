from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
import os
from dotenv import load_dotenv

load_dotenv()
 
# Define a tool
@tool
def get_weather(location: str) -> str:
    "Get the current weather in a given location"
    return "It's sunny."
 
# Initialize model and bind the tool
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
llm_with_tools = llm.bind_tools([get_weather])
 
# Invoke with a query that should trigger the tool
query = "What's the weather in San Francisco?"
ai_msg = llm_with_tools.invoke(query)
 
# Access tool calls in the response
print(ai_msg.tool_calls)
 
# Pass tool results back to the model
tool_message = ToolMessage(
    content=get_weather(*ai_msg.tool_calls[0]['args']), 
    tool_call_id=ai_msg.tool_calls[0]['id']
)
final_response = llm_with_tools.invoke([ai_msg, tool_message])
print(final_response.content)