from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

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


def load_app_config(
    settings_path: Path,
    policies_path: Path,
    sources_path: Path,
) -> AppConfig:
    settings = SettingsFileModel.model_validate(_load_yaml_file(settings_path))
    policies = PoliciesFileModel.model_validate(_load_yaml_file(policies_path))
    sources = SourcesFileModel.model_validate(_load_yaml_file(sources_path))

    return AppConfig(
        settings=settings.settings,
        policies=policies.policies,
        sources=sources.sources,
    )
