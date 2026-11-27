from __future__ import annotations

from fastmcp import FastMCP

from laserchicken.mcp.tools import (
    generate_example_workflow,
    get_example_workflow_questions,
)


def create_server() -> FastMCP:
    server = FastMCP(name="laserchicken-example-workflow")
    server.tool(name="get_example_workflow_questions")(get_example_workflow_questions)
    server.tool(name="generate_example_workflow")(generate_example_workflow)
    return server


mcp = create_server()


def main() -> None:
    mcp.run()
