from __future__ import annotations

import json
import re
from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path

from infomanagerbot.domain.models import PersistedItem


def slugify(value: str, max_length: int = 60) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    if not normalized:
        return "item"
    return normalized[:max_length].rstrip("-") or "item"


def build_short_id(value: str, length: int = 8) -> str:
    return sha1(value.encode("utf-8")).hexdigest()[:length]


def build_archive_directory(output_dir: Path, item: PersistedItem) -> Path:
    date_prefix = (item.published_at or item.discovered_at)[:10]
    short_id = build_short_id(item.external_id)
    slug = slugify(item.title)
    return output_dir / item.source_type / item.source_key / f"{date_prefix}_{short_id}_{slug}"


def build_metadata_payload(item: PersistedItem) -> dict[str, object]:
    return {
        "item_id": item.item_id,
        "source_key": item.source_key,
        "source_type": item.source_type,
        "external_id": item.external_id,
        "title": item.title,
        "url": item.url,
        "discovered_at": item.discovered_at,
        "published_at": item.published_at,
        "run_id": item.run_id,
        "status": item.status,
    }


@dataclass(slots=True)
class ArchiveWriter:
    output_dir: Path

    def write_item(self, item: PersistedItem) -> dict[str, Path]:
        archive_dir = build_archive_directory(self.output_dir, item)
        archive_dir.mkdir(parents=True, exist_ok=True)

        metadata_path = archive_dir / "metadata.json"
        content_path = archive_dir / "content.md"

        metadata_path.write_text(
            json.dumps(build_metadata_payload(item), indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )
        content_path.write_text(self._build_markdown_content(item), encoding="utf-8")

        return {
            "metadata": metadata_path,
            "content": content_path,
        }

    def _build_markdown_content(self, item: PersistedItem) -> str:
        lines = [
            f"# {item.title}",
            "",
            f"- Quelle: `{item.source_key}`",
            f"- Quellentyp: `{item.source_type}`",
        ]
        if item.url:
            lines.append(f"- URL: {item.url}")
        if item.published_at:
            lines.append(f"- Published At: {item.published_at}")
        lines.append(f"- Discovered At: {item.discovered_at}")
        lines.append("")

        if item.content_text:
            lines.append(item.content_text.strip())
        else:
            lines.append("_Kein weiterer Inhalt im aktuellen Discovery-Schritt verfuegbar._")

        lines.append("")
        return "\n".join(lines)
