from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class SourceType(str, Enum):
    RSS_ATOM = "rss_atom"
    YOUTUBE_CHANNEL = "youtube_channel"


class SettingsModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    app_name: str = "InfoManagerBot"
    log_level: str = "INFO"
    environment: str = "local"
    database_path: str = "data/infomanagerbot.sqlite3"


class PolicyModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    enabled: bool = True
    match_source_ids: list[str] = Field(default_factory=list)
    archive_format: str = "markdown"


class SourceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: SourceType
    enabled: bool = True
    display_name: str
    locator: str


class SettingsFileModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    settings: SettingsModel


class PoliciesFileModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    policies: list[PolicyModel] = Field(default_factory=list)


class SourcesFileModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sources: list[SourceModel] = Field(default_factory=list)


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    settings: SettingsModel
    policies: list[PolicyModel] = Field(default_factory=list)
    sources: list[SourceModel] = Field(default_factory=list)
