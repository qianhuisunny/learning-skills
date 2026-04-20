"""Copy shell into build/, merge content, fill manifest, zip.

Usage:
    python3 pack_scorm.py <module_dir>

Produces: <module_dir>/dist/<module_id>.zip
"""
from __future__ import annotations
import json
import shutil
import sys
import zipfile
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
SHELL_DIR = WORKSPACE / "shell"

sys.path.insert(0, str(Path(__file__).parent))
from merge_content import write_content_json
from fill_manifest import write_manifest

SHELL_COPY_ITEMS = ["index.html", "css", "js", "schemas", "assets"]


def copy_shell(module_dir: Path) -> None:
    build = module_dir / "build"
    build.mkdir(parents=True, exist_ok=True)
    for item in SHELL_COPY_ITEMS:
        src = SHELL_DIR / item
        if not src.exists():
            continue
        dst = build / item
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)


def zip_build(module_dir: Path, module_id: str) -> Path:
    build = module_dir / "build"
    dist = module_dir / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    out = dist / f"{module_id}.zip"
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(build.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(build).as_posix())
    return out


def validate_zip(zip_path: Path) -> list[str]:
    errors = []
    if not zip_path.exists():
        return [f"zip file does not exist: {zip_path}"]
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if "imsmanifest.xml" not in names:
            errors.append("missing imsmanifest.xml at zip root")
        if "index.html" not in names:
            errors.append("missing index.html at zip root")
        try:
            import xml.etree.ElementTree as ET
            with zf.open("imsmanifest.xml") as mf:
                ET.parse(mf)
        except Exception as e:
            errors.append(f"imsmanifest.xml not well-formed XML: {e}")
    return errors


def pack(module_dir: Path) -> Path:
    module_dir = module_dir.expanduser().resolve()
    copy_shell(module_dir)
    write_content_json(module_dir)
    write_manifest(module_dir)
    data = json.loads((module_dir / "build" / "content.json").read_text())
    module_id = data["module"]["id"]
    zip_path = zip_build(module_dir, module_id)
    errors = validate_zip(zip_path)
    if errors:
        raise RuntimeError("zip validation failed:\n" + "\n".join(errors))
    return zip_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 pack_scorm.py <module_dir>", file=sys.stderr)
        sys.exit(2)
    zip_path = pack(Path(sys.argv[1]))
    size_kb = zip_path.stat().st_size // 1024
    with zipfile.ZipFile(zip_path) as zf:
        file_count = len(zf.namelist())
    print(f"SCORM package built: {zip_path} ({size_kb} KB, {file_count} files)")


if __name__ == "__main__":
    main()
