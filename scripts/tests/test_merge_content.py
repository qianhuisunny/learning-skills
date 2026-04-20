import json
from pathlib import Path
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from merge_content import parse_slide_file, merge, write_content_json


def make_module(tmp_path: Path) -> Path:
    (tmp_path / "content").mkdir()
    (tmp_path / "module.yml").write_text(
        "id: test\ntitle: Test Module\nmodule_label: Test\nscorm_identifier: com.test\n"
    )
    return tmp_path


def test_parse_slide_minimal(tmp_path):
    f = tmp_path / "01-intro.md"
    f.write_text("---\nlayout: L01\ntitle: Intro\nbody:\n  - Hello\n---\n")
    slide = parse_slide_file(f)
    assert slide["id"] == "01-intro"
    assert slide["layout"] == "L01"
    assert slide["title"] == "Intro"
    assert slide["body"] == ["Hello"]


def test_parse_slide_missing_layout_raises(tmp_path):
    f = tmp_path / "01-intro.md"
    f.write_text("---\ntitle: Intro\n---\n")
    with pytest.raises(ValueError, match="layout"):
        parse_slide_file(f)


def test_parse_slide_missing_frontmatter_raises(tmp_path):
    f = tmp_path / "01-intro.md"
    f.write_text("Just some text, no frontmatter.")
    with pytest.raises(ValueError, match="frontmatter"):
        parse_slide_file(f)


def test_merge_produces_valid_structure(tmp_path):
    module_dir = make_module(tmp_path)
    (module_dir / "content" / "01-intro.md").write_text(
        "---\nlayout: L01\ntitle: Intro\nbody:\n  - Hello\n---\n"
    )
    (module_dir / "content" / "02-summary.md").write_text(
        "---\nlayout: L14\ntitle: Wrap\ntakeaways:\n  - Nice\n---\n"
    )
    data = merge(module_dir)
    assert data["module"]["id"] == "test"
    assert len(data["slides"]) == 2
    assert data["slides"][0]["layout"] == "L01"
    assert data["slides"][1]["layout"] == "L14"


def test_merge_sorts_by_filename(tmp_path):
    module_dir = make_module(tmp_path)
    for name, title in [("03-c.md", "C"), ("01-a.md", "A"), ("02-b.md", "B")]:
        (module_dir / "content" / name).write_text(
            f"---\nlayout: L01\ntitle: {title}\nbody: []\n---\n"
        )
    data = merge(module_dir)
    assert [s["title"] for s in data["slides"]] == ["A", "B", "C"]


def test_write_content_json(tmp_path):
    module_dir = make_module(tmp_path)
    (module_dir / "content" / "01.md").write_text(
        "---\nlayout: L01\ntitle: T\nbody: []\n---\n"
    )
    out = write_content_json(module_dir)
    assert out.exists()
    data = json.loads(out.read_text())
    assert data["module"]["id"] == "test"
    assert data["slides"][0]["title"] == "T"
