from utils.autotool_formatter import obtain_code_chain

def create_tool_from_user_input(query : str):
    """
    Pass the user query to chain to obtain the function from the llm

    Args:
        query (str): User input query
    """
    tool_from_llm = obtain_code_chain.invoke(query)
    code_string = "@mcp.tool()\n" + tool_from_llm.code
    return code_string

def append_code_to_server_file(code_to_insert : str, file_path : str):
    """
    Append the new MCP tool to target server above main

    Args:
        code_to_insert (str): The code string which needs to be appended
        file_path (str): File path of the MCP server

    Raises:
        ValueError: If name main is not found , error will be raised as it disqualifies to be a runnning server
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    main_index = None
    for i, line in enumerate(lines):
        stripped_line = ' '.join(line.strip().split())
        if stripped_line.startswith('if __name__ == "__main__"'):
            main_index = i
            break

    if main_index is None:
        raise ValueError("The 'if __name__ == \"__main__\"' block was not found in the file.")

    # Insert the new code before the main block
    lines = lines[:main_index] + [code_to_insert + '\n'] + lines[main_index:]
    print("Successfully appended function to server")
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Example usage

if __name__ == "__main__":

    file_path = r"..\servers\mcp_server_autorestart.py"
    code_to_insert = '''
    def new_function():
        """This is a new function with a docstring."""
        print("Hello from the new function!")
    '''

    append_code_to_server_file(file_path, code_to_insert)
