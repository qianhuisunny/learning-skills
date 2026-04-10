# eLearning pipeline workspace

Three-skill Claude Code pipeline that produces SCORM 1.2 packages.

Design spec + plan: `~/Desktop/elearning-storyboard/docs/superpowers/`.

## Layout
- `shell/` — shared HTML/CSS/JS + SCORM wrapper + XSD schemas (the "master template")
- `modules/` — one folder per module; each contains content-map, content files, build, dist
- `scripts/` — Python build helpers (merge, manifest-fill, pack)
- `skills-src/` — source for the three skills (symlinked into `~/.claude/skills/`)
- `dev/` — throwaway test harnesses (hello-world SCO, test-layouts.html)
