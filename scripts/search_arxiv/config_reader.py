"""Read and validate the user-facing YAML topic configuration."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List


class ConfigError(Exception):
    """Raised when the topic configuration is invalid."""
    pass


@dataclass
class TopicConfig:
    """Configuration for a single arXiv search topic.

    Attributes:
        name: Internal identifier (e.g. "dexterous_grasp").
        display_name: Human-readable label shown on the website.
        search_query: arXiv API search query string.
        max_results: Maximum number of results to fetch per run.
        abstract_contains: Keywords that must ALL appear in the abstract.
        any_keyword: Keywords where AT LEAST ONE must appear in the abstract.
    """
    name: str
    display_name: str
    search_query: str
    max_results: int = 20
    abstract_contains: List[str] = field(default_factory=list)
    any_keyword: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.name or not isinstance(self.name, str):
            raise ConfigError("Each topic must have a non-empty 'name'")
        if not self.search_query or not isinstance(self.search_query, str):
            raise ConfigError(f"Topic '{self.name}' must have a non-empty 'search_query'")
        if not isinstance(self.max_results, int) or self.max_results < 1:
            self.max_results = 20
        self.max_results = min(self.max_results, 100)


@dataclass
class PipelineConfig:
    """Top-level pipeline configuration holding all topics."""
    topics: List[TopicConfig] = field(default_factory=list)


class ConfigReader:
    """Reads and validates the YAML topic configuration file."""

    DEFAULT_YAML = """# =============================================================================
# Research Pipeline — Topic Configuration
# =============================================================================
# Customize this file to control which arXiv papers are discovered.
#
# Each topic defines:
#   - name:              Internal identifier (use snake_case, no spaces)
#   - display_name:      Human-readable name shown on the website
#   - search_query:      arXiv API search string (supports full query syntax:
#                         boolean operators, category filters like cat:cs.RO, etc.)
#   - max_results:       Max papers to fetch per run (1–100; default 20)
#   - abstract_contains: ALL of these strings must appear in the abstract
#                         (case-insensitive). Set to [] to disable.
#   - any_keyword:       AT LEAST ONE of these strings must appear in the
#                         abstract (case-insensitive). Set to [] to disable.
#
# To add your own research area, append a new entry to the 'topics' list.
# =============================================================================

topics:
  - name: "dexterous_grasp"
    display_name: "Dexterous Grasp"
    search_query: "grasp"
    max_results: 20
    abstract_contains:
      - "grasp"
    any_keyword:
      - "dexterous"
      - "dex"
"""

    @staticmethod
    def load(path: Path) -> PipelineConfig:
        """Load and validate topic configuration from a YAML file.

        Args:
            path: Path to the YAML configuration file.

        Returns:
            A validated PipelineConfig instance.

        Raises:
            ConfigError: If the file is missing, unparseable, or invalid.
        """
        import yaml

        if not path.exists():
            raise ConfigError(
                f"Topic config not found at {path}. "
                f"Run with no arguments to auto-create a default config."
            )

        try:
            with open(path, "r") as f:
                raw = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigError(f"Failed to parse {path}: {e}")

        if raw is None:
            raise ConfigError(f"Topic config at {path} is empty. Add at least one topic.")

        topics_raw = raw.get("topics", [])
        if not isinstance(topics_raw, list):
            raise ConfigError("'topics' must be a list in the YAML config.")

        if not topics_raw:
            raise ConfigError("No topics defined. Add at least one topic to 'topics' list.")

        topics = []
        for i, t in enumerate(topics_raw):
            if not isinstance(t, dict):
                raise ConfigError(f"Topic entry {i} must be a dictionary, got {type(t).__name__}")

            # Validate required string fields
            for field_name in ("name", "search_query"):
                val = t.get(field_name)
                if not val or not isinstance(val, str):
                    raise ConfigError(
                        f"Topic entry {i} is missing required string field '{field_name}'"
                    )

            topic = TopicConfig(
                name=t["name"],
                display_name=t.get("display_name", t["name"]),
                search_query=t["search_query"],
                max_results=t.get("max_results", 20),
                abstract_contains=t.get("abstract_contains", []),
                any_keyword=t.get("any_keyword", []),
            )
            topics.append(topic)

        return PipelineConfig(topics=topics)

    @staticmethod
    def create_default(path: Path) -> PipelineConfig:
        """Write the default configuration template to disk and return it.

        Args:
            path: Where to write the default YAML file.

        Returns:
            The default PipelineConfig.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(ConfigReader.DEFAULT_YAML)
        return ConfigReader.load(path)
