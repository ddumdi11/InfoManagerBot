from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from infomanagerbot.archive.writer import ArchiveWriter, build_archive_directory
from infomanagerbot.domain.models import PersistedItem


class ArchiveWriterTests(unittest.TestCase):
    def test_build_archive_directory_uses_stable_structure(self) -> None:
        item = PersistedItem(
            item_id=1,
            source_id=10,
            source_key="example-rss",
            source_type="rss_atom",
            external_id="entry-123",
            title="Example Entry",
            url="https://example.invalid/1",
            discovered_at="2026-03-23T10:00:00+00:00",
            published_at="2026-03-22T09:00:00+00:00",
            run_id=5,
            status="discovered",
            content_text="Hello world",
        )

        archive_dir = build_archive_directory(Path("output"), item)

        self.assertEqual(
            archive_dir.as_posix(),
            "output/rss_atom/example-rss/2026-03-22_75ed6784_example-entry",
        )

    def test_write_item_creates_metadata_and_content(self) -> None:
        item = PersistedItem(
            item_id=1,
            source_id=10,
            source_key="example-rss",
            source_type="rss_atom",
            external_id="entry-123",
            title="Example Entry",
            url="https://example.invalid/1",
            discovered_at="2026-03-23T10:00:00+00:00",
            published_at=None,
            run_id=5,
            status="discovered",
            content_text="Hello world",
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            writer = ArchiveWriter(output_dir=Path(tmp_dir))
            result = writer.write_item(item)

            metadata = json.loads(result["metadata"].read_text(encoding="utf-8"))
            content = result["content"].read_text(encoding="utf-8")

            self.assertEqual(metadata["item_id"], 1)
            self.assertEqual(metadata["source_key"], "example-rss")
            self.assertIn("# Example Entry", content)
            self.assertIn("Hello world", content)


if __name__ == "__main__":
    unittest.main()
