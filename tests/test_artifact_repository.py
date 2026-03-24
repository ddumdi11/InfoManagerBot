from __future__ import annotations

import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from infomanagerbot.persistence.repositories import ArtifactRepository


class ArtifactRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript(
            """
            CREATE TABLE sources (
                id INTEGER PRIMARY KEY,
                source_key TEXT NOT NULL UNIQUE,
                source_type TEXT NOT NULL,
                enabled INTEGER NOT NULL DEFAULT 1,
                display_name TEXT NOT NULL,
                locator TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE runs (
                id INTEGER PRIMARY KEY,
                started_at TEXT NOT NULL,
                finished_at TEXT,
                status TEXT NOT NULL,
                notes TEXT
            );
            CREATE TABLE items (
                id INTEGER PRIMARY KEY,
                source_id INTEGER NOT NULL,
                run_id INTEGER,
                external_id TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT,
                discovered_at TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL DEFAULT 'discovered',
                published_at TEXT,
                content_text TEXT,
                FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE,
                FOREIGN KEY (run_id) REFERENCES runs(id) ON DELETE SET NULL,
                UNIQUE (source_id, external_id)
            );
            CREATE TABLE artifacts (
                id INTEGER PRIMARY KEY,
                item_id INTEGER NOT NULL,
                artifact_type TEXT NOT NULL,
                storage_path TEXT NOT NULL,
                content_format TEXT,
                FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
                UNIQUE (item_id, artifact_type, storage_path)
            );
            INSERT INTO sources (
                id, source_key, source_type, enabled, display_name, locator
            ) VALUES (
                1, 'example-rss', 'rss_atom', 1, 'Example RSS', 'https://example.invalid/feed.xml'
            );
            INSERT INTO runs(id, started_at, status) VALUES (1, '2026-03-24T10:00:00+00:00', 'prepared');
            INSERT INTO items (
                id, source_id, run_id, external_id, title, url, discovered_at, status
            ) VALUES (
                1, 1, 1, 'entry-1', 'Example Entry', 'https://example.invalid/1',
                '2026-03-24T10:05:00+00:00', 'discovered'
            );
            """
        )
        self.repository = ArtifactRepository(self.connection)

    def tearDown(self) -> None:
        self.connection.close()

    def test_create_if_missing_is_atomic(self) -> None:
        created = self.repository.create_artifact_if_missing(
            item_id=1,
            artifact_type="metadata",
            storage_path="output/rss/example/metadata.json",
            content_format="json",
        )
        created_again = self.repository.create_artifact_if_missing(
            item_id=1,
            artifact_type="metadata",
            storage_path="output/rss/example/metadata.json",
            content_format="json",
        )
        count = self.connection.execute("SELECT COUNT(*) AS count FROM artifacts").fetchone()["count"]

        self.assertTrue(created)
        self.assertFalse(created_again)
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
