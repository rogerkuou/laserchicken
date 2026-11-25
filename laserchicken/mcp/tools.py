from __future__ import annotations

import json
from importlib import resources
from typing import Any

from laserchicken.mcp.generator import generate_example_workflow_script
from laserchicken.mcp.schemas import ExampleWorkflowRequest


def get_example_workflow_questions() -> dict[str, Any]:
    """Return the prompt schema/questions for collecting workflow inputs."""
    questions_path = resources.files("laserchicken.mcp").joinpath("questions.json")
    return json.loads(questions_path.read_text(encoding="utf-8"))


def generate_example_workflow(payload: dict[str, Any]) -> dict[str, str]:
    """Generate Python workflow content from structured step inputs."""
    request = ExampleWorkflowRequest.from_dict(payload)
    script = generate_example_workflow_script(request)
    return {"script": script}
