---
name: build-html
description: Use after /storyboard — transforms per-slide markdown files into a runnable HTML module using the shared shell. Two phases with a review gate between them. Third skill in the eLearning pipeline.
---

# /build-html

## Overview

Two-phase skill:
- **Phase 1 (storyboard → slide files):** Read the storyboard output, produce one markdown file per slide in `content/`, present a summary table. STOP for review.
- **Phase 2 (build step):** Merge `content/*.md` + copy shell → produce runnable `build/index.html`. STOP for review.

## When to use

- User invokes `/build-html` after the storyboard has been reviewed
- User says "build the slides" / "generate the HTML" / "continue"

## Input

- `modules/<slug>/content-map.md` (from `/content-map`)
- Storyboard output (from `/storyboard` — PPT or markdown storyboard)
- Optional: supplementary reference material

## Phase 1 — Slide files

1. Read the storyboard. For each slide decide:
   - Which layout: L01, L03, L09, L12, L13, L14, or popup
   - What content goes in each field (per `shell/content.schema.md`)
2. Write `modules/<slug>/module.yml`:
   ```yaml
   id: 2.5-procurement-plan
   title: Developing the procurement plan
   module_label: Module 2.5
   scorm_identifier: com.qianhui.m2-5-procurement-plan
   ```
3. Write one `modules/<slug>/content/NN-slug.md` per slide with YAML frontmatter.
4. Present summary table (slide #, file, title, layout, type, notes).
5. **STOP for G2 review.** User verifies slide count, layouts, order, content. User can hand-edit files or describe changes in natural language.
6. On approval:
   ```bash
   cd ~/Desktop/elearning-skills && git add modules/<slug>/content/ modules/<slug>/module.yml && git commit -m "G2: content files approved for <slug>"
   ```

## Phase 2 — Build step

1. Run the pack script (which copies shell + merges content + fills manifest + zips):
   ```bash
   python3 ~/Desktop/elearning-skills/scripts/pack_scorm.py ~/Desktop/elearning-skills/modules/<slug>
   ```
   This populates `build/` as a side effect. For a build-only check (no zip needed yet), you can stop here and browse `build/`.
2. Start a local server:
   ```bash
   cd ~/Desktop/elearning-skills/modules/<slug>/build && python3 -m http.server 8765 &
   ```
3. Tell user: "Open http://localhost:8765/ and walk through the module."
4. **STOP for G3 review.** User walks through. Route feedback by layer:
   - **Content fix** ("slide 4 title should be X") → edit `content/*.md`, re-run build.
   - **Shell visual fix** ("all popup borders too thin") → edit `shell/css/themes/theme-b-airy.css`, warn user it affects all modules, re-run build.
   - **Shell behavior fix** ("checkmark doesn't show") → edit `shell/js/app.js`, re-run build.
5. On approval:
   ```bash
   pkill -f "http.server 8765" || true
   cd ~/Desktop/elearning-skills && git add modules/<slug>/build/ shell/ && git commit -m "G3: browser walkthrough passed for <slug>"
   ```

## Rules

1. Phase 1 and 2 are separate — STOP for G2 in between.
2. Use only MVP layouts: L01, L03, L09, L12, L13, L14, popup. Push back on deferred layouts.
3. Slide filenames: `NN-slug.md`, zero-padded prefix for ordering.
4. Popups use `layout: popup`, referenced by `popup_slide_id` from L12 bars.
5. Respect `shell/content.schema.md`.
6. **Slides must fit 16:9 (1280×720). No scrolling.** If content overflows, split into more slides.
7. Route user feedback to the right layer — don't make the user pick files.
8. On shell-level changes, warn the user that the change affects all modules.
9. Do not auto-trigger `/scorm-pack`.

## Reference files

- `shell/content.schema.md` — JSON field shapes per layout
- `docs/reference/elearning_available_components_and_layouts_3.md` — full layout spec
