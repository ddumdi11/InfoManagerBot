from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from infomanagerbot.adapters.rss import build_external_id, map_entry_to_item
from infomanagerbot.config.models import SourceModel, SourceType


class RssAdapterTests(unittest.TestCase):
    def test_build_external_id_uses_stable_fallback_hash(self) -> None:
        entry = {
            "title": "Example entry",
            "summary": "Summary text",
            "published": "Sat, 21 Mar 2026 10:00:00 GMT",
        }

        first_id = build_external_id("example-rss", entry)
        second_id = build_external_id("example-rss", entry)

        self.assertEqual(first_id, second_id)
        self.assertTrue(first_id.startswith("rss-fallback:"))

    def test_map_entry_prefers_link_as_external_id_when_no_feed_id_exists(self) -> None:
        source = SourceModel(
            id="example-rss",
            type=SourceType.RSS_ATOM,
            display_name="Example RSS",
            locator="https://example.invalid/feed.xml",
            enabled=True,
        )
        entry = {
            "title": "Example entry",
            "link": "https://example.invalid/articles/1",
            "summary": "Summary text",
        }

        item = map_entry_to_item(source, entry)

        self.assertEqual(item.source_key, "example-rss")
        self.assertEqual(item.external_id, "https://example.invalid/articles/1")
        self.assertEqual(item.title, "Example entry")
        self.assertEqual(item.content_text, "Summary text")


if __name__ == "__main__":
    unittest.main()
