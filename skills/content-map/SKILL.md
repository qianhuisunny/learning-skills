---
name: content-map
description: Use when starting a new eLearning module — turns a brief, lesson plan, or seed content into a 4-column O-A-P-P (Objective / Assessment / Practice / Presentation) alignment table with cognitive sequencing. First skill in the eLearning pipeline.
---

# /content-map

## Overview

Transforms a lesson brief into a tight alignment table. Every row links one learning objective to its assessment, practice, and presentation content — with the Presentation column specifying **slide-by-slide sequence, layout IDs, and cognitive processing strategy**. Forces alignment AND sequencing thinking BEFORE any storyboard or slide design.

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
3. **Draft the 4-column O-A-P-P table.** The Presentation column must be slide-level specific (see Presentation Column Rules below).
4. **Run quality checklist** (see `docs/reference/content-mapping-best-practices.md`):
   - Every objective starts with an action verb
   - NO "understand", "know", "be aware of", "appreciate"
   - Every assessment is concretely specifiable (MCQ, scenario, performance task)
   - Every row's alignment is end-to-end (no gaps, no "nice to know" padding)
   - Scope fits duration target (~1 objective per 8–10 min)
   - Presentation column passes the cognitive sequencing check (see below)
5. **Write output** to `modules/<module-slug>/content-map.md`.
6. **Generate Word doc** for stakeholder review:
   ```bash
   python3 ~/Desktop/elearning-skills/scripts/generate_content_map_docx.py ~/Desktop/elearning-skills/modules/<slug>
   ```
7. **Open the .docx** for the user to review. Do NOT present the table in chat — the artifact lives in the file.
8. **Stop for review.** Ask user to verify alignment, scope, cognitive sequencing. Do NOT auto-trigger the next skill.
9. **On approval**, git auto-commit:
   ```bash
   cd ~/Desktop/elearning-skills && git add modules/<slug>/ && git commit -m "G1: content-map approved for <slug>"
   ```

## Presentation Column Rules

The Presentation column is NOT a vague content description ("Definition + side-by-side compare"). It is a **slide-by-slide instructional sequence** that someone can read and know exactly what page 1 says, what page 2 says, and WHY they're in that order.

Each cell in the Presentation column must specify:
- **Slide number and layout ID** (e.g., "Slide 3 (L03):")
- **What the learner sees** on that slide (content summary, not just a label)
- **Cognitive purpose** — why this slide is HERE in the sequence, not somewhere else

### Cognitive sequencing checklist

Apply these principles when deciding slide order:

1. **Activate before introduce.** Before teaching something new, connect to what the learner already knows. ("You already use a project plan. What does it cover?" → THEN introduce procurement plan.)
2. **Framework before details.** Before dumping 5+ items, give the learner a way to organize them in memory. (Chunk 8 components into 3 phases → THEN show the menu hub.)
3. **Contrast, don't just define.** Don't define concept A in isolation. Show concept A next to concept B so the learner sees the boundary. ("Project plan asks WHAT/WHEN. Procurement plan asks HOW/FROM WHOM.")
4. **Practice bridges objectives.** If Objective 3 requires knowledge from Objective 2, embed Objective 3's practice INSIDE Objective 2's exploration. (Contract-type popup teaches the decision criteria → MCQ asks learner to apply them.)
5. **One idea per slide.** If a slide tries to do two cognitive jobs, split it.

### Bad vs good Presentation column

**Bad (vague, no sequencing, no cognitive rationale):**
```
Definition + side-by-side compare
```

**Good (slide-level, sequenced, cognitive purpose clear):**
```
Slide 2 (L01): Activate prior knowledge — "You already use a project plan.
What does it cover?" List familiar project-plan elements.
Slide 3 (L03): Introduce the new concept — "A procurement plan answers a
different question: how will we buy?" Definition + visual showing procurement
plan as a subset document.
Slide 4 (L01): Contrast — side-by-side: "Project plan asks WHAT/WHEN.
Procurement plan asks HOW/FROM WHOM." 3 concrete scope examples per column.
```

## Output format

```markdown
# Module <id> — <title>

**Target learner:** <description>
**Duration target:** ~<n> min
**Assessment strategy:** <summary>

| Objective | Assessment | Practice | Presentation |
|-----------|------------|----------|--------------|
| **<verb>** ... | <type + content> | <description or —> | **Slide N (LXX):** what + why. **Slide N+1 (LXX):** what + why. |

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
3. Every row must align end-to-end.
4. Max ~6 objectives for a 30-min module.
5. **Output goes to .md + .docx files, not chat.** Open the .docx for the user.
6. **Presentation column must be slide-level specific with cognitive rationale.** No vague summaries.
7. Stop after writing. Do not auto-trigger `/storyboard`.

## Reference files

- `docs/reference/content-mapping-best-practices.md`
- `shell/content.schema.md` — for layout field shapes (so Presentation column references correct layout IDs)
