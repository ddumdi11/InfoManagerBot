from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Migration:
    version: str
    path: Path


INITIAL_MIGRATION = Migration(
    version="001_initial_schema",
    path=Path("migrations/001_initial_schema.sql"),
)


def ensure_schema_migrations_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL
        )
        """
    )
    connection.commit()


def is_migration_applied(connection: sqlite3.Connection, version: str) -> bool:
    ensure_schema_migrations_table(connection)
    row = connection.execute(
        "SELECT 1 FROM schema_migrations WHERE version = ?",
        (version,),
    ).fetchone()
    return row is not None


def apply_migration(connection: sqlite3.Connection, migration: Migration) -> bool:
    ensure_schema_migrations_table(connection)
    if is_migration_applied(connection, migration.version):
        return False

    sql = migration.path.read_text(encoding="utf-8")
    connection.executescript(sql)
    connection.execute(
        "INSERT INTO schema_migrations(version, applied_at) VALUES (?, ?)",
        (migration.version, datetime.now(timezone.utc).isoformat()),
    )
    connection.commit()
    return True


def apply_initial_schema(connection: sqlite3.Connection, migrations_dir: Path | None = None) -> bool:
    migration = INITIAL_MIGRATION
    if migrations_dir is not None:
        migration = Migration(
            version=INITIAL_MIGRATION.version,
            path=migrations_dir / INITIAL_MIGRATION.path.name,
        )
    return apply_migration(connection, migration)
