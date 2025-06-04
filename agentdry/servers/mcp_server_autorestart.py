from mcp.server.fastmcp import FastMCP
import time
import os
import sys
import threading

# Record the last modified time of this script
current_file = os.path.abspath(__file__)
last_modified = os.path.getmtime(current_file)

def file_watcher():
    """Monitor this file for changes and restart when modified."""
    global last_modified
    while True:
        time.sleep(1)  # Check every second
        current_modified = os.path.getmtime(current_file)
        if current_modified > last_modified:
            print("File changed, restarting server...")
            try:
                mcp.stop()
            except Exception:
                pass
            time.sleep(2)  # Give the OS time to release the port
            python = sys.executable
            os.execl(python, python, *sys.argv)

mcp = FastMCP("Math")

@mcp.tool()
def divide_numbers(numerator: int, denominator: int):
    """Divides two numbers and handles potential ZeroDivisionError.

    Args:
        numerator: The number to be divided.
        denominator: The number to divide by.

    Returns:
        The result of the division, or an appropriate message if denominator is zero.
    """
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return "Cannot divide by zero."

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    watcher_thread = threading.Thread(target=file_watcher, daemon=True)
    watcher_thread.start()
    print(f"MCP Server started. Watching {current_file} for changes...")
    mcp.run(transport='sse')