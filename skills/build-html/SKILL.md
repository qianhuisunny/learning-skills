---
name: build-html
description: Use after /storyboard approval — implements the approved storyboard as a runnable HTML eLearning module using the shared shell. Third skill in the eLearning pipeline.
---

# /build-html

## Overview

Builds the production HTML module from an approved storyboard. This skill owns
implementation: translating storyboard screens into `content/*.md`, copying the
shared shell, merging `content.json`, and preparing a browser-reviewable build.

It does **not** redesign the instructional flow, create a new storyboard, or
package the module as SCORM. If the storyboard is insufficient, stop and ask for
G2 storyboard fixes before building.

Important: storyboard and runtime use the same canonical layout registry. This
skill verifies that the shell can render each approved canonical layout and
closes runtime gaps when needed.

## When to use

- User invokes `/build-html` after G2 storyboard approval
- User says "build the HTML", "implement the storyboard", or "make the module runnable"

## Input

Required:
- `modules/<slug>/storyboard/storyboard.md` or `storyboard.json`
- `modules/<slug>/module.yml` or enough metadata to create it

Optional:
- `modules/<slug>/storyboard/prototype/` as visual reference only
- `modules/<slug>/storyboard.pptx` as stakeholder-review reference

## Output

```text
modules/<slug>/
  module.yml
  content/
    NN-slug.md
  build/
    index.html
    content.json
    css/
    js/
    assets/
```

Do not write `dist/` and do not create a SCORM zip. That belongs to
`/scorm-pack`.

## Workflow

1. **Read the approved storyboard.** Treat it as the source of truth.
2. **Check build readiness.** Confirm every screen has an ID, title, canonical
   `layout`, type, on-screen content, interaction notes, and required build data.
3. **Write `module.yml`** if missing:
   ```yaml
   id: <module-slug>
   title: <module title>
   module_label: <module label>
   scorm_identifier: <reverse-domain.identifier>
   ```
4. **Verify runtime coverage.** Use `docs/reference/layout-contract.md` and
   `shell/content.schema.md`. If the shell cannot render an approved canonical
   layout, extend the schema/renderer/CSS or stop for a user-approved temporary
   adaptation.
5. **Write one `content/*.md` file per production screen** using YAML
   frontmatter that matches `shell/content.schema.md`.
6. **Preserve interaction wiring.** Popups use `layout: popup` and are
   referenced by `popup_slide_id` from L12 bars. Assessment screens include
   correct answers, feedback, and points.
7. **Run the HTML build script:**
   ```bash
   python3 ~/Desktop/elearning-skills/scripts/build_html.py ~/Desktop/elearning-skills/modules/<slug>
   ```
8. **Start a local server for browser review:**
   ```bash
   cd ~/Desktop/elearning-skills/modules/<slug>/build && python3 -m http.server 8765
   ```
9. **Tell the user to review** `http://localhost:8765/`.
10. **Route G3 feedback by layer:**
   - Content mismatch -> edit `content/*.md`, rerun build.
   - Storyboard mismatch -> return to `/storyboard`.
   - Missing runtime layout -> extend the shell, or ask for explicit approval
     before using a temporary adaptation.
   - Shell visual issue -> edit `shell/css/...`, warn user it affects all modules.
   - Shell behavior issue -> edit `shell/js/app.js`, warn user it affects all modules.
11. **On G3 approval**, git auto-commit:
    ```bash
    cd ~/Desktop/elearning-skills && git add modules/<slug>/module.yml modules/<slug>/content/ modules/<slug>/build/ shell/ && git commit -m "G3: HTML build approved for <slug>"
    ```

## Rules

1. Build from the approved storyboard; do not invent a new screen flow.
2. Production slide files live in `content/*.md`; storyboard artifacts stay in
   `storyboard/`.
3. Use only fields supported by `shell/content.schema.md`.
4. Production `layout` values must use the canonical registry in
   `docs/reference/layout-contract.md`.
5. Slides must fit the 16:9 shell. If content overflows, return to storyboard or
   split the production content only when the split is faithful to the approved
   storyboard.
6. Popups and assessments must preserve all states described in the storyboard.
7. If the storyboard requires an unsupported runtime component, default to
   extending the shell. Temporary adaptation requires explicit approval and an
   `adapted_from` note.
8. Do not call `pack_scorm.py`; use `build_html.py` for HTML builds.
9. Do not auto-trigger `/scorm-pack`.

## Reference Files

- `shell/content.schema.md`
- `docs/reference/layout-contract.md` — authoritative layout registry
- `scripts/build_html.py`
- `scripts/merge_content.py`
