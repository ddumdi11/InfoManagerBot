from __future__ import annotations

from hashlib import sha256
from typing import Any, Mapping

import feedparser

from infomanagerbot.adapters.base import AdapterError, DiscoveryAdapter
from infomanagerbot.adapters.feed_common import (
    coerce_text,
    extract_content_text,
    parse_published_at,
)
from infomanagerbot.config.models import SourceModel, SourceType
from infomanagerbot.domain.models import DiscoveredItem

YOUTUBE_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
YOUTUBE_CHANNEL_URL_PREFIX = "https://www.youtube.com/channel/"


def build_feed_url(locator: str) -> str:
    value = locator.strip()
    if not value:
        raise AdapterError("YouTube-Quelle hat keinen gueltigen Locator.")

    if "feeds/videos.xml?channel_id=" in value:
        return value

    if value.startswith(YOUTUBE_CHANNEL_URL_PREFIX):
        channel_id = value.removeprefix(YOUTUBE_CHANNEL_URL_PREFIX).strip("/")
        if channel_id:
            return YOUTUBE_FEED_URL.format(channel_id=channel_id)

    if value.startswith("UC"):
        return YOUTUBE_FEED_URL.format(channel_id=value)

    raise AdapterError(
        "YouTube-Locator muss ein Channel-Feed, eine Channel-URL oder eine Channel-ID sein."
    )


def build_external_id(source_key: str, entry: Mapping[str, Any]) -> str:
    video_id = coerce_text(entry.get("yt_videoid"))
    if video_id:
        return video_id

    entry_id = coerce_text(entry.get("id"))
    if entry_id:
        if entry_id.startswith("yt:video:"):
            return entry_id.removeprefix("yt:video:")
        return entry_id

    link = coerce_text(entry.get("link"))
    if link:
        return link

    fallback_parts = [
        source_key,
        coerce_text(entry.get("title")) or "",
        coerce_text(entry.get("published")) or coerce_text(entry.get("updated")) or "",
        extract_content_text(entry) or "",
    ]
    digest = sha256("||".join(fallback_parts).encode("utf-8")).hexdigest()
    return f"youtube-fallback:{digest}"


def map_entry_to_item(source: SourceModel, entry: Mapping[str, Any]) -> DiscoveredItem:
    title = coerce_text(entry.get("title")) or "(ohne Titel)"
    return DiscoveredItem(
        source_key=source.id,
        external_id=build_external_id(source.id, entry),
        title=title,
        url=coerce_text(entry.get("link")),
        published_at=parse_published_at(entry),
        content_text=extract_content_text(entry),
    )


class YouTubeChannelAdapter(DiscoveryAdapter):
    def __init__(self) -> None:
        super().__init__(source_type=SourceType.YOUTUBE_CHANNEL)

    def discover(self, source: SourceModel) -> list[DiscoveredItem]:
        if source.type is not SourceType.YOUTUBE_CHANNEL:
            raise AdapterError(f"YouTube-Adapter kann Source-Typ nicht verarbeiten: {source.type}")

        feed = feedparser.parse(build_feed_url(source.locator))
        if getattr(feed, "bozo", False):
            detail = getattr(feed, "bozo_exception", "Unbekannter Feed-Fehler")
            raise AdapterError(f"YouTube-Feed konnte nicht verarbeitet werden: {detail}")

        entries = getattr(feed, "entries", [])
        return [map_entry_to_item(source, entry) for entry in entries]
