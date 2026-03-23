from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import logging

from infomanagerbot.archive.writer import ArchiveWriter
from infomanagerbot.adapters.registry import get_adapter_for_source
from infomanagerbot.config.models import AppConfig, SourceModel, SourceType
from infomanagerbot.domain.models import DiscoveredItem
from infomanagerbot.domain.models import RunInfo
from infomanagerbot.persistence.repositories import ArtifactRepository, ItemRepository, SourceRepository

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class Orchestrator:
    config: AppConfig

    def prepare_run(self) -> RunInfo:
        return RunInfo(
            started_at=datetime.now(timezone.utc),
            source_count=len(self.get_discovery_sources()),
            policy_count=len(self.config.policies),
            status="prepared",
        )

    def get_discovery_sources(self, source_type: SourceType | None = None) -> list[SourceModel]:
        sources = [source for source in self.config.sources if source.enabled]
        if source_type is not None:
            sources = [source for source in sources if source.type is source_type]
        return sources

    def discover_for_source(self, source: SourceModel) -> list[DiscoveredItem]:
        adapter = get_adapter_for_source(source)
        return adapter.discover(source)

    def execute_discovery(
        self,
        source_repository: SourceRepository,
        item_repository: ItemRepository,
        run_id: int,
    ) -> RunInfo:
        run_info = self.prepare_run()

        for source in self.get_discovery_sources():
            source_id = source_repository.get_db_id_by_key(source.id)
            if source_id is None:
                LOGGER.error("Quelle fuer Discovery nicht in der Datenbank gefunden: %s", source.id)
                run_info.error_count += 1
                continue

            try:
                discovered_items = self.discover_for_source(source)
            except Exception:
                LOGGER.exception("Discovery fuer Quelle fehlgeschlagen: %s", source.id)
                run_info.error_count += 1
                continue

            run_info.processed_source_count += 1
            run_info.discovered_item_count += len(discovered_items)

            for item in discovered_items:
                try:
                    if item_repository.exists(source_id=source_id, external_id=item.external_id):
                        run_info.known_item_count += 1
                        continue

                    item_repository.create_discovered_item(
                        source_id=source_id,
                        item=item,
                        run_id=run_id,
                    )
                    run_info.new_item_count += 1
                except Exception:
                    LOGGER.exception(
                        "Persistenz fuer entdecktes Item fehlgeschlagen: source=%s external_id=%s",
                        source.id,
                        item.external_id,
                    )
                    run_info.error_count += 1

        if run_info.error_count:
            run_info.status = "completed_with_errors"
        else:
            run_info.status = "completed"

        run_info.notes = (
            f"processed_sources={run_info.processed_source_count}, "
            f"new_items={run_info.new_item_count}, "
            f"known_items={run_info.known_item_count}, "
            f"errors={run_info.error_count}"
        )
        return run_info

    def execute_archiving(
        self,
        item_repository: ItemRepository,
        artifact_repository: ArtifactRepository,
        archive_writer: ArchiveWriter,
        run_info: RunInfo,
    ) -> RunInfo:
        for item in item_repository.list_items_for_archiving():
            try:
                artifact_paths = archive_writer.write_item(item)

                if not artifact_repository.exists(item.item_id, "metadata"):
                    artifact_repository.create_artifact(
                        item_id=item.item_id,
                        artifact_type="metadata",
                        storage_path=str(artifact_paths["metadata"]),
                        content_format="json",
                    )
                if not artifact_repository.exists(item.item_id, "content"):
                    artifact_repository.create_artifact(
                        item_id=item.item_id,
                        artifact_type="content",
                        storage_path=str(artifact_paths["content"]),
                        content_format="markdown",
                    )

                item_repository.mark_as_archived(item.item_id)
                run_info.archived_item_count += 1
            except Exception:
                LOGGER.exception("Archivierung fuer Item fehlgeschlagen: item_id=%s", item.item_id)
                run_info.error_count += 1

        if run_info.error_count:
            run_info.status = "completed_with_errors"
        else:
            run_info.status = "completed"

        run_info.notes = (
            f"processed_sources={run_info.processed_source_count}, "
            f"new_items={run_info.new_item_count}, "
            f"known_items={run_info.known_item_count}, "
            f"archived_items={run_info.archived_item_count}, "
            f"errors={run_info.error_count}"
        )
        return run_info
