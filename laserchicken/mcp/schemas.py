from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class LoadStepInput:
    path: str
    format: str | None = None


@dataclass
class NormalizationStepInput:
    cell_size: float | None = None


@dataclass
class FilterStepInput:
    polygon_wkt: str
    height_threshold: float


@dataclass
class VolumeInput:
    volume_type: str
    radius: float | None = None
    side_length: float | None = None


@dataclass
class FeatureStepInput:
    feature_names: list[str]
    volume: VolumeInput
    target: str = "points_above_threshold"
    sample_size: int | None = None


@dataclass
class SaveStepInput:
    path: str
    format: str | None = None
    overwrite: bool = False


@dataclass
class ExampleWorkflowRequest:
    load: LoadStepInput
    normalize: NormalizationStepInput
    filter: FilterStepInput
    features: FeatureStepInput
    save: SaveStepInput

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> ExampleWorkflowRequest:
        load = LoadStepInput(**payload["load"])
        normalize = NormalizationStepInput(**payload["normalize"])
        filter_step = FilterStepInput(**payload["filter"])
        features = FeatureStepInput(
            feature_names=payload["features"]["feature_names"],
            volume=VolumeInput(**payload["features"]["volume"]),
            target=payload["features"].get("target", "points_above_threshold"),
            sample_size=payload["features"].get("sample_size"),
        )
        save = SaveStepInput(**payload["save"])
        return cls(
            load=load,
            normalize=normalize,
            filter=filter_step,
            features=features,
            save=save,
        )
