from __future__ import annotations

import sqlite3
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from infomanagerbot.domain.models import DiscoveredItem
from infomanagerbot.persistence.repositories import ItemRepository


class ItemRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(
            """
            CREATE TABLE sources (
                id INTEGER PRIMARY KEY,
                source_key TEXT NOT NULL UNIQUE
            );
            CREATE TABLE items (
                id INTEGER PRIMARY KEY,
                source_id INTEGER NOT NULL,
                run_id INTEGER,
                external_id TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT,
                status TEXT NOT NULL,
                discovered_at TEXT NOT NULL,
                published_at TEXT,
                content_text TEXT,
                UNIQUE (source_id, external_id)
            );
            INSERT INTO sources(id, source_key) VALUES (1, 'example-rss');
            """
        )
        self.repository = ItemRepository(self.connection)

    def tearDown(self) -> None:
        self.connection.close()

    def test_create_discovered_item_persists_row(self) -> None:
        item = DiscoveredItem(
            source_key="example-rss",
            external_id="entry-1",
            title="Example entry",
            url="https://example.invalid/1",
            published_at=datetime(2026, 3, 21, 12, 0, tzinfo=timezone.utc),
        )

        item_id = self.repository.create_discovered_item(source_id=1, item=item, run_id=10)

        self.assertGreater(item_id, 0)
        row = self.connection.execute(
            "SELECT external_id, title, url, status, published_at, content_text FROM items WHERE id = ?",
            (item_id,),
        ).fetchone()
        self.assertEqual(row["external_id"], "entry-1")
        self.assertEqual(row["status"], "discovered")
        self.assertEqual(row["published_at"], "2026-03-21T12:00:00+00:00")
        self.assertIsNone(row["content_text"])

    def test_exists_detects_known_item(self) -> None:
        self.connection.execute(
            """
            INSERT INTO items (source_id, run_id, external_id, title, status, discovered_at)
            VALUES (1, 10, 'known-entry', 'Known', 'discovered', '2026-03-21T12:00:00+00:00')
            """
        )
        self.connection.commit()

        self.assertTrue(self.repository.exists(source_id=1, external_id="known-entry"))
        self.assertFalse(self.repository.exists(source_id=1, external_id="other-entry"))


if __name__ == "__main__":
    unittest.main()
