from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from infomanagerbot.config.models import SourceModel
from infomanagerbot.domain.models import DiscoveredItem


class AdapterError(RuntimeError):
    pass


@dataclass(slots=True)
class DiscoveryAdapter(ABC):
    source_type: str

    @abstractmethod
    def discover(self, source: SourceModel) -> list[DiscoveredItem]:
        """Load source data and map it to normalized discovered items."""

    def enrich(self, item: DiscoveredItem, source: SourceModel) -> DiscoveredItem:
        return item
