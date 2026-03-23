from __future__ import annotations

from functools import lru_cache

from infomanagerbot.adapters.base import DiscoveryAdapter
from infomanagerbot.adapters.rss import RssAtomAdapter
from infomanagerbot.adapters.youtube import YouTubeChannelAdapter
from infomanagerbot.config.models import SourceModel, SourceType


@lru_cache(maxsize=1)
def build_adapter_registry() -> dict[SourceType, DiscoveryAdapter]:
    return {
        SourceType.RSS_ATOM: RssAtomAdapter(),
        SourceType.YOUTUBE_CHANNEL: YouTubeChannelAdapter(),
    }


def get_adapter_for_source(source: SourceModel) -> DiscoveryAdapter:
    registry = build_adapter_registry()
    try:
        return registry[source.type]
    except KeyError as error:
        raise ValueError(f"Kein Adapter fuer Source-Typ registriert: {source.type}") from error
