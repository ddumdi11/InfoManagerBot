from __future__ import annotations

import sqlite3
from pathlib import Path


def resolve_database_path(database_path: str | Path) -> Path:
    path = Path(database_path)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def create_connection(database_path: str | Path) -> sqlite3.Connection:
    path = resolve_database_path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    connection.execute("PRAGMA journal_mode = WAL;")
    return connection
