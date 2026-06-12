"""Filter arXiv papers by abstract keyword matching."""

from .config_reader import TopicConfig
from .search_engine import PaperInfo


class PaperFilter:
    """Applies keyword-based filtering to arXiv search results.

    Two filter stages (both case-insensitive):
    1. abstract_contains: ALL listed keywords must appear in the abstract.
    2. any_keyword: AT LEAST ONE listed keyword must appear in the abstract.

    If a filter list is empty, that stage is skipped (passes automatically).
    """

    @staticmethod
    def passes(paper: PaperInfo, cfg: TopicConfig) -> bool:
        """Check whether a paper satisfies the topic's filter rules.

        Args:
            paper: The paper to check.
            cfg: The topic configuration with filter keywords.

        Returns:
            True if the paper passes all filter stages.
        """
        abstract_lower = paper.abstract.lower()

        # Stage 1: ALL of abstract_contains must be present
        if cfg.abstract_contains:
            if not all(kw.lower() in abstract_lower for kw in cfg.abstract_contains):
                return False

        # Stage 2: AT LEAST ONE of any_keyword must be present
        if cfg.any_keyword:
            if not any(kw.lower() in abstract_lower for kw in cfg.any_keyword):
                return False

        return True
