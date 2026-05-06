---
name: content-map
description: Use when starting a new eLearning module — turns a brief, lesson plan, or seed content into a 4-column O-A-P-P (Objective / Assessment / Practice / Presentation) alignment table. First skill in the eLearning pipeline.
---

# /content-map

## Overview

Transforms a lesson brief into a tight alignment table. Every row links one learning objective to its assessment, practice, and presentation content. This skill owns instructional alignment and scope only; it does **not** storyboard screens, assign layout IDs, write slide copy, or decide implementation details.

## When to use

- User invokes `/content-map`
- User asks to "map out content" / "plan a module" / "build a course on X"

## Input

Any of:
- A one-line brief with topic, audience, and duration
- A lesson plan document (PDF, Word, pasted text)
- A seed example + user's ID intuition

## Workflow

1. **Parse the input.** Identify topic, audience, scope, duration target.
2. **Ask targeted alignment questions.** One at a time. Keep terse.
   - What should the learner be able to *do* at the end? (action verbs only — never "understand" / "know")
   - What Bloom level does that verb imply: Remember, Understand, Apply,
     Analyze, Evaluate, or Create?
   - How will each objective be assessed?
   - What practice should precede the assessment?
   - What content teaches the practice?
3. **Draft the 4-column O-A-P-P table.** The Presentation column must describe the teaching treatment and sequencing logic at a learning-design level, not individual screens.
4. **Run quality checklist** (see `docs/reference/content-mapping-best-practices.md`):
   - Every objective starts with an action verb
   - NO "understand", "know", "be aware of", "appreciate"
   - Every objective has an explicit or inferable Bloom level
   - Every assessment is concretely specifiable (MCQ, scenario, performance task)
   - Every assessment and practice activity matches the objective's Bloom level
   - Every row's alignment is end-to-end (no gaps, no "nice to know" padding)
   - Scope fits duration target (~1 objective per 8–10 min)
   - Presentation column passes the instructional sequencing check (see below)
5. **Write output** to `modules/<module-slug>/content-map.md`.
6. **Generate Word doc** for stakeholder review:
   ```bash
   python3 ~/Desktop/elearning-skills/scripts/generate_content_map_docx.py ~/Desktop/elearning-skills/modules/<slug>
   ```
7. **Open the .docx** for the user to review. Do NOT present the table in chat — the artifact lives in the file.
8. **Stop for review.** Ask user to verify alignment, scope, and instructional sequencing. Do NOT auto-trigger the next skill.
9. **On approval**, git auto-commit:
   ```bash
   cd ~/Desktop/elearning-skills && git add modules/<slug>/ && git commit -m "G1: content-map approved for <slug>"
   ```

## Presentation Column Rules

The Presentation column is NOT a vague topic label ("Definition + compare"). It is an instructional treatment note that tells the next agent what needs to be taught, in what conceptual order, and why.

Each cell in the Presentation column must specify:
- **Teaching move** — activate, introduce, contrast, model, worked example, practice bridge, summarize, etc.
- **Essential content** — the concepts, examples, misconceptions, or decision criteria that must appear later.
- **Sequencing rationale** — why this content should come before or after related content.

Each cell must avoid:
- Slide numbers
- Layout IDs
- Screen-by-screen copy
- Visual wireframe instructions
- HTML, CSS, SCORM, or implementation details

### Instructional Sequencing Checklist

Apply these principles when deciding the learning sequence:

1. **Activate before introduce.** Before teaching something new, connect to what the learner already knows.
2. **Framework before details.** Before dumping 5+ items, give the learner a way to organize them in memory.
3. **Contrast, don't just define.** Don't define concept A in isolation. Show concept A next to concept B so the learner sees the boundary.
4. **Practice bridges objectives.** If Objective 3 requires knowledge from Objective 2, embed Objective 3's practice inside Objective 2's exploration.
5. **One idea per teaching move.** If a presentation note tries to do two cognitive jobs, split the treatment into separate moves for the storyboard agent.

## Output format

```markdown
# Module <id> — <title>

**Target learner:** <description>
**Duration target:** ~<n> min
**Assessment strategy:** <summary>

| Objective | Assessment | Practice | Presentation |
|-----------|------------|----------|--------------|
| **<verb>** ... | <type + content> | <description or —> | <teaching move + essential content + sequencing rationale> |

## Quality checklist
- [x] / [ ] items...

## Notes
- Cognitive sequencing rationale
- Cross-objective bridges
```

Output file: `modules/<slug>/content-map.md` + `modules/<slug>/content-map.docx`

## Rules

1. One question at a time during dialogue.
2. Action verbs only for objectives.
3. Include Bloom level inline in the Objective cell when it affects assessment
   design, e.g. `**Analyze** ... (Bloom: Analyze)`.
4. Every row must align end-to-end, including Bloom-level match between
   objective, practice, and assessment.
5. Max ~6 objectives for a 30-min module.
6. **Output goes to .md + .docx files, not chat.** Open the .docx for the user.
7. **Presentation column must be instructionally specific but not slide-specific.**
8. Stop after writing. Do not auto-trigger `/storyboard`.

## Reference files

- `docs/reference/content-mapping-best-practices.md`
