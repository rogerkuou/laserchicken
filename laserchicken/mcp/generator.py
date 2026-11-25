from __future__ import annotations

from importlib import resources

from laserchicken.mcp.schemas import ExampleWorkflowRequest


def generate_example_workflow_script(request: ExampleWorkflowRequest) -> str:
    template = _load_template()
    volume_param_name, volume_param_value = _volume_parameter_pair(request)

    rendered = template.format(
        load_path=repr(request.load.path),
        load_format_arg=_optional_keyword("format", request.load.format),
        normalize_call=_normalize_call(request),
        polygon_wkt=repr(request.filter.polygon_wkt),
        height_threshold=repr(request.filter.height_threshold),
        feature_target=request.features.target,
        volume_type=repr(request.features.volume.volume_type),
        volume_parameter_name=volume_param_name,
        volume_parameter_value=repr(volume_param_value),
        sample_size_arg=_optional_keyword("sample_size", request.features.sample_size),
        feature_names=repr(request.features.feature_names),
        save_path=repr(request.save.path),
        save_format_arg=_optional_keyword("format", request.save.format),
        overwrite=repr(request.save.overwrite),
    )

    return rendered


def _normalize_call(request: ExampleWorkflowRequest) -> str:
    if request.normalize.cell_size is None:
        return "lc.normalize(point_cloud)"
    return f"lc.normalize(point_cloud, cell_size={request.normalize.cell_size!r})"


def _volume_parameter_pair(request: ExampleWorkflowRequest) -> tuple[str, float | None]:
    volume_type = request.features.volume.volume_type.lower()
    if volume_type in {"sphere", "infinite cylinder"}:
        return "radius", request.features.volume.radius
    return "side_length", request.features.volume.side_length


def _optional_keyword(name: str, value: object | None) -> str:
    if value is None:
        return ""
    return f", {name}={value!r}"


def _load_template() -> str:
    template_path = resources.files("laserchicken.mcp").joinpath("templates/example_workflow.py.j2")
    return template_path.read_text(encoding="utf-8")
