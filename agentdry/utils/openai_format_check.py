import asyncio
import json

def transform_schema(input_schema):
    """Transform the input schema to the desired output format."""
    output_schema = {
        "type": "object",
        "properties": {},
        "required": input_schema.get("required", [])
    }
    
    # Transform properties
    for prop_name, prop_details in input_schema.get("properties", {}).items():
        output_schema["properties"][prop_name] = {
            "type": "integer" if prop_details.get("type") == "integer" else prop_details.get("type"),
            "description": f"The {'first' if prop_name == 'a' else 'second'} number"
        }
    
    return output_schema

def transform_schemas(input_schemas):
    """Transform multiple schemas and return the results as a list."""
    transformed_schemas = []
    
    for schema in input_schemas:
        transformed_schema = transform_schema(schema)
        transformed_schemas.append(transformed_schema)
    
    return transformed_schemas

# Example of how to use this in another function
def use_transformed_schemas(input_schemas):
    # Get the transformed schemas
    transformed_schemas = transform_schemas(input_schemas)
    
    # Now you can use the transformed schemas directly
    # For example, return them as JSON strings
    json_results = [json.dumps(schema, indent=4) for schema in transformed_schemas]
    return json_results


def parse_response(response):
    """
    Parse a ChatCompletion response to check if it contains a function call.
    If it does, extract the function name and arguments.
    If not, return the content of the message.
    
    Args:
        response: The ChatCompletion response object
        
    Returns:
        dict: If function call exists: A dictionary with 'has_function_call' (True), 
              'function_name' (str), and 'function_args' (dict)
        str: If no function call: The content of the message
    """
    # Check if response has choices with tool_calls
    if (hasattr(response, 'choices') and 
        response.choices and 
        hasattr(response.choices[0], 'message') and 
        hasattr(response.choices[0].message, 'tool_calls') and
        response.choices[0].message.tool_calls):
        
        # Get the first tool call
        tool_call = response.choices[0].message.tool_calls[0]
        
        # Check if it's a function call
        if tool_call.type == 'function':
            result = {
                'has_function_call': True,
                'function_name': tool_call.function.name
            }
            
            # Parse the arguments JSON string into a Python dictionary
            import json
            try:
                result['function_args'] = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw arguments string
                result['function_args'] = tool_call.function.arguments
            
            return result
    
    # If no function call exists, return the content
    if (hasattr(response, 'choices') and 
        response.choices and 
        hasattr(response.choices[0], 'message') and 
        hasattr(response.choices[0].message, 'content')):
        return response.choices[0].message.content
    
    # If no content found either
    return None

if __name__ == "__main__":

    sample_schemas = {
                'properties': {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}, 
                'required': ['a', 'b'], 
                'title': 'addArguments', 
                'type': 'object'
            }

    transformed_schemas = transform_schema(sample_schemas)
    # print(transformed_schemas)

    tooler = [{
                        'type' : 'function',
                        'function' : {
                            "name" : "add",
                            "description": "Adds two numbers",
                            "parameters": transformed_schemas,
                        }
                    }]
        
    from agentdry.clients.groq_client_mcp import client

    response = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "user",
                                    "content": "How is claude today",
                                }
                            ],
                            model = "llama-3.3-70b-versatile",
                            temperature = 0,
                            tools = tooler)

    print(response)