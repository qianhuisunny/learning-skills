"""Merge content/*.md slide files into a single content.json.

Each slide file has YAML frontmatter (--- delimited) with structured metadata
(id, layout, title, layout-specific fields). The body below the frontmatter
is currently ignored — all data lives in the frontmatter.

Usage:
    python3 merge_content.py <module_dir>

Reads:  <module_dir>/content/*.md + <module_dir>/module.yml
Writes: <module_dir>/build/content.json
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
import yaml

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def parse_slide_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"{path}: missing YAML frontmatter")
    slide = yaml.safe_load(m.group(1)) or {}
    if "id" not in slide:
        slide["id"] = path.stem
    if "layout" not in slide:
        raise ValueError(f"{path}: missing 'layout' in frontmatter")
    return slide


def load_module_metadata(module_dir: Path) -> dict:
    module_yml = module_dir / "module.yml"
    if not module_yml.exists():
        raise FileNotFoundError(f"{module_yml} not found")
    return yaml.safe_load(module_yml.read_text(encoding="utf-8"))


def merge(module_dir: Path) -> dict:
    content_dir = module_dir / "content"
    if not content_dir.is_dir():
        raise FileNotFoundError(f"{content_dir} not found")
    slide_files = sorted(content_dir.glob("*.md"))
    if not slide_files:
        raise ValueError(f"no slide files in {content_dir}")
    return {
        "module": load_module_metadata(module_dir),
        "slides": [parse_slide_file(p) for p in slide_files],
    }


def write_content_json(module_dir: Path) -> Path:
    data = merge(module_dir)
    build_dir = module_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    out = build_dir / "content.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 merge_content.py <module_dir>", file=sys.stderr)
        sys.exit(2)
    out = write_content_json(Path(sys.argv[1]).expanduser().resolve())
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
