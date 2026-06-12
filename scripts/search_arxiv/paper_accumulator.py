"""Manage the on-disk papers_index.json store."""

import json
from pathlib import Path
from typing import Dict, Set

from .search_engine import PaperInfo


class PaperAccumulator:
    """Manages the papers_index.json index file.

    Loads the existing index on construction, provides methods to add
    new papers while preserving existing entries and their flags
    (interesting, has_summary, has_podcast).

    The index format is:
        {paper_id: {arxiv_id, title, abstract, authors, first_author,
                    primary_category, pdf_url, abs_url, topic,
                    interesting, has_summary, has_podcast}}
    """

    def __init__(self, path: Path):
        """Initialize the accumulator, loading the existing index if present.

        Args:
            path: Path to papers_index.json.
        """
        self.path = path
        self._index = self._load()

    def _load(self) -> dict:
        """Load the index from disk, or return an empty dict if missing."""
        if self.path.exists():
            with open(self.path, "r") as f:
                content = f.read()
                if content.strip():
                    return json.loads(content)
        return {}

    def save(self) -> None:
        """Write the index back to disk."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self._index, f, ensure_ascii=False, indent=2)

    @property
    def index(self) -> dict:
        """The full index dictionary (read-only access)."""
        return self._index

    def known_ids(self) -> Set[str]:
        """Return the set of paper IDs already in the index."""
        return set(self._index.keys())

    def add_paper(self, info: PaperInfo) -> str:
        """Add a new paper entry to the index.

        Args:
            info: PaperInfo from the search engine.

        Returns:
            The arxiv_id of the added paper.

        Raises:
            KeyError: If the paper ID already exists in the index.
        """
        if info.arxiv_id in self._index:
            raise KeyError(f"Paper {info.arxiv_id} already exists in index")

        entry = {
            "arxiv_id": info.arxiv_id,
            "title": info.title,
            "abstract": info.abstract,
            "published_date": info.published_date,
            "authors": info.authors,
            "first_author": info.first_author,
            "primary_category": info.primary_category,
            "pdf_url": info.pdf_url,
            "abs_url": info.abs_url,
            "topic": info.topic,
            "interesting": False,
            "has_summary": False,
            "has_podcast": False,
        }

        self._index[info.arxiv_id] = entry
        return info.arxiv_id

    def __len__(self) -> int:
        return len(self._index)

    def __contains__(self, arxiv_id: str) -> bool:
        return arxiv_id in self._index
