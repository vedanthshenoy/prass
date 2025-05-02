from mcp.server.fastmcp import FastMCP
# from rag_system import rag_system_bm25
mcp = FastMCP("Tools")

@mcp.tool()
def adding(x: float, y: float) -> float:
    """
    Adds two numbers together.

    Args:
        x: The first number to be added.
        y: The second number to be added.

    Returns:
        The sum of x and y.
    """
    return x + y

@mcp.tool()
def secret_code() -> str:
    """
    Returns a secret code.

    Returns:
        A string representing the secret code.
    """
    return "secret_code_123"

# @mcp.tool()
# def document_retriever(query: str) -> str:
#     """
#     Retrieves documents based on a query.

#     Args:
#         query: The search query.

#     Returns:
#         A string containing the retrieved documents.
#     """
#     results = rag_system_bm25(query=query)
#     if results:
#         return results
#     else:
#         return "No relevant documents found for the query."

if __name__ == "__main__":
    mcp.run(transport="stdio")
    # document_retriever("What is neral network?")
