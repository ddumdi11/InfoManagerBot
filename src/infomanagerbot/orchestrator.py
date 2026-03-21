from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from infomanagerbot.config.models import AppConfig, SourceModel, SourceType
from infomanagerbot.domain.models import RunInfo


@dataclass(slots=True)
class Orchestrator:
    config: AppConfig

    def prepare_run(self) -> RunInfo:
        return RunInfo(
            started_at=datetime.now(timezone.utc),
            source_count=len(self.config.sources),
            policy_count=len(self.config.policies),
            status="prepared",
        )

    def get_discovery_sources(self, source_type: SourceType | None = None) -> list[SourceModel]:
        sources = [source for source in self.config.sources if source.enabled]
        if source_type is not None:
            sources = [source for source in sources if source.type is source_type]
        return sources
