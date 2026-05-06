# Storyboard Output Contract

Use this contract for `modules/<slug>/storyboard/storyboard.md`.

## Required Structure

```markdown
# Storyboard — <module title>

## Module metadata
- Module ID: <slug>
- Target learner: <description>
- Duration target: <n> min
- Source content map: modules/<slug>/content-map.md

## Screen list

| Screen ID | Title | Layout | Type | Notes |
|-----------|-------|--------|------|-------|
| 01 | <title> | L13 | objectives | <review note> |

## Screens

### 01 — <title>

**Layout:** <canonical layout ID>
**Type:** <screen type>
**Objective alignment:** <objective or row reference>

**On-screen:**
- <learner-facing text>

**Voiceover:**
<narration or "None/minimal">

**Visual/graphic description:**
<what the learner sees, including hierarchy and media direction>

**Interaction & dev notes:**
- <states, branching, navigation, scoring, tracking>
```

## Required Screen Fields

Every learner-visible screen must include:
- Screen ID
- Title
- Canonical layout ID from `docs/reference/layout-contract.md`
- Screen type
- Objective/practice/assessment alignment reference
- On-screen content
- Voiceover or minimal/no-VO note
- Visual/graphic direction
- Interaction and developer notes

## Interaction State Requirements

For menu, popup, assessment, scenario, drag/match, and similar interactive
screens, specify:
- Default state
- Selected/open/submitted state
- Feedback or consequence state, where applicable
- Visited/completed state, where applicable
- Continue gating and completion behavior

## Review Notes

Use review/developer notes for:
- SME validation flags
- Source-gap notes
- Build assumptions
- Reviewer-only diagrams or non-learner-facing logic maps
- Any temporary adaptation from the canonical layout contract
