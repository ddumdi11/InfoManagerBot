from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone

from infomanagerbot.config.models import PolicyModel, SourceModel
from infomanagerbot.domain.models import DiscoveredItem, PersistedItem, Policy, Source


@dataclass(slots=True)
class PolicyRepository:
    connection: sqlite3.Connection

    def sync(self, policies: list[PolicyModel]) -> None:
        with self.connection:
            for policy in policies:
                self.connection.execute(
                    """
                    INSERT INTO policies (
                        policy_key,
                        enabled,
                        archive_format,
                        match_source_ids_json,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(policy_key) DO UPDATE SET
                        enabled = excluded.enabled,
                        archive_format = excluded.archive_format,
                        match_source_ids_json = excluded.match_source_ids_json,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        policy.id,
                        int(policy.enabled),
                        policy.archive_format,
                        json.dumps(policy.match_source_ids),
                    ),
                )

    def list_all(self) -> list[Policy]:
        rows = self.connection.execute(
            """
            SELECT policy_key, enabled, archive_format, match_source_ids_json
            FROM policies
            ORDER BY policy_key
            """
        ).fetchall()
        return [
            Policy(
                id=row["policy_key"],
                enabled=bool(row["enabled"]),
                archive_format=row["archive_format"],
                match_source_ids=json.loads(row["match_source_ids_json"]),
            )
            for row in rows
        ]


@dataclass(slots=True)
class SourceRepository:
    connection: sqlite3.Connection

    def sync(self, sources: list[SourceModel]) -> None:
        with self.connection:
            for source in sources:
                self.connection.execute(
                    """
                    INSERT INTO sources (
                        source_key,
                        source_type,
                        enabled,
                        display_name,
                        locator,
                        updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(source_key) DO UPDATE SET
                        source_type = excluded.source_type,
                        enabled = excluded.enabled,
                        display_name = excluded.display_name,
                        locator = excluded.locator,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (
                        source.id,
                        source.type.value,
                        int(source.enabled),
                        source.display_name,
                        source.locator,
                    ),
                )

    def list_all(self) -> list[Source]:
        rows = self.connection.execute(
            """
            SELECT source_key, source_type, enabled, display_name, locator
            FROM sources
            ORDER BY source_key
            """
        ).fetchall()
        return [
            Source(
                id=row["source_key"],
                source_type=row["source_type"],
                enabled=bool(row["enabled"]),
                display_name=row["display_name"],
                locator=row["locator"],
            )
            for row in rows
        ]

    def get_db_id_by_key(self, source_key: str) -> int | None:
        row = self.connection.execute(
            "SELECT id FROM sources WHERE source_key = ?",
            (source_key,),
        ).fetchone()
        if row is None:
            return None
        return int(row["id"])


@dataclass(slots=True)
class ItemRepository:
    connection: sqlite3.Connection

    def exists(self, source_id: int, external_id: str) -> bool:
        row = self.connection.execute(
            """
            SELECT 1
            FROM items
            WHERE source_id = ? AND external_id = ?
            """,
            (source_id, external_id),
        ).fetchone()
        return row is not None

    def create_discovered_item(
        self,
        source_id: int,
        item: DiscoveredItem,
        run_id: int,
        status: str = "discovered",
    ) -> int:
        discovered_at = datetime.now(timezone.utc).isoformat()
        published_at = item.published_at.isoformat() if item.published_at else None
        cursor = self.connection.execute(
            """
            INSERT INTO items (
                source_id,
                run_id,
                external_id,
                title,
                url,
                status,
                discovered_at,
                published_at,
                content_text
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source_id,
                run_id,
                item.external_id,
                item.title,
                item.url,
                status,
                discovered_at,
                published_at,
                item.content_text,
            ),
        )
        item_id = cursor.lastrowid
        if item_id is None:
            raise RuntimeError("Item konnte nicht gespeichert werden.")
        self.connection.commit()
        return int(item_id)

    def list_items_for_archiving(self) -> list[PersistedItem]:
        with self.connection:
            rows = self.connection.execute(
                """
                SELECT
                    items.id AS item_id,
                    items.source_id,
                    sources.source_key,
                    sources.source_type,
                    items.external_id,
                    items.title,
                    items.url,
                    items.discovered_at,
                    items.published_at,
                    items.run_id,
                    items.content_text
                FROM items
                INNER JOIN sources ON sources.id = items.source_id
                WHERE items.status = 'discovered'
                ORDER BY items.id
                """
            ).fetchall()

            if not rows:
                return []

            item_ids = [int(row["item_id"]) for row in rows]
            placeholders = ", ".join("?" for _ in item_ids)
            self.connection.execute(
                f"""
                UPDATE items
                SET status = 'archiving'
                WHERE status = 'discovered' AND id IN ({placeholders})
                """,
                item_ids,
            )

        return [
            PersistedItem(
                item_id=int(row["item_id"]),
                source_id=int(row["source_id"]),
                source_key=row["source_key"],
                source_type=row["source_type"],
                external_id=row["external_id"],
                title=row["title"],
                url=row["url"],
                discovered_at=row["discovered_at"],
                published_at=row["published_at"],
                run_id=row["run_id"],
                status="archiving",
                content_text=row["content_text"],
            )
            for row in rows
        ]

    def mark_as_archived(self, item_id: int) -> None:
        cursor = self.connection.execute(
            "UPDATE items SET status = 'archived' WHERE id = ? AND status = 'archiving'",
            (item_id,),
        )
        if cursor.rowcount == 0:
            raise RuntimeError(f"Item konnte nicht als archiviert markiert werden: id={item_id}.")
        self.connection.commit()


@dataclass(slots=True)
class ArtifactRepository:
    connection: sqlite3.Connection

    def create_artifact_if_missing(
        self,
        item_id: int,
        artifact_type: str,
        storage_path: str,
        content_format: str,
    ) -> bool:
        cursor = self.connection.execute(
            """
            INSERT INTO artifacts (item_id, artifact_type, storage_path, content_format)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(item_id, artifact_type, storage_path) DO NOTHING
            """,
            (item_id, artifact_type, storage_path, content_format),
        )
        self.connection.commit()
        return cursor.rowcount > 0


@dataclass(slots=True)
class RunRepository:
    connection: sqlite3.Connection

    def create_run(self, status: str = "prepared", notes: str | None = None) -> int:
        cursor = self.connection.execute(
            """
            INSERT INTO runs (started_at, status, notes)
            VALUES (?, ?, ?)
            """,
            (datetime.now(timezone.utc).isoformat(), status, notes),
        )
        run_id = cursor.lastrowid
        if run_id is None:
            raise RuntimeError("Failed to create run: sqlite3 did not return a lastrowid.")
        self.connection.commit()
        return run_id

    def finish_run(self, run_id: int, status: str, notes: str | None = None) -> None:
        cursor = self.connection.execute(
            """
            UPDATE runs
            SET finished_at = ?, status = ?, notes = ?
            WHERE id = ?
            """,
            (datetime.now(timezone.utc).isoformat(), status, notes, run_id),
        )
        if cursor.rowcount == 0:
            raise RuntimeError(f"Run konnte nicht abgeschlossen werden, keine Zeile fuer id={run_id}.")
        self.connection.commit()
