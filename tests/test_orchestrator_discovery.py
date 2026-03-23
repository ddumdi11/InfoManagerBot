from __future__ import annotations

import sqlite3
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from infomanagerbot.config.models import AppConfig, SettingsModel, SourceModel, SourceType
from infomanagerbot.domain.models import DiscoveredItem
from infomanagerbot.orchestrator import Orchestrator
from infomanagerbot.persistence.repositories import ItemRepository, SourceRepository


class _FakeAdapter:
    def __init__(self, items: list[DiscoveredItem]) -> None:
        self._items = items

    def discover(self, source: SourceModel) -> list[DiscoveredItem]:
        return list(self._items)


class OrchestratorDiscoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        self.connection.executescript(
            """
            CREATE TABLE sources (
                id INTEGER PRIMARY KEY,
                source_key TEXT NOT NULL UNIQUE,
                source_type TEXT NOT NULL,
                enabled INTEGER NOT NULL,
                display_name TEXT NOT NULL,
                locator TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT
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
                UNIQUE (source_id, external_id)
            );
            """
        )
        self.source = SourceModel(
            id="example-rss",
            type=SourceType.RSS_ATOM,
            enabled=True,
            display_name="Example RSS",
            locator="https://example.invalid/feed.xml",
        )
        self.config = AppConfig(
            settings=SettingsModel(),
            policies=[],
            sources=[self.source],
        )
        self.source_repository = SourceRepository(self.connection)
        self.source_repository.sync([self.source])
        self.item_repository = ItemRepository(self.connection)

    def tearDown(self) -> None:
        self.connection.close()

    def test_execute_discovery_counts_known_items(self) -> None:
        item = DiscoveredItem(
            source_key="example-rss",
            external_id="entry-1",
            title="Example entry",
        )
        source_id = self.source_repository.get_db_id_by_key("example-rss")
        assert source_id is not None
        self.item_repository.create_discovered_item(source_id=source_id, item=item, run_id=1)

        orchestrator = Orchestrator(config=self.config)
        with patch("infomanagerbot.orchestrator.get_adapter_for_source", return_value=_FakeAdapter([item])):
            run_info = orchestrator.execute_discovery(
                source_repository=self.source_repository,
                item_repository=self.item_repository,
                run_id=2,
            )

        self.assertEqual(run_info.new_item_count, 0)
        self.assertEqual(run_info.known_item_count, 1)
        self.assertEqual(run_info.error_count, 0)
        self.assertEqual(run_info.status, "completed")


if __name__ == "__main__":
    unittest.main()
