# Research Pipeline — Paper Digest + AI Podcast

Track arXiv papers by your keywords, with AI-generated summaries and Chinese podcasts. Built on GitHub Pages + Actions.

## Quick Start

### 1. Use this template

Click the green **"Use this template"** button → **"Create a new repository"**. Choose a repository name (e.g., `my-research-digest`).

### 2. Configure your site

Copy the example configs to real ones:

```bash
cp config/settings.example.yaml config/settings.yaml
cp config/topics.example.yaml config/topics.yaml
```

Edit **`config/settings.yaml`** — set your GitHub username and repo name:

```yaml
site:
  title: "My Research Digest"
  url: "https://YOUR_USERNAME.github.io"
  baseurl: "/YOUR_REPO_NAME"        # your repo name, with leading /
```

Edit **`config/topics.yaml`** — define your arXiv search topics:

```yaml
topics:
  - name: "my_topic"
    display_name: "My Topic"
    search_query: "machine learning"    # arXiv search query
    max_results: 20
    abstract_contains: []               # ALL keywords must be in abstract
    any_keyword:                        # AT LEAST ONE keyword must be in abstract
      - "deep learning"
      - "transformer"
```

### 3. Edit `.gitignore` for your fork

The template's `.gitignore` includes rules that prevent generated content from being committed — these are only needed in the template repo itself. **Delete the entire "TEMPLATE-ONLY RULES" section** (everything between the `=====` markers at the top of `.gitignore`). Keep the "SHARED RULES" section.

After editing, your `.gitignore` should look roughly like:

```gitignore
# =============================================================================
# SHARED RULES — KEEP THESE
# =============================================================================

# Python
__pycache__/
*.pyc

# OS
.DS_Store
Thumbs.db

# (Add your own rules below if needed)
```

> Skipping this step will prevent the CI workflow from committing summary, podcast, and audio files.

### 4. Enable GitHub Pages

Go to your repo on GitHub: **Settings → Pages**:
- Source: **Deploy from a branch**
- Branch: `main`, folder: `/ (root)`
- Click **Save**

### 5. Add API key secret

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Required | Purpose |
|--------|----------|---------|
| `DEEPSEEK_API_KEY` | Yes (default) | DeepSeek API for summaries & podcasts |

Optional: `ANTHROPIC_API_KEY` (Claude) or `OPENAI_API_KEY` (GPT + TTS).

### 6. Run the first update

Go to **Actions → Daily Paper Update → Run workflow**.

Your site will be live at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/` within a minute.

---

## How It Works

```
arXiv API                    GitHub Actions (daily / on-demand)
    │                              │
    ▼                              ▼
┌─────────────┐    ┌──────────────────────────────┐
│ fetch new   │───▶│ scripts/fetch_abstracts.py    │──▶ data/papers_index.json
│ papers      │    │ scripts/generate_pages.py     │──▶ _papers/*.md + index.md
└─────────────┘    │ scripts/process_paper.py      │──▶ summary + MP3 podcast
                   └──────────────────────────────┘
                              │
                              ▼
                   GitHub Pages (Jekyll)
                   https://<you>.github.io/<repo>/
```

- **Daily update** (12:00 UTC): searches arXiv for your topics, publishes new papers
- **Summary + Podcast**: request from any paper page — opens a GitHub Issue, workflow generates English summary + Chinese podcast (~15-30 min MP3)
- **Manual Upload**: for non-arXiv papers — drag & drop PDF into an issue form
- **Cleanup**: papers older than 7 days without summaries are auto-removed

---

## Configuration Reference

### `config/settings.yaml`

| Field | Description | Default |
|-------|-------------|---------|
| `site.title` | Site title shown in header | `"Research Paper Digest"` |
| `site.url` | Full GitHub Pages URL | `https://YOUR_USERNAME.github.io` |
| `site.baseurl` | Repo path prefix | `"/YOUR_REPO_NAME"` |
| `llm.backend` | LLM for summaries: `deepseek`, `claude`, or `openai` | `deepseek` |
| `llm.model.<backend>` | Override default model per backend (optional) | see below |
| `tts.backend` | TTS for audio: `edge` or `openai` | `edge` |
| `tts.edge.voice` | Edge TTS voice name | `zh-CN-XiaoxiaoNeural` |
| `tts.edge.rate` | Edge TTS speech rate | `-5%` |
| `tts.openai.model` | OpenAI TTS model | `tts-1-hd` |
| `tts.openai.voice` | OpenAI TTS voice | `nova` |
| `tts.openai.speed` | OpenAI TTS speed (0.25–4.0) | `0.95` |

**Default models per LLM backend:**

| Backend | Default model |
|---------|---------------|
| `claude` | `claude-sonnet-4-6` |
| `openai` | `gpt-4o` |
| `deepseek` | `deepseek-chat` |

Override them under `llm.model` in settings.yaml (see `config/settings.example.yaml`).

### `config/topics.yaml`

| Field | Description |
|-------|-------------|
| `name` | Internal ID (snake_case) |
| `display_name` | Label shown on the website |
| `search_query` | arXiv query string (supports `cat:cs.RO`, boolean ops) |
| `max_results` | Papers per run (1–100) |
| `abstract_contains` | ALL keywords must appear in abstract. Empty = no filter |
| `any_keyword` | AT LEAST ONE keyword must appear. Empty = no filter |

### Environment variable overrides

| Variable | Overrides |
|----------|-----------|
| `LLM_BACKEND` | `config/settings.yaml` → `llm.backend` |
| `TTS_BACKEND` | `config/settings.yaml` → `tts.backend` |
| `SETTINGS_CONFIG_PATH` | Path to `settings.yaml` |
| `TOPICS_CONFIG_PATH` | Path to `topics.yaml` |

---

## Staying Up to Date

This repo is a **GitHub template** — your fork is independent, but you can pull upstream improvements manually.

### One-time setup (do this right after forking)

In your fork, add the upstream remote:

```bash
git remote add upstream https://github.com/Solitary2005/research-pipeline-template.git
git fetch upstream
```

### Pulling updates

```bash
git fetch upstream
git merge upstream/main
```

### What merges cleanly (no conflicts, ever)

| Files | Why |
|-------|-----|
| `scripts/`, `.github/workflows/` | Template changes code; you don't touch code |
| `_layouts/`, `_includes/`, `assets/css/` | Same reason |
| `config/settings.yaml`, `config/topics.yaml` | Template doesn't track them (gitignored) |
| `_papers/`, `_podcasts/`, `assets/audio/`, `_data/` | Template doesn't track them |
| `config/settings.example.yaml`, `config/topics.example.yaml` | Ignored by your `.gitignore` |

### What may need manual attention

| File | How often | What to do |
|------|-----------|------------|
| `.gitignore` | Rare (only if upstream adds new ignore rules) | Keep your version (`git checkout --ours .gitignore`). If upstream added a new shared rule (in the SHARED RULES section), copy only that line to your version. |
| `README.md` | Occasional | If you customized your README, resolve manually. Otherwise accept upstream's. |

### After-merge checklist

1. Check that **GitHub Actions** workflows still run (Actions tab in your repo)
2. Trigger a manual **Daily Paper Update** run to verify the pipeline works
3. Verify your **GitHub Pages** site loads correctly

### Wall-chart summary

```
fork once → edit .gitignore/config → done
merge upstream → resolve .gitignore (rare) → check CI → done
```

---

## Directory Structure

```
your-fork/
├── config/
│   ├── settings.yaml          ← YOU EDIT: site + backend config
│   ├── topics.yaml            ← YOU EDIT: arXiv search topics
│   ├── settings.example.yaml  ← template reference (gitignored in user repo)
│   └── topics.example.yaml    ← template reference (gitignored in user repo)
├── scripts/                   ← Pipeline code (pull upstream updates)
├── .github/workflows/         ← CI workflows (pull upstream updates)
├── _layouts/                  ← Jekyll page layouts
├── _includes/                 ← Jekyll partials
├── _papers/                   ← Generated paper pages (auto, committed by CI)
├── _podcasts/                 ← Generated podcast pages (auto, committed by CI)
├── _data/summaries/           ← Generated summary JSON (auto, committed by CI)
├── assets/
│   ├── css/style.scss         ← Site styles
│   └── audio/                 ← Generated MP3 files (auto, committed by CI)
├── data/
│   └── papers_index.json      ← Paper metadata index (auto, committed by CI)
├── index.md                   ← Landing page (auto-generated)
├── favorites.md               ← Favorites index page
└── _config.yml                ← Jekyll config (auto-synced from settings.yaml)
```

---

## License

MIT — see [LICENSE](LICENSE).
