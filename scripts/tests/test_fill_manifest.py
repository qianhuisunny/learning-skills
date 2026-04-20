import json
import xml.etree.ElementTree as ET
from pathlib import Path
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from fill_manifest import enumerate_files, render, write_manifest


def test_enumerate_files_skips_manifest(tmp_path):
    build = tmp_path / "build"
    build.mkdir()
    (build / "index.html").write_text("x")
    (build / "imsmanifest.xml").write_text("x")
    (build / "css").mkdir()
    (build / "css" / "theme.css").write_text("x")
    files = enumerate_files(build)
    assert "index.html" in files
    assert "css/theme.css" in files
    assert "imsmanifest.xml" not in files


def test_render_produces_valid_xml():
    meta = {"id": "m1", "title": "Test Module", "scorm_identifier": "com.test.m1"}
    files = ["index.html", "js/app.js", "css/theme.css"]
    xml = render(meta, files)
    root = ET.fromstring(xml)
    assert root.attrib["identifier"] == "com.test.m1"
    assert "Test Module" in xml
    assert 'href="index.html"' in xml
    assert 'href="js/app.js"' in xml


def test_render_falls_back_to_id_when_no_scorm_identifier():
    meta = {"id": "m1", "title": "T"}
    xml = render(meta, ["index.html"])
    assert 'identifier="m1"' in xml


def test_write_manifest_end_to_end(tmp_path):
    module_dir = tmp_path / "mod"
    build = module_dir / "build"
    build.mkdir(parents=True)
    (build / "index.html").write_text("x")
    (build / "content.json").write_text(json.dumps({
        "module": {"id": "m1", "title": "Test", "scorm_identifier": "com.test.m1"},
        "slides": []
    }))
    out = write_manifest(module_dir)
    assert out.exists()
    root = ET.fromstring(out.read_text())
    assert root.tag.endswith("manifest")
