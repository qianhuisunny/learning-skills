"""Package an already-approved HTML build as a SCORM zip.

Usage:
    python3 package_scorm.py <module_dir>

Reads:  <module_dir>/build/index.html + content.json
Writes: <module_dir>/build/imsmanifest.xml + dist/<module_id>.zip
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fill_manifest import write_manifest
from pack_scorm import validate_zip, zip_build


def package(module_dir: Path) -> Path:
    module_dir = module_dir.expanduser().resolve()
    build_dir = module_dir / "build"
    content_json = build_dir / "content.json"
    index_html = build_dir / "index.html"
    if not index_html.exists():
        raise FileNotFoundError(f"{index_html} not found — run /build-html first")
    if not content_json.exists():
        raise FileNotFoundError(f"{content_json} not found — run /build-html first")

    write_manifest(module_dir)
    data = json.loads(content_json.read_text(encoding="utf-8"))
    zip_path = zip_build(module_dir, data["module"]["id"])
    errors = validate_zip(zip_path)
    if errors:
        raise RuntimeError("zip validation failed:\n" + "\n".join(errors))
    return zip_path


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 package_scorm.py <module_dir>", file=sys.stderr)
        sys.exit(2)
    zip_path = package(Path(sys.argv[1]))
    size_kb = zip_path.stat().st_size // 1024
    with zipfile.ZipFile(zip_path) as zf:
        file_count = len(zf.namelist())
    print(f"SCORM package built: {zip_path} ({size_kb} KB, {file_count} files)")


if __name__ == "__main__":
    main()
