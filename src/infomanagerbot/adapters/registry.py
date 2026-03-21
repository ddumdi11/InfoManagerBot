from __future__ import annotations

from infomanagerbot.adapters.base import DiscoveryAdapter
from infomanagerbot.adapters.rss import RssAtomAdapter
from infomanagerbot.config.models import SourceModel, SourceType


def build_adapter_registry() -> dict[SourceType, DiscoveryAdapter]:
    return {
        SourceType.RSS_ATOM: RssAtomAdapter(),
    }


def get_adapter_for_source(source: SourceModel) -> DiscoveryAdapter:
    registry = build_adapter_registry()
    try:
        return registry[source.type]
    except KeyError as error:
        raise ValueError(f"Kein Adapter fuer Source-Typ registriert: {source.type}") from error
