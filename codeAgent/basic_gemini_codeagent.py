import os
import sys
import warnings
from dotenv import load_dotenv
from smolagents import ToolCollection, CodeAgent, LiteLLMModel, Tool
from mcp import StdioServerParameters
from langchain_core.prompts import ChatPromptTemplate
from langchain_perplexity import ChatPerplexity
import subprocess
# Set UTF-8 encoding environment variable for PowerShell
os.environ["PYTHONUTF8"] = "1"

# model = ChatPerplexity(
#     temperature=0, pplx_api_key=os.getenv("PERPLEXITY_API_KEY"), model="llama-3-sonar-small-32k-online"
# )
# Suppress resource warnings which are happening during cleanup
warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*")

# Load environment variables
load_dotenv()
github_api_key = os.getenv("GITHUB_API_KEY")
if not github_api_key:
    sys.exit(1)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    sys.exit(1)

def main():
    try:
        # this is for openai model or base models
        model = LiteLLMModel(
            model_id="openai/gpt-4.1",
            api_base="https://models.github.ai/inference",
            api_key=github_api_key,
            publisher="openai"
        )
        # model = LiteLLMModel(
        #     model_id="perplexity/r1-1776",
        #     api_base="https://api.perplexity.ai",
        #     api_key=os.getenv("PERPLEXITY_API_KEY"),
        #     drop_params=True,
        # )

        # this is for gemini model
        # model = LiteLLMModel(
        #     model_id="gemini/gemini-2.0-flash",
        #     api_key=gemini_api_key,
        # )
        
        server_parameters = StdioServerParameters(
            command="uv",
            args=["run", "--with", "mcp", "mcp", "run", "tools.py"],
            env={"UV_PYTHON": "3.12", "PYTHONUTF8": "1", **os.environ},
        )
        
        try:
            with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
                agent = CodeAgent(tools=[*tool_collection.tools], add_base_tools=False, model=model)
                
                input_data = input("Enter your question: ")
                result = agent.run(input_data)
                
                return result
                
        except Exception:
            pass
            
    except Exception:
        pass

if __name__ == "__main__":
    result = main()
    os._exit(0)
