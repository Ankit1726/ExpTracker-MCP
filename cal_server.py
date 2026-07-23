from fastmcp import FastMCP

mcp = FastMCP("Math Server")


@mcp.tool()
def add(a: float, b: float):
    """Add two numbers."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float):
    """Subtract two numbers."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float):
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def divide(a: float, b: float):
    """Divide two numbers."""
    if b == 0:
        return {"error": "Division by zero"}
    return a / b


if __name__ == "__main__":
    mcp.run(transport="http")
