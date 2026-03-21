from __future__ import annotations

import argparse
import logging
from pathlib import Path

from infomanagerbot.config.loader import load_app_config
from infomanagerbot.logging_config import setup_logging
from infomanagerbot.orchestrator import Orchestrator
from infomanagerbot.persistence.connection import create_connection, resolve_database_path
from infomanagerbot.persistence.repositories import (
    PolicyRepository,
    RunRepository,
    SourceRepository,
)
from infomanagerbot.persistence.schema import apply_initial_schema

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
    with create_connection(database_path) as connection:
        schema_changed = apply_initial_schema(
            connection=connection,
            migrations_dir=args.migrations_dir,
        )
        SourceRepository(connection).sync(app_config.sources)
        PolicyRepository(connection).sync(app_config.policies)

        run_repository = RunRepository(connection)
        run_id = run_repository.create_run(status="prepared")

        orchestrator = Orchestrator(config=app_config)
        run_info = orchestrator.prepare_run()
        run_repository.finish_run(
            run_id=run_id,
            status="prepared",
            notes="Konfiguration und Persistenzbasis vorbereitet.",
        )

    LOGGER.info("Persistenzbasis vorbereitet.")

    print("Projektgrundgeruest geladen.")
    print("Konfiguration erfolgreich geprueft.")
    print(
        "Persistenzbasis vorbereitet. "
        f"Datenbank: {database_path} | Schema angewendet: {'ja' if schema_changed else 'bereits vorhanden'}."
    )
    print(
        "Weitere Implementierung folgt. "
        f"Quellen: {run_info.source_count}, Policies: {run_info.policy_count}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
