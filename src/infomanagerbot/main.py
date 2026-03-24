from __future__ import annotations

import argparse
import logging
from pathlib import Path

from infomanagerbot.config.loader import load_app_config
from infomanagerbot.logging_config import setup_logging
from infomanagerbot.orchestrator import Orchestrator
from infomanagerbot.archive.writer import ArchiveWriter
from infomanagerbot.persistence.connection import create_connection, resolve_database_path
from infomanagerbot.persistence.repositories import (
    ArtifactRepository,
    ItemRepository,
    PolicyRepository,
    RunRepository,
    SourceRepository,
)
from infomanagerbot.persistence.schema import apply_migrations

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="infomanagerbot",
        description="Startet das minimale MVP-Grundgeruest von InfoManagerBot.",
    )
    parser.add_argument(
        "--settings",
        type=Path,
        default=Path("config/settings.example.yaml"),
        help="Pfad zur Settings-Konfiguration.",
    )
    parser.add_argument(
        "--policies",
        type=Path,
        default=Path("config/policies.example.yaml"),
        help="Pfad zur Policy-Konfiguration.",
    )
    parser.add_argument(
        "--sources",
        type=Path,
        default=Path("config/sources.example.yaml"),
        help="Pfad zur Source-Konfiguration.",
    )
    parser.add_argument(
        "--migrations-dir",
        type=Path,
        default=Path("migrations"),
        help="Pfad zum Verzeichnis mit SQL-Migrationen.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    bootstrap_logging_level = "INFO"
    setup_logging(log_level=bootstrap_logging_level)
    LOGGER.info("Projektgrundgeruest wird initialisiert.")

    app_config = load_app_config(
        settings_path=args.settings,
        policies_path=args.policies,
        sources_path=args.sources,
    )

    setup_logging(log_level=app_config.settings.log_level)
    LOGGER.info("Konfiguration erfolgreich geprueft.")

    database_path = resolve_database_path(app_config.settings.database_path)
    archive_root = Path("output").resolve()
    with create_connection(database_path) as connection:
        applied_migrations = apply_migrations(
            connection=connection,
            migrations_dir=args.migrations_dir,
        )
        source_repository = SourceRepository(connection)
        item_repository = ItemRepository(connection)
        artifact_repository = ArtifactRepository(connection)
        source_repository.sync(app_config.sources)
        PolicyRepository(connection).sync(app_config.policies)

        run_repository = RunRepository(connection)
        run_id = run_repository.create_run(status="prepared")

        orchestrator = Orchestrator(config=app_config)
        run_info = orchestrator.execute_discovery(
            source_repository=source_repository,
            item_repository=item_repository,
            run_id=run_id,
        )
        run_info = orchestrator.execute_archiving(
            item_repository=item_repository,
            artifact_repository=artifact_repository,
            archive_writer=ArchiveWriter(output_dir=archive_root),
            run_info=run_info,
        )
        run_repository.finish_run(
            run_id=run_id,
            status=run_info.status,
            notes=run_info.notes,
        )

    LOGGER.info(
        "Discovery- und Archivierungs-Lauf abgeschlossen: status=%s new=%s known=%s archived=%s errors=%s",
        run_info.status,
        run_info.new_item_count,
        run_info.known_item_count,
        run_info.archived_item_count,
        run_info.error_count,
    )

    print("Projektgrundgeruest geladen.")
    print("Konfiguration erfolgreich geprueft.")
    print(
        "Persistenzbasis vorbereitet. "
        f"Datenbank: {database_path} | Migrationen: {', '.join(applied_migrations) if applied_migrations else 'keine neuen'}."
    )
    print(
        "Discovery, Item-Persistenz und erste Archivierung wurden ausgefuehrt. "
        f"Neue Items: {run_info.new_item_count}, bekannte Items: {run_info.known_item_count}, Fehler: {run_info.error_count}."
    )
    print(
        "Archivartefakte wurden fuer neu verarbeitete Items geschrieben. "
        f"Archivierte Items: {run_info.archived_item_count}, aktive Quellen: {run_info.source_count}, verarbeitete Quellen: {run_info.processed_source_count}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
