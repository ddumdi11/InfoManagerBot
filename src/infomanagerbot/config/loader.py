from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

from infomanagerbot.config.models import (
    AppConfig,
    PoliciesFileModel,
    SettingsFileModel,
    SourcesFileModel,
)


def _load_yaml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {path}")

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Konfigurationsdatei muss ein YAML-Objekt enthalten: {path}")

    return data


def _validate_config_section(
    path: Path,
    label: str,
    model_class: type[BaseModel],
) -> BaseModel:
    try:
        return model_class.model_validate(_load_yaml_file(path))
    except ValidationError as error:
        raise ValueError(f"Ungueltige {label}-Konfiguration in {path}: {error}") from error


def load_app_config(
    settings_path: Path,
    policies_path: Path,
    sources_path: Path,
) -> AppConfig:
    settings = _validate_config_section(settings_path, "Settings", SettingsFileModel)
    policies = _validate_config_section(policies_path, "Policies", PoliciesFileModel)
    sources = _validate_config_section(sources_path, "Sources", SourcesFileModel)

    return AppConfig(
        settings=settings.settings,
        policies=policies.policies,
        sources=sources.sources,
    )
