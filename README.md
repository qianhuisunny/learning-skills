# eLearning pipeline workspace

Four-skill Claude Code pipeline that produces SCORM 1.2 packages.

The pipeline keeps instructional design, storyboarding, HTML production, and SCORM
packaging as separate reviewable stages.

## Layout
- `shell/` — shared HTML/CSS/JS + SCORM wrapper + XSD schemas (the "master template")
- `modules/` — one folder per module; each contains content-map, content files, build, dist
- `scripts/` — Python build helpers (merge, manifest-fill, pack)
- `skills/` — source for the four Claude skills
- `dev/` — throwaway test harnesses (hello-world SCO, test-layouts.html)

## Pipeline

```
brief/source
  -> /content-map   -> modules/<slug>/content-map.md + .docx
  -> /storyboard    -> modules/<slug>/storyboard/ + storyboard.pptx
  -> /build-html    -> modules/<slug>/content/*.md + build/
  -> /scorm-pack    -> modules/<slug>/dist/<slug>.zip
```

Stage boundaries:

- `/content-map` decides learning outcomes, assessment, practice, and teaching
  sequence at an instructional level. It does not assign slide numbers, layout
  IDs, or screen copy.
- `/storyboard` decides screen flow, interaction states, canonical layouts,
  voiceover, and developer notes. Because Claude Code is stronger at
  frontend/layout work than rich PPT editing, this stage may create an
  HTML-first storyboard prototype and then export or mirror it into a PPT review
  artifact.
- `/build-html` implements the approved storyboard in the shared shell. It does
  not redesign the lesson; when an approved canonical layout is missing in the
  shell, the default move is to extend the shell rather than silently adapt.
- `/scorm-pack` packages an already approved HTML build. It does not modify
  content, visuals, or behavior.

See `docs/reference/layout-contract.md` for the canonical layout registry.
