from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Migration:
    version: str
    path: Path


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


def load_migrations(migrations_dir: Path) -> list[Migration]:
    migrations: list[Migration] = []
    for path in sorted(migrations_dir.glob("*.sql")):
        migrations.append(Migration(version=path.stem, path=path))
    return migrations


def apply_migrations(connection: sqlite3.Connection, migrations_dir: Path | None = None) -> list[str]:
    target_dir = migrations_dir or Path("migrations")
    applied_versions: list[str] = []
    for migration in load_migrations(target_dir):
        if apply_migration(connection, migration):
            applied_versions.append(migration.version)
    return applied_versions
