"""arXiv paper search and filtering module.

Provides the classes needed to search arXiv by topic configuration,
filter results by keyword, and accumulate papers into the local index.
"""

from .config_reader import TopicConfig, PipelineConfig, ConfigReader
from .search_engine import PaperInfo, ArxivSearchEngine
from .paper_filter import PaperFilter
from .paper_accumulator import PaperAccumulator

__all__ = [
    "TopicConfig",
    "PipelineConfig",
    "ConfigReader",
    "PaperInfo",
    "ArxivSearchEngine",
    "PaperFilter",
    "PaperAccumulator",
]
