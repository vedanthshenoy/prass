import sys
import os

# Add the 'agentdry' directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import create_and_update_tool
from utils.openai_format_check import parse_response

from groq import Groq
from dotenv import load_dotenv
load_dotenv()

groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def extract_info_and_create_tool(query: str):
    """
    Understand the user query :
    1. Extract the functionality of the query , eg. book flights, store in db
    2. Use this info in prompt to create_and_update_tool in main.py
    3. Rerun the original user query to obtain the answer

    Args:
        query (str): _description_
    """
    response_from_groq = groq_client.chat.completions.create(
                            messages=[
                                {
                                    "role": "system",
                                    "content": "you are an expert at understanding the exact ask of a user. you also only provide exact respose without any explainations"
                                },
                                {
                                    "role": "user",
                                    "content": f"""From the user query given , extract and only return the topic based on given examples,
                                                user query : Can you book a flight from Mangaluru to New York
                                                extracted topic : book flights given source and destination location
                                                
                                                user query : Can you upload this file to db
                                                extracted topic : Upload the file to db given the file
                                                
                                                user query : Please generate an image of a dog with wings
                                                extracted topic : Generate image given a prompt
                                                
                                                user query : Find all the mutual fund information from FY22 till now
                                                extracted topic : Search for mutual fund information given the year 
                                                
                                                user query : Convert 100 $ into INR
                                                extracted topic : Convert currency given source currency and target currency

                                                user query : {query}
                                                extracted topic : """,
                                }
                            ],
                            model = "llama-3.3-70b-versatile",
                            temperature = 0)

    print(parse_response(response_from_groq))
    return parse_response(response_from_groq)
    
    
if __name__ == "__main__":
    topic = extract_info_and_create_tool(query="Can you find the stats of Virat Kohli this IPL")
    create_and_update_tool(query=f"Create a function for {topic}")