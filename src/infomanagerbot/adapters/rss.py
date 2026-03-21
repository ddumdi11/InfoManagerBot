from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from time import struct_time
from typing import Any, Mapping

import feedparser

from infomanagerbot.adapters.base import AdapterError, DiscoveryAdapter
from infomanagerbot.config.models import SourceModel, SourceType
from infomanagerbot.domain.models import DiscoveredItem


def _coerce_text(value: Any) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return None


def _extract_content_text(entry: Mapping[str, Any]) -> str | None:
    content = entry.get("content")
    if isinstance(content, list) and content:
        first_part = content[0]
        if isinstance(first_part, Mapping):
            text = _coerce_text(first_part.get("value"))
            if text:
                return text
    return _coerce_text(entry.get("summary"))


def _parse_published_at(entry: Mapping[str, Any]) -> datetime | None:
    published_struct = entry.get("published_parsed") or entry.get("updated_parsed")
    if isinstance(published_struct, struct_time):
        return datetime(
            published_struct.tm_year,
            published_struct.tm_mon,
            published_struct.tm_mday,
            published_struct.tm_hour,
            published_struct.tm_min,
            published_struct.tm_sec,
            tzinfo=timezone.utc,
        )
    return None


def build_external_id(source_key: str, entry: Mapping[str, Any]) -> str:
    entry_id = _coerce_text(entry.get("id")) or _coerce_text(entry.get("guid"))
    if entry_id:
        return entry_id

    link = _coerce_text(entry.get("link"))
    if link:
        return link

    fallback_parts = [
        source_key,
        _coerce_text(entry.get("title")) or "",
        _coerce_text(entry.get("published")) or _coerce_text(entry.get("updated")) or "",
        _extract_content_text(entry) or "",
    ]
    digest = sha256("||".join(fallback_parts).encode("utf-8")).hexdigest()
    return f"rss-fallback:{digest}"


def map_entry_to_item(source: SourceModel, entry: Mapping[str, Any]) -> DiscoveredItem:
    title = _coerce_text(entry.get("title")) or "(ohne Titel)"
    return DiscoveredItem(
        source_key=source.id,
        external_id=build_external_id(source.id, entry),
        title=title,
        url=_coerce_text(entry.get("link")),
        published_at=_parse_published_at(entry),
        content_text=_extract_content_text(entry),
    )


class RssAtomAdapter(DiscoveryAdapter):
    def __init__(self) -> None:
        super().__init__(source_type=SourceType.RSS_ATOM.value)

    def discover(self, source: SourceModel) -> list[DiscoveredItem]:
        if source.type is not SourceType.RSS_ATOM:
            raise AdapterError(f"RSS-Adapter kann Source-Typ nicht verarbeiten: {source.type}")

        feed = feedparser.parse(source.locator)
        if getattr(feed, "bozo", False):
            detail = getattr(feed, "bozo_exception", "Unbekannter Feed-Fehler")
            raise AdapterError(f"Feed konnte nicht verarbeitet werden: {detail}")

        entries = getattr(feed, "entries", [])
        return [map_entry_to_item(source, entry) for entry in entries]
