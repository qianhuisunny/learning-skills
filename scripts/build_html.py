"""Copy the shared shell into build/ and merge content into content.json.

Usage:
    python3 build_html.py <module_dir>

Reads:  <module_dir>/module.yml + <module_dir>/content/*.md
Writes: <module_dir>/build/index.html + assets + content.json
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from merge_content import write_content_json
from pack_scorm import copy_shell


def build(module_dir: Path) -> Path:
    module_dir = module_dir.expanduser().resolve()
    copy_shell(module_dir)
    stale_manifest = module_dir / "build" / "imsmanifest.xml"
    if stale_manifest.exists():
        stale_manifest.unlink()
    return write_content_json(module_dir)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 build_html.py <module_dir>", file=sys.stderr)
        sys.exit(2)
    content_json = build(Path(sys.argv[1]))
    print(f"HTML build written: {content_json.parent}")
    print(f"Content JSON: {content_json}")


if __name__ == "__main__":
    main()
