from __future__ import annotations

import logging


def setup_logging(log_level: str = "INFO") -> None:
    normalized_level_name = log_level.upper()
    level = getattr(logging, normalized_level_name, None)
    if not isinstance(level, int):
        level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )
    if normalized_level_name != logging.getLevelName(level):
        logging.getLogger(__name__).warning(
            "Ungueltiges Log-Level '%s', falle auf INFO zurueck.",
            log_level,
        )
