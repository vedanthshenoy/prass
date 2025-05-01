from langchain_google_genai import ChatGoogleGenerativeAI
from google.ai.generativelanguage_v1beta.types import Tool as GenAITool
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

search_resp = llm.invoke(
    "When is the next total solar eclipse in US?",
    tools=[GenAITool(google_search={})],
)
print(search_resp.content)
 
# Code Execution
# code_resp = llm.invoke(
#     "What is 2*2, use python",
#     tools=[GenAITool(code_execution={})],
# )
 
# for c in code_resp.content:
#     if isinstance(c, dict):
#         if c["type"] == 'code_execution_result':
#             print(f"Code execution result: {c['code_execution_result']}")
#         elif c["type"] == 'executable_code':
#             print(f"Executable code: {c['executable_code']}")
#     else:
#         print(c)