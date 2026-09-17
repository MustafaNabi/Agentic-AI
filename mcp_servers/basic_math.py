from fastmcp import FastMCP

mcp = FastMCP("Basic Math MCP Server")

@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers and returns the result"""
    return a + b

@mcp.tool
def subtract(a: float, b: float) -> float:
    """ Subtracts two numbers and returns the result"""
    return a - b

@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the result"""
    return a * b


@mcp.tool
def divide(a: float, b: float) -> float:
    """
    Divides two numbes and returns the result
    """
    try:
        return a / b
    except ZeroDivisionError:
        return f"Error: Division by zero, b = {b}"


@mcp.tool
def square(a: float) -> float:
    """Returns square of a number"""
    return a * a


if __name__ == "__main__":
    mcp.run()
    
