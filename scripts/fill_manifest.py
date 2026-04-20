"""Render shell/manifest-template.xml with module metadata + file list.

Usage:
    python3 fill_manifest.py <module_dir>

Reads:  <module_dir>/build/content.json for metadata
        Enumerates files under <module_dir>/build/
Writes: <module_dir>/build/imsmanifest.xml
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from jinja2 import Template

WORKSPACE = Path(__file__).parent.parent
TEMPLATE_PATH = WORKSPACE / "shell" / "manifest-template.xml"


def enumerate_files(build_dir: Path) -> list[str]:
    files = []
    for p in sorted(build_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(build_dir).as_posix()
        if rel == "imsmanifest.xml":
            continue
        files.append(rel)
    return files


def render(module_meta: dict, files: list[str]) -> str:
    template = Template(TEMPLATE_PATH.read_text(encoding="utf-8"), keep_trailing_newline=True)
    return template.render(
        identifier=module_meta.get("scorm_identifier", module_meta["id"]),
        version="1.0",
        title=module_meta["title"],
        files=files,
    )


def write_manifest(module_dir: Path) -> Path:
    build_dir = module_dir / "build"
    content_json = build_dir / "content.json"
    if not content_json.exists():
        raise FileNotFoundError(f"{content_json} not found — run merge_content first")
    data = json.loads(content_json.read_text(encoding="utf-8"))
    manifest_xml = render(data["module"], enumerate_files(build_dir))
    out = build_dir / "imsmanifest.xml"
    out.write_text(manifest_xml, encoding="utf-8")
    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fill_manifest.py <module_dir>", file=sys.stderr)
        sys.exit(2)
    out = write_manifest(Path(sys.argv[1]).expanduser().resolve())
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
