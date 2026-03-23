from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from infomanagerbot.adapters.youtube import build_external_id, build_feed_url, map_entry_to_item
from infomanagerbot.config.models import SourceModel, SourceType


class YouTubeAdapterTests(unittest.TestCase):
    def test_build_feed_url_accepts_channel_id(self) -> None:
        self.assertEqual(
            build_feed_url("UC0000000000000000000000"),
            "https://www.youtube.com/feeds/videos.xml?channel_id=UC0000000000000000000000",
        )

    def test_map_entry_uses_video_id_as_external_id(self) -> None:
        source = SourceModel(
            id="example-youtube",
            type=SourceType.YOUTUBE_CHANNEL,
            display_name="Example YouTube",
            locator="UC0000000000000000000000",
            enabled=True,
        )
        entry = {
            "yt_videoid": "video-123",
            "title": "Example video",
            "link": "https://www.youtube.com/watch?v=video-123",
            "summary": "Short description",
        }

        item = map_entry_to_item(source, entry)

        self.assertEqual(item.source_key, "example-youtube")
        self.assertEqual(item.external_id, "video-123")
        self.assertEqual(item.content_text, "Short description")

    def test_build_external_id_falls_back_to_link(self) -> None:
        entry = {
            "title": "Example video",
            "link": "https://www.youtube.com/watch?v=video-123",
        }

        self.assertEqual(
            build_external_id("example-youtube", entry),
            "https://www.youtube.com/watch?v=video-123",
        )


if __name__ == "__main__":
    unittest.main()
