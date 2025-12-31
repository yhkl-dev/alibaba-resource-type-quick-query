Quick lookup for Alibaba resource types

This repository contains `a.json` — a list of Alibaba Cloud resource types — and a small helper to perform quick lookups and optional GitHub code searches.

Quick start

- Ensure you have Python 3.8+
- Run a local lookup:

```bash
python tools/github_search.py --query ECS::Instance
```

Optional: search GitHub for files mentioning the resource type

```bash
# Set GITHUB_TOKEN to increase quota and avoid rate limits
export GITHUB_TOKEN=ghp_xxx
python tools/github_search.py --query ECS::Instance --github-search --repo yhkl/alibaba-resource-type-quick-query
```

What I added
- `tools/github_search.py`: simple CLI to search `a.json` locally and call GitHub Search API.
- `README.md`: usage notes.

Next suggestions
- Add caching for GitHub results
- Build a small web UI or VS Code extension for instant fuzzy lookup
- Periodically refresh `a.json` using a GitHub Action that collects resource types from official docs

Static GitHub Pages site

I added a static UI at the repository root that loads `a.json` and provides instant fuzzy search. Files added:

- `index.html`
- `static/app.js`
- `static/style.css`

To preview locally:

```bash
# from repo root
python3 -m http.server 8000
# then open http://127.0.0.1:8000 in your browser
```
