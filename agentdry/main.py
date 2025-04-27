from utils.append_to_server import create_tool_from_user_input, append_code_to_server_file

def create_and_update_tool(query: str, server_file_path : str = r"C:\prass\agentdry\servers\mcp_trial_server.py"):
    print(query)
    code_string = create_tool_from_user_input(query)
    append_code_to_server_file(code_string, server_file_path)
    print("Server Updated !!!")
    print("Ask the query again to obtain the answer.") # will route query back in future versions rather than user asking again
    
if __name__ == "__main__":
    create_and_update_tool("Create a function for dividing two numbers")