---
name: storyboard
description: Use after /content-map approval — turns the approved instructional map into an eLearning storyboard with screen flow, canonical layouts, interaction states, voiceover, visual notes, and developer notes. Second skill in the eLearning pipeline.
---

# /storyboard

## Overview

Transforms an approved content map into a screen-level eLearning storyboard.
This skill owns learning experience design: screen order, canonical layout
choices, interaction states, voiceover, visual/graphic direction, and developer
notes.

It does **not** build the production HTML module, package SCORM, or revise the
instructional alignment unless the content map has a clear gap that must be sent
back to `/content-map`.

## When to use

- User invokes `/storyboard`
- User asks to storyboard an approved module/content map
- User wants PPT-based storyboard cards, HTML-based storyboard review, or both

## Input

Required:
- `modules/<slug>/content-map.md` approved at G1

Optional:
- Source documents or examples referenced by the content map
- Brand/layout reference files
- Existing storyboard PPT to revise

## Outputs

Write storyboard artifacts under the module folder:

```text
modules/<slug>/
  storyboard/
    storyboard.md          # canonical screen-level spec
    storyboard.json        # optional structured version for /build-html
    prototype/             # optional temporary HTML-first review prototype
  storyboard.pptx          # stakeholder review artifact when requested/needed
```

Do not write:
- `modules/<slug>/content/*.md`
- `modules/<slug>/build/`
- `modules/<slug>/dist/`

Those belong to later skills.

## Workflow

1. **Read the approved content map.** Extract objectives, assessments,
   Bloom levels when present, practice moments, teaching moves, sequencing
   rationale, and scope.
2. **Flag alignment gaps.** If objectives, assessment, practice, or presentation
   do not align, stop and ask the user whether to return to `/content-map`.
3. **Create the screen flow.** Decide screen count, order, page types, and
   transitions. Preserve the content map's instructional sequence unless there
   is a stated reason to adjust it.
4. **Map screens to canonical layouts.** Assign layout IDs from
   `docs/reference/layout-contract.md`; do not duplicate or invent layout
   language inside the storyboard.
5. **Specify interaction states.** Include defaults, selected/submitted states,
   pop-up layers, visited states, feedback states, disabled/enabled navigation,
   and completion behavior.
6. **Run the lesson-end practice and assessment gate.** Before each lesson or
   small module summary, confirm that the lesson includes active practice and an
   assessment checkpoint aligned to the objective's Bloom level. If MCQs are the
   assessment format, provide two L09 questions by default and follow
   `skills/mcq/SKILL.md`.
7. **Write notes.** For every screen include:
   - On-screen content
   - Voiceover
   - Visual/graphic description
   - Interaction and developer notes
8. **Use HTML-first prototype if helpful.** Keep it inside
   `storyboard/prototype/` and label it as a storyboard review prototype, not a
   production build.
9. **Generate PPT artifact when needed.** Use `storyboard-template.py` or a
   module-specific generator to produce `modules/<slug>/storyboard.pptx`.
10. **Present a summary table** with screen ID, title, layout, type, and review
   notes.
11. **Stop for G2 storyboard review.** Ask the user to approve the screen flow,
   interactions, wording level, and review artifact. Do not auto-trigger
   `/build-html`.
12. **On approval**, git auto-commit:
   ```bash
   cd ~/Desktop/elearning-skills && git add modules/<slug>/storyboard/ modules/<slug>/storyboard.pptx && git commit -m "G2: storyboard approved for <slug>"
   ```

## Output Contract

Write `storyboard/storyboard.md` using
`docs/reference/storyboard-output-contract.md`.

## Interaction Rules

### Standard content screens

One storyboard screen per learner-visible screen. Keep each screen to one
instructional job.

### Anchor + pop-up screens

When the learning experience uses click-to-explore or menu-hub behavior:

- Include the anchor screen.
- Include one pop-up/layer state per topic.
- Include an anchor visited-state screen when visited tracking matters.
- Specify close behavior, visited indicators, disabled/enabled Continue states,
  and any internal interactions.

### Assessments

For MCQ, scenario, drag/match, and similar interactions:

- Include the default learner state.
- Include selected/submitted behavior.
- Include correct and incorrect feedback states.
- Specify score contribution and completion implications.

For MCQs:

- Use `skills/mcq/SKILL.md` for item-writing rules and L09 state notes.
- Provide two MCQs per lesson or small module checkpoint by default unless the
  content map, duration, or user request specifies otherwise.
- Use scenario-based MCQs when the objective requires Apply, Analyze, or
  Evaluate-level judgement.

## Rules

1. Storyboard output is screen-level, not SCORM/build-level.
2. Do not write production `content/*.md` or `build/` files.
3. Every screen must have a canonical `layout`, interaction type, and
   objective/practice alignment reference.
4. Every assessment must include feedback behavior.
5. Every lesson or small module must include at least one active practice before
   its summary, aligned to the objective's Bloom level.
6. Every lesson or small module must include an assessment checkpoint before its
   summary. When the checkpoint is MCQ-based, provide two MCQs by default.
7. Every pop-up/menu interaction must include default, layer, and visited states
   when those states affect the learner or developer.
8. HTML-first prototypes are allowed only as storyboard review/prototyping
   artifacts under `storyboard/prototype/`.
9. Stop after G2 storyboard artifacts are written. Do not auto-trigger
   `/build-html`.

## Storyboard Design Principles

Use these principles as design judgment, not as a checklist to copy into every
module. The goal is to create a learner-facing experience that is coherent,
useful, buildable, and faithful to the approved content map.

### 1. Design from learner cognition, not slide inventory

Every screen must earn its place by doing at least one learning job: reducing
confusion, building a mental model, creating contrast, enabling practice, or
supporting transfer to real work. Do not add screens simply because a source has
another paragraph, list, or heading. When the audience is experienced, consider
opening a lesson with a short challenge, misconception check, or ordering task
that activates prior knowledge before objectives or content.

When a lesson depends on a realistic situation, introduce the case facts once
and reuse them across downstream practice. A stable case set, bid set, customer
profile, project brief, or data snapshot lets later activities test judgement
instead of asking learners to re-orient each time.

### 2. Make structure visible through interaction

Use interactive structure when exploration is itself the learning move. A
click-to-reveal menu, tab set, accordion, hotspot, or labelled graphic can serve
as both overview and detail access. Do not add a duplicate static overview before
an interactive screen unless it teaches a different relationship, such as timing,
dependencies, sequence, or before/after contrast. If a separate overview is
needed, explain why in the developer notes.

For process content, make the order and position visually legible. First show
where the process sits in the larger lifecycle when that context changes how the
learner interprets the steps, then zoom into the process itself. Choose a visual
form that expresses the relationship being taught: timeline for sequence, loop
for iteration, swimlane for role handoffs, funnel for narrowing decisions, or
map/checkpoint metaphor for a journey.

When responsibility boundaries are part of the learning, include a role map or
hotspot. Group roles by the content's logic, such as client, advisor, approver,
operator, regulator, or other specialist contributors, and give each group a
small set of concrete responsibilities. Flag role boundaries for SME validation
when they are inferred or jurisdiction-specific.

### 3. Teach through consequential practice

Each lesson should include active practice tied to the learning objective, not
only a final check. Choose the practice type based on the learner decision being
trained: scenarios for judgement and tradeoffs, matching or ordering for
relationships and sequence, and MCQs for targeted conceptual checks. Practice
should appear close enough to the teaching moment that learners can apply the
idea while it is still live. A pre-challenge can count as practice only when it
requires a real learner decision and includes feedback that sets up the lesson.

For senior judgement skills, prefer practice that models how an expert thinks:
branching roleplay, dialogue simulation, case review, or consequence-based
scenario. A strong simulation usually has a diagnostic choice, an advisor/client
response, a second action choice, and a key insight that explains the reasoning.
Use one-off MCQs only when the intended skill is a focused concept check.

### 4. Preserve source integrity without weakening learner copy

Learner-facing copy should be confident, clear, and useful. If the storyboard
synthesises content from context, fills a gap, or makes an instructional
inference that needs SME review, record that in the review/developer notes
rather than diluting the learner screen with caveats. Name what was synthesised
and what should be validated.

Do not invent best-practice principles, policy rules, or professional doctrine
just to make a screen feel complete. If a principle is not explicitly sourced,
teach the underlying judgement through sourced scenarios, evidence, and
consequences, then add SME questions in the review notes.

### 5. Use information architecture to reduce cognitive load

Parallel topics should feel parallel. When multiple screens, reveals, or popups
describe comparable concepts, use a repeated frame so learners can scan for the
difference instead of relearning the structure. Choose the frame from the
content's logic: definition/source/use, risk/control/evidence, role/action/output,
definition/importance/role, what-happens/how-we-support, or another pattern that
fits the material. Do not hard-code a frame that the content does not naturally
support.

For dense comparisons, do not force all content onto a static two-column screen.
Use tabs, accordions, button reveals, or click-to-expand when progressive
disclosure will reduce load. Keep the visible layer to about 4-6 bullets and
move detail into reveals, notes, or follow-on practice.

### 6. Prefer build-native interactions

Storyboard interactions should map cleanly to the target authoring environment.
Use buttons, tabs, accordions, hotspots, labelled graphics, scenario blocks, or
other native components when they can express the intended learning move. Avoid
specifying bespoke overlays as the only build path when the target tool would
more naturally use a native reveal pattern. For complex branching, add
reviewer-only diagrams that show branches, choices, feedback, state logic, and
completion behavior.

Avoid making every exploration a must-visit-all gated tile set. Use completion
gating only when required for learning, compliance, or assessment logic; otherwise
let senior learners move through the interaction with purposeful friction.

### 7. Create programme coherence

For multi-lesson courses, design the course as one learning journey rather than
a bundle of lessons. Use purposeful scaffolding, clear module transitions,
completion rules, and a final throughline that reframes the individual lessons
as one professional capability. Reviewer-only notes are appropriate when they
clarify build assumptions, SME review focus, source gaps, or interaction wiring;
mark them clearly as not learner-facing.

## Reference Files

- `docs/reference/layout-contract.md` — authoritative layout registry
- `docs/reference/storyboard-output-contract.md`
- `docs/reference/content-mapping-best-practices.md`
- `storyboard-template.py`
