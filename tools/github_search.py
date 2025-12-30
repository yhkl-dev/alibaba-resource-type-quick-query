#!/usr/bin/env python3
"""Quick lookup for resource types from a.json and optional GitHub search.

Usage:
  python tools/github_search.py --query ECS::Instance --github-search --repo yhkl/alibaba-resource-type-quick-query

Options:
  --query TEXT        Search query (resource type or substring)
  --github-search     Use GitHub Search API to find files mentioning the query
  --repo OWNER/REPO   Limit GitHub search to this repository
  --token ENV         Read GitHub token from env var name (default: GITHUB_TOKEN)
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def load_resources(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [r.get("ResourceType", "") for r in data.get("ResourceTypes", [])]


def local_search(resources, query):
    q = query.lower()
    return [r for r in resources if q in r.lower()]


def github_search(query, repo=None, token_env="GITHUB_TOKEN"):
    token = os.environ.get(token_env)
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    q = f'"{query}" in:file'
    if repo:
        q += f" repo:{repo}"
    params = {"q": q}
    url = "https://api.github.com/search/code?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        print("GitHub API error:", e.read().decode("utf-8"), file=sys.stderr)
        return None


def print_results(query, local_matches, gh_results):
    print(f"Query: {query}\n")
    print("Local matches:")
    for m in local_matches:
        print(" -", m)
    print("\n")
    if gh_results is None:
        print("GitHub search: skipped or failed")
        return
    print("GitHub search results:")
    items = gh_results.get("items", [])
    for it in items[:20]:
        name = it.get("name")
        path = it.get("path")
        html_url = it.get("html_url")
        repo = it.get("repository", {}).get("full_name")
        print(f" - {repo}/{path} -> {html_url}")


def main():
    parser = argparse.ArgumentParser(description="Quick lookup for resource types and optional GitHub search")
    parser.add_argument("--query", required=True)
    parser.add_argument("--github-search", action="store_true")
    parser.add_argument("--repo")
    parser.add_argument("--token", default="GITHUB_TOKEN")
    parser.add_argument("--data", default="a.json")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = args.data if os.path.isabs(args.data) else os.path.join(script_dir, args.data)
    resources = load_resources(data_path)
    local_matches = local_search(resources, args.query)
    gh_results = None
    if args.github_search:
        gh_results = github_search(args.query, repo=args.repo, token_env=args.token)

    print_results(args.query, local_matches, gh_results)


if __name__ == "__main__":
    main()
