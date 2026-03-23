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
        self.connection.executescript(
            """
            CREATE TABLE artifacts (
                id INTEGER PRIMARY KEY,
                item_id INTEGER NOT NULL,
                artifact_type TEXT NOT NULL,
                storage_path TEXT NOT NULL,
                content_format TEXT,
                UNIQUE (item_id, artifact_type, storage_path)
            );
            """
        )
        self.repository = ArtifactRepository(self.connection)

    def tearDown(self) -> None:
        self.connection.close()

    def test_create_and_exists(self) -> None:
        artifact_id = self.repository.create_artifact(
            item_id=1,
            artifact_type="metadata",
            storage_path="output/rss/example/metadata.json",
            content_format="json",
        )

        self.assertGreater(artifact_id, 0)
        self.assertTrue(self.repository.exists(item_id=1, artifact_type="metadata"))
        self.assertFalse(self.repository.exists(item_id=1, artifact_type="content"))


if __name__ == "__main__":
    unittest.main()
