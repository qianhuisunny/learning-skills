import zipfile
from pathlib import Path
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from pack_scorm import validate_zip


def test_validate_zip_passes_on_good_zip(tmp_path):
    zpath = tmp_path / "ok.zip"
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("imsmanifest.xml", "<?xml version='1.0'?><manifest/>")
        zf.writestr("index.html", "<html/>")
    assert validate_zip(zpath) == []


def test_validate_zip_flags_missing_manifest(tmp_path):
    zpath = tmp_path / "bad.zip"
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("index.html", "<html/>")
    errors = validate_zip(zpath)
    assert any("imsmanifest.xml" in e for e in errors)


def test_validate_zip_flags_malformed_manifest(tmp_path):
    zpath = tmp_path / "bad.zip"
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("imsmanifest.xml", "not xml at all")
        zf.writestr("index.html", "<html/>")
    errors = validate_zip(zpath)
    assert any("well-formed" in e.lower() for e in errors)
