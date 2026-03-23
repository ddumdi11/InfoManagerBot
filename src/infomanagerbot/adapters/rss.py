from __future__ import annotations

import logging
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

LOGGER = logging.getLogger(__name__)


def build_external_id(source_key: str, entry: Mapping[str, Any]) -> str:
    entry_id = coerce_text(entry.get("id")) or coerce_text(entry.get("guid"))
    if entry_id:
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
    return f"rss-fallback:{digest}"


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


class RssAtomAdapter(DiscoveryAdapter):
    def __init__(self) -> None:
        super().__init__(source_type=SourceType.RSS_ATOM)

    def discover(self, source: SourceModel) -> list[DiscoveredItem]:
        if source.type is not SourceType.RSS_ATOM:
            raise AdapterError(f"RSS-Adapter kann Source-Typ nicht verarbeiten: {source.type}")

        feed = feedparser.parse(source.locator)
        entries = getattr(feed, "entries", [])
        if getattr(feed, "bozo", False):
            detail = getattr(feed, "bozo_exception", "Unbekannter Feed-Fehler")
            LOGGER.warning(
                "RSS-Feed mit Parser-Warnung geladen: source=%s detail=%s",
                source.id,
                detail,
            )
            if not entries:
                raise AdapterError(f"Feed konnte nicht brauchbar verarbeitet werden: {detail}")

        return [map_entry_to_item(source, entry) for entry in entries]
