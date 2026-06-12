#!/usr/bin/env python3
"""Search arXiv for new papers matching configured topics, update papers_index.json.

Replaces the old CDN-based flow (which downloaded JSON from Dexterous-grasp-daily).
Now searches arXiv directly using the user-configurable topics in config/topics.yaml.
"""

import sys
import time

from search_arxiv.config_reader import ConfigReader, ConfigError
from search_arxiv.search_engine import ArxivSearchEngine
from search_arxiv.paper_filter import PaperFilter
from search_arxiv.paper_accumulator import PaperAccumulator
from utils.config import config


def main():
    # 1. Load or create topic configuration
    if not config.topics_config_path.exists():
        print(f"[search] No topic config found at {config.topics_config_path}")
        print(f"[search] Creating default config from template...")
        pipeline_cfg = ConfigReader.create_default(config.topics_config_path)
        print(f"[search] Created {config.topics_config_path}. Edit it to customize your topics.")
        print(f"[search] Re-run to start searching with the default config.")
    else:
        try:
            pipeline_cfg = ConfigReader.load(config.topics_config_path)
        except ConfigError as e:
            print(f"[search] ERROR: {e}", file=sys.stderr)
            sys.exit(1)

    if not pipeline_cfg.topics:
        print("[search] No topics configured. Add topics to config/topics.yaml and re-run.")
        return

    print(f"[search] Loaded {len(pipeline_cfg.topics)} topic(s) from {config.topics_config_path}")

    # 2. Load existing paper index
    accumulator = PaperAccumulator(config.index_path)
    known_ids = accumulator.known_ids()
    print(f"[search] Existing index: {len(known_ids)} papers")

    # 3. Search each topic
    new_paper_ids = []
    engine = ArxivSearchEngine()
    total_raw = 0
    total_filtered = 0

    for i, topic_cfg in enumerate(pipeline_cfg.topics):
        print(f"\n[search] Topic {i+1}/{len(pipeline_cfg.topics)}: {topic_cfg.display_name}")
        print(f"[search]   Query: \"{topic_cfg.search_query}\", max_results={topic_cfg.max_results}")

        if topic_cfg.abstract_contains:
            print(f"[search]   Must contain ALL: {topic_cfg.abstract_contains}")
        if topic_cfg.any_keyword:
            print(f"[search]   Must contain ANY: {topic_cfg.any_keyword}")

        try:
            raw_papers = engine.search(topic_cfg)
        except Exception as e:
            print(f"[search]   ERROR searching arXiv: {e}", file=sys.stderr)
            continue

        total_raw += len(raw_papers)
        filtered = [p for p in raw_papers if PaperFilter.passes(p, topic_cfg)]
        total_filtered += len(filtered)

        print(f"[search]   Fetched {len(raw_papers)} results, {len(filtered)} passed filter")

        for paper in filtered:
            if paper.arxiv_id in known_ids:
                continue

            accumulator.add_paper(paper)
            known_ids.add(paper.arxiv_id)
            new_paper_ids.append(paper.arxiv_id)
            print(f"[search]   → NEW: {paper.arxiv_id} — {paper.title[:80]}")

        # Brief pause between topics to be kind to arXiv
        if i < len(pipeline_cfg.topics) - 1:
            time.sleep(2)

    # 4. Save updated index
    accumulator.save()
    print(f"\n[search] Summary: {total_raw} total fetched, {total_filtered} passed filter, "
          f"{len(new_paper_ids)} new papers added.")
    print(f"[search] Index now has {len(accumulator)} papers total.")

    # 5. Write new_papers.txt for generate_pages.py
    new_ids_path = config.data_dir / "new_papers.txt"
    config.data_dir.mkdir(parents=True, exist_ok=True)
    with open(new_ids_path, "w") as f:
        for pid in new_paper_ids:
            if pid in accumulator:
                f.write(f"{pid}\n")

    if new_paper_ids:
        print(f"[search] Wrote {len(new_paper_ids)} IDs to {new_ids_path}")


if __name__ == "__main__":
    main()
