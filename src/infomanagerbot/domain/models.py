from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Source:
    id: str
    source_type: str
    display_name: str
    locator: str
    enabled: bool = True


@dataclass(slots=True)
class Policy:
    id: str
    enabled: bool = True
    match_source_ids: list[str] = field(default_factory=list)
    archive_format: str = "markdown"


@dataclass(slots=True)
class DiscoveredItem:
    source_key: str
    external_id: str
    title: str
    url: str | None = None
    published_at: datetime | None = None
    content_text: str | None = None


@dataclass(slots=True)
class RunInfo:
    started_at: datetime
    source_count: int
    policy_count: int
    status: str
