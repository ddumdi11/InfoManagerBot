from __future__ import annotations

from datetime import datetime, timezone
from time import struct_time
from typing import Any, Mapping


def coerce_text(value: Any) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return None


def extract_content_text(entry: Mapping[str, Any]) -> str | None:
    content = entry.get("content")
    if isinstance(content, list) and content:
        first_part = content[0]
        if isinstance(first_part, Mapping):
            text = coerce_text(first_part.get("value"))
            if text:
                return text
    return coerce_text(entry.get("summary"))


def parse_published_at(entry: Mapping[str, Any]) -> datetime | None:
    published_struct = entry.get("published_parsed") or entry.get("updated_parsed")
    if isinstance(published_struct, struct_time):
        # Feedparser liefert hier UTC-nahe struct_time-Werte, die wir im MVP direkt als UTC behandeln.
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
