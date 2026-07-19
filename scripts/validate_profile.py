#!/usr/bin/env python3
"""Validate the profile README and static GitHub Pages source without third-party CI actions."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.refs: list[str] = []
        self.meta: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for key in ("href", "src"):
            if values.get(key):
                self.refs.append(values[key] or "")
        if tag == "meta":
            key = values.get("property") or values.get("name")
            if key and values.get("content"):
                self.meta[key] = values["content"] or ""


def require_files(paths: list[str]) -> list[str]:
    return [f"missing or empty: {path}" for path in paths if not (ROOT / path).is_file() or (ROOT / path).stat().st_size == 0]


def local_target(base: Path, reference: str) -> Path | None:
    parsed = urlparse(reference)
    if parsed.scheme or reference.startswith(("#", "//")):
        return None
    return (base / parsed.path).resolve()


def validate() -> list[str]:
    errors = require_files([
        "README.md",
        "assets/profile-banner.svg",
        "docs/index.html",
        "docs/styles.css",
        "docs/assets/og-card-1200x630.jpg",
        "docs/assets/favicon.png",
        ".github/dependabot.yml",
    ])

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for ref in re.findall(r"!?(?:\[[^]]*\])\(([^)]+)\)", readme):
        target = local_target(ROOT, ref.strip())
        if target and not target.is_file():
            errors.append(f"broken local README reference: {ref}")

    parser = PageParser()
    parser.feed((ROOT / "docs/index.html").read_text(encoding="utf-8"))
    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        errors.append(f"duplicate HTML ids: {', '.join(duplicates)}")
    for required_id in ("main", "expertise", "work", "contact"):
        if required_id not in parser.ids:
            errors.append(f"missing HTML id: {required_id}")
    for ref in parser.refs:
        target = local_target(ROOT / "docs", ref)
        if target and not target.is_file():
            errors.append(f"broken local Pages reference: {ref}")
    for meta in ("description", "og:title", "og:description", "og:url", "og:image"):
        if not parser.meta.get(meta):
            errors.append(f"missing metadata: {meta}")

    html = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    for project in ("wisdom-it-readiness-toolkit", "sports-management-system-legacy"):
        if project not in html:
            errors.append(f"missing project reference: {project}")

    css = (ROOT / "docs/styles.css").read_text(encoding="utf-8")
    for marker in (":root", "@media", "prefers-reduced-motion"):
        if marker not in css:
            errors.append(f"missing CSS marker: {marker}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("Validation failed:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        raise SystemExit(1)
    print("Profile and Pages validation passed.")
