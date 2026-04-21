---
name: content-map
description: Use when starting a new eLearning module — turns a brief, lesson plan, or seed content into a 4-column O-A-P-P (Objective / Assessment / Practice / Presentation) alignment table. First skill in the eLearning pipeline.
---

# /content-map

## Overview

Transforms a lesson brief into a tight alignment table. Every row links one learning objective to its assessment, practice, and presentation content. Forces alignment thinking BEFORE any storyboard or slide design.

## When to use

- User invokes `/content-map`
- User asks to "map out content" / "plan a module" / "build a course on X"

## Input

Any of:
- A one-line brief ("30-min module on procurement planning for PMs")
- A lesson plan document (PDF, Word, pasted text)
- A seed example + user's ID intuition

## Workflow

1. **Parse the input.** Identify topic, audience, scope, duration target.
2. **Ask targeted alignment questions.** One at a time. Keep terse.
   - What should the learner be able to *do* at the end? (action verbs only — never "understand" / "know")
   - How will each objective be assessed?
   - What practice should precede the assessment?
   - What content teaches the practice?
3. **Draft the 4-column O-A-P-P table.**
4. **Run quality checklist** (see `docs/reference/content-mapping-best-practices.md`):
   - Every objective starts with an action verb
   - NO "understand", "know", "be aware of", "appreciate"
   - Every assessment is concretely specifiable (MCQ, scenario, performance task)
   - Every row's alignment is end-to-end (no gaps, no "nice to know" padding)
   - Scope fits duration target (~1 objective per 8–10 min)
5. **Write output** to `modules/<module-slug>/content-map.md`.
6. **Stop for review.** Present the table. Ask user to verify alignment, scope, action verbs. Do NOT auto-trigger the next skill.
7. **On approval**, git auto-commit:
   ```bash
   cd ~/Desktop/elearning-skills && git add modules/<slug>/content-map.md && git commit -m "G1: content-map approved for <slug>"
   ```

## Output format

```markdown
# Module <id> — <title>

**Target learner:** <description>
**Duration target:** ~<n> min
**Assessment strategy:** <summary>

| Objective | Assessment | Practice | Presentation |
|-----------|------------|----------|--------------|
| **<verb>** ... | <type + content> | <description or —> | <content summary> |
```

## Rules

1. One question at a time during dialogue.
2. Action verbs only for objectives.
3. Every row must align end-to-end.
4. Max ~6 objectives for a 30-min module.
5. Output goes to file, not chat.
6. Stop after writing. Do not auto-trigger `/storyboard`.

## Reference files

- `docs/reference/content-mapping-best-practices.md`
