from typing import Literal
import os
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters


def add_subtract(
    first_operand: float,
    second_operand: float,
    operation: Literal["add", "subtract"] = "add",
) -> dict:
    """
    Performs addition or subtraction operations on two numbers.

    Args:
        first_operand (float): The first number for the calculation.
        second_operand (float): The second number for the calculation.
        operation (Literal["add", "subtract"], optional): The operation to perform.
            Defaults to "add".

    Returns:
        dict: A dictionary with 'operation' (str) and 'result' (float) keys.
    """

    if operation == "add":
        result = first_operand + second_operand
    elif operation == "subtract":
        result = first_operand - second_operand
    else:
        raise ValueError("operation must be either 'add' or 'subtract'")

    return {"operation": operation, "result": result}


def multiply_divide(
    first_operand: float,
    second_operand: float,
    operation: Literal["multiply", "divide"] = "multiply",
) -> dict:
    """
    Performs multiplication or division operations on two numbers.

    Args:
        first_operand (float): The first number for the calculation.
        second_operand (float): The second number for the calculation.
        operation (Literal["multiply", "divide"], optional): The operation to perform.
            Defaults to "multiply".

    Returns:
        dict: A dictionary with 'operation' (str) and 'result' (float) keys.

    Raises:
        ValueError: When the operation is invalid or division by zero is attempted.
    """

    if operation == "multiply":
        result = first_operand * second_operand
    elif operation == "divide":
        if second_operand == 0:
            raise ValueError("division by zero is not allowed")
        result = first_operand / second_operand
    else:
        raise ValueError("operation must be either 'multiply' or 'divide'")

    return {"operation": operation, "result": result}


def create_filesystem_mcp_toolset():
    """
    Creates an MCP toolset for basic filesystem operations.

    Returns:
        MCPToolset: Filesystem MCP toolset rooted at the current directory.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))

    return MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    current_directory,
                ],
            )
        )
    )
