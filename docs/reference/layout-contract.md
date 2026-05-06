# Layout Contract

**Authoritative source of truth:** this file is the only canonical layout
registry for the repo. When another document describes components, visual style,
or historical layout ideas, treat it as non-authoritative unless it points back
to this contract.

This repo has one canonical layout registry. Storyboards and the HTML runtime are
two implementations of that same registry.

The source of truth is not "what the PPT template currently has" or "what the
shell currently renders." The source of truth is the set of reusable eLearning
screen patterns required by the product.

## First Principles

A layout exists when it represents a distinct instructional or interaction
pattern that recurs across modules:

- Explain one idea
- Pair an idea with media
- Compare two choices or concepts
- Show a set of peer concepts
- Show a process or sequence
- Let the learner explore a menu
- Ask the learner to choose, match, classify, or decide
- Summarize and complete

The canonical registry is the union of those recurring patterns. If either
storyboard or runtime is missing one, that side has an implementation gap.

## Canonical Registry

| ID | Canonical pattern | Storyboard status | Runtime status |
|---|---|---|---|
| L01 | Text / single-column explanation | Implemented | Implemented |
| L02 | Hero / section intro | Implemented | Implemented |
| L03 | Media left + text right | Implemented | Implemented |
| L04 | Text left + media right | Implemented | Implemented |
| L05 | 3-up cards / peer concepts | Implemented | Implemented |
| L06 | Compare 2-up | Implemented | Implemented |
| L07 | Stepper | Implemented | Implemented |
| L08 | Timeline | Implemented | Implemented |
| L09 | MCQ knowledge check | Implemented | Implemented |
| L10 | Scenario choice | Implemented | Implemented |
| L11 | Drag/match | Implemented | Implemented |
| L12 | Menu / click-to-explore | Implemented | Implemented |
| L13 | Objectives / agenda | Implemented | Implemented |
| L14 | Summary / completion | Implemented | Implemented |
| popup | L12 popup layer | Implemented as storyboard state | Implemented as runtime overlay |

## Global Design Defaults

These defaults apply to storyboard artifacts and production HTML unless a module
has an explicit, approved brand override.

### Canvas And Limits

- Canvas: 16:9 widescreen.
- Storyboard reference canvas: 1920 x 1080 px.
- Safe margins: 5% on all sides.
- Max content per screen: one instructional idea, about 150 words, and 7 +/- 2
  visible elements.
- Default fallback layout: L01 when the intended instructional pattern is truly
  unclear.

### EY-Parthenon Branding Notes

The historical palette used for this workspace is a blue-led EY-Parthenon look,
with EY yellow reserved as an accent rather than the dominant color.

| Role | Name | Hex | RGB | Usage |
|---|---|---|---|---|
| Primary | EY-Parthenon blue | `#1A9AFA` | 26, 154, 250 | Headers, titles, accent bars, component bars, primary CTAs |
| Secondary | EY yellow accent | `#FFE600` | 255, 230, 0 | Sparing EY co-branding or emphasis |
| Neutral | Charcoal | `#2C3E50` | 44, 62, 80 | Body text and primary text |
| Neutral | Dark gray | `#4A4A4A` | 74, 74, 74 | Secondary text and labels |
| Neutral | Medium gray | `#7F8C8D` | 127, 140, 141 | Captions and muted text |
| Neutral | Light gray | `#D5D8DC` | 213, 216, 220 | Borders, dividers, inactive UI |
| Neutral | Faint gray | `#F4F6F7` | 244, 246, 247 | Card backgrounds and panels |
| Background | White | `#FFFFFF` | 255, 255, 255 | Light-theme slide background |
| Feedback | Success green | `#27AE60` | 39, 174, 96 | Correct feedback |
| Feedback | Error red | `#C0392B` | 192, 57, 43 | Incorrect feedback |

Color rules:
- Use EY-Parthenon blue for titles, section headers, accent bars, component
  bars, icons, buttons, and interactive affordances.
- Use charcoal for body copy in light-theme artifacts.
- Use light gray for borders, dividers, and inactive UI.
- Use EY yellow sparingly; do not make it the primary UI color.

### Typography Notes

| Element | Font | Weight | Size | Line height | Color |
|---|---|---|---|---|---|
| Slide title | EYInterstate | Bold | 32 pt | 40 pt | `#1A3E6F` |
| Section heading | EYInterstate | Bold | 24 pt | 32 pt | `#1A3E6F` |
| Body copy | EYInterstate | Regular | 18 pt | 28 pt | `#2C3E50` |
| Card/module text | EYInterstate | Light | 14 pt | 22 pt | `#4A4A4A` |
| Captions/labels | EYInterstate | Light | 12 pt | 18 pt | `#7F8C8D` |
| Button text | EYInterstate | Bold | 14 pt | n/a | white on blue |

Typography rules:
- Fallback font: Arial or Helvetica.
- Use no more than two font weights on a single screen.
- Minimum font size: 12 pt in PowerPoint/storyboard artifacts.
- Prefer sentence case for body text and bullets. Slide title casing should
  follow the active brand/style guide for the module.

## Available Components

These are component-level affordances that can be mapped into the canonical
layout IDs above. They are not separate layout IDs.

Presentation components:
- Audio, code, dialog, GIF, graphic, icon, iframe, media, media grid, table,
  text, text and graphic, video stream.

Interaction components:
- Accordion, tabs, flip card / single flip card, gallery, hot graphic /
  hotspots, image slider, infographic, interactive video, links, narrative,
  text reveal, role hotspot, dialogue simulation / roleplay.
- Input-style components: checkbox group, radio group, select, number input,
  text area, open input, sliders / confidence sliders, survey, checklist,
  action button.

Question components:
- Branching, drag and drop, matching, ordering, sorting, multiple choice
  including graphic MCQ, text input, game, card drop, branching dialogue
  simulation.

## Canonical Layout Details

The registry above is authoritative. The following detail defines the expected
structure, content limits, and usage guidance for each canonical layout.

### Core Content Layouts

#### L01: Text / Single-Column Explanation

- Structure: single full-width column, vertically stacked.
- Anatomy: title, body text, optional bullets.
- Body limit: about 120-160 words or 6-8 lines.
- Spacing: 5% side margins; about 24 px between title and body.
- Use for: definitions, introductions, explanations, policy statements, and
  text-heavy content without visuals.

#### L02: Hero / Section Intro

- Structure: single column with hero media above body content.
- Anatomy: hero image/banner, subheading, body, optional CTA.
- Hero aspect ratio: 16:9.
- Body limit: about 60-80 words or 3-4 lines.
- CTA location: bottom-right or bottom-center.
- Use for: module openers, section intros, high-impact announcements, welcome
  screens.

#### L03: Media Left + Text Right

- Structure: two columns, left 60% media and right 40% text.
- Anatomy: media on left; heading, body, and optional bullets on right.
- Body limit: about 80-100 words or 4-5 lines.
- Bullets: optional, max 3-4 items.
- Media aspect ratio: 4:3 or 16:9.
- Use for: concept explanation with visual support, feature highlights, process
  introductions.

#### L04: Text Left + Media Right

- Structure: two columns, left 40% text and right 60% media.
- Anatomy: heading, body, and optional bullets on left; media on right.
- Body limit: about 80-100 words or 4-5 lines.
- Bullets: optional, max 3-4 items.
- Media aspect ratio: 4:3 or 16:9.
- Use for: concept explanation with visual support and case-study
  introductions.

#### L05: 3-Up Cards / Peer Concepts

- Structure: three equal columns, horizontally centered.
- Card anatomy: icon, heading, short body.
- Icon size: about 60 x 60 px.
- Body limit: max two lines per card.
- Spacing: about 24 px between cards.
- Use for: key concepts, module overviews, benefits/features, and small sets of
  peer concepts.

#### L06: Compare 2-Up

- Structure: two equal columns, side by side.
- Column anatomy: header, parallel bullet list, optional icon.
- Bullets: 3-5 parallel items per column.
- Spacing: about 16 px between columns and 12 px between bullets.
- Use for: pros/cons, before/after, option A vs option B, and method
  comparisons.

### Process / Sequence Layouts

#### L07: Stepper

- Structure: horizontal sequence of steps with connectors.
- Preferred count: 3-5 steps. More steps are allowed only when the template and
  runtime can render them without overflow.
- Step anatomy: number circle, label, short caption.
- Caption limit: 1-2 lines.
- Connector: horizontal line or arrow between steps.
- Use for: sequential processes, workflows, phase overviews, and how-to steps.

#### L08: Timeline

- Structure: vertical line with nodes.
- Preferred count: 4-6 nodes.
- Node anatomy: marker, date/label, short content.
- Content limit: 2-3 lines per node.
- Spacing: about 40 px vertical gap between nodes.
- Use for: project phases, historical progression, milestones, and
  chronological events.

### Interaction / Practice Layouts

#### L09: MCQ Knowledge Check

- Structure: stem at top, options in the middle, feedback after submission.
- Anatomy: question stem, 4 options, feedback area, submit button.
- Item-writing guidance: use `skills/mcq/SKILL.md` for Bloom alignment,
  parallel answer construction, scenario-based MCQs, distractor quality, and
  feedback rationale.
- Stem limit: 2-3 lines.
- Option limit: 1-2 lines per option.
- Feedback limit: about 3 lines.
- Use for: formative checks, quizzes, recall, and concept checks.
- States:
  - Default: options visible, feedback hidden, submit inactive until selection.
  - Selected: chosen option highlighted.
  - Submitted: options disabled, feedback shown.
  - Retry: optional reset to default.
- Branching: linear unless the storyboard specifies a hint or remediation layer.

#### L10: Scenario Choice

- Structure: scenario prompt/context plus choices and consequence.
- Anatomy: context panel, 2-3 choices, consequence panel, continue CTA.
- Context limit: 3-4 lines.
- Choice limit: max 2 lines per choice.
- Consequence limit: about 3 lines plus feedback.
- Use for: decision-based scenarios, branching simulations, application
  exercises, and judgement calls.
- Roleplay / dialogue simulation variant: use L10 across multiple linked
  screens or states to model a realistic exchange. Typical structure is case
  setup, round 1 diagnostic choice, advisor/client response, round 2 action
  choice, and key insight end state. Choices should have meaningful consequences
  such as Good, Redirect, or Try again rather than simple recall correctness.
- Reviewer-only diagram: complex branching simulations should include a
  non-learner-facing interaction map showing branches, feedback, state logic,
  completion conditions, and any reusable case facts.
- States:
  - Default: context visible, choices enabled, consequence hidden.
  - Hover: choice affordance highlighted.
  - Selected: other choices disabled, consequence revealed.
  - Consequence: outcome and continue CTA shown.
- Branching: specify destination per choice when the scenario branches.

#### L11: Drag/Match

- Structure: instruction bar, draggable items, drop targets, feedback.
- Anatomy: instruction, 4-6 draggable cards, 4-6 targets, submit, feedback.
- Item limit: 1-2 lines per draggable item.
- Use for: matching, categorization, sequencing, and term-definition pairing.
- States:
  - Default: items in source area, targets empty.
  - Dragging: item follows cursor and target highlights.
  - Dropped: item snaps to target.
  - Complete: all items placed and submit activates.
  - Feedback: correct/incorrect per item plus overall feedback.
- Branching: linear unless a retry/remediation threshold is specified.

### Navigation / Framing Layouts

#### L12: Menu / Click-To-Explore

- Structure: a menu of clickable items that reveal detail content.
- Accepted shapes: vertical bar list, grid, buttons, tabs, accordion, or labelled
  graphic, chosen for the build target and content type.
- Preferred repo pattern for process/pathway anchors: full-width vertical bars
  with numbers, labels, visited states, and optional Continue unlock.
- Grid use: acceptable for dashboards, module selection, or peer topics where a
  grid is more scannable than a sequence.
- Item count: usually 4-8 items.
- Use for: topic menus, module selection, click-to-reveal, lesson navigation,
  and dashboard/home screens.
- States:
  - Default: items unvisited.
  - Open/reveal: selected item displays detail layer/block.
  - Visited: selected item receives a visited indicator.
  - Complete: Continue unlocks when required items are visited.

#### popup: L12 Popup Layer

- Structure: detail layer/state launched from an L12 item.
- Anatomy: anchor context, close/back affordance, title, body, optional bullets,
  media, key message, or nested content.
- Use for: storyboard state representation and runtime overlays.
- Build note: in Rise-style tools, the production equivalent may be an
  accordion row, tab panel, button reveal, or labelled-graphic hotspot rather
  than a literal modal overlay.

#### L13: Objectives / Agenda

- Structure: single column with 3-5 stacked objective rows.
- Row anatomy: optional icon/number plus objective text.
- Objective limit: 1-2 lines per objective.
- Use for: learning objectives, agendas, "what you'll learn", and module goals.

#### L14: Summary / Completion

- Structure: heading, key takeaways, CTA.
- Takeaway count: 3-5 concise takeaways. Use more only when a programme summary
  needs a throughline plus module-level recap.
- Takeaway limit: 1-2 lines each.
- CTA location: bottom-right or bottom-center.
- Use for: module wrap-up, section summary, lesson recap, transition, and final
  completion screen.

## Layout Rules

- Grid: use a 12-column grid or clear proportional split such as 60/40.
- Margins: use fixed safe margins, usually 5-7%.
- Text limits: enforce max lines per region; split content when it does not fit.
- Image ratios: 16:9 for hero media, 4:3 for inline media, square for icons.
- Default fallback: L01 if unsure.
- One interaction type per screen.
- CTAs should appear at the bottom-right or bottom-center, not in the top half
  of the screen.

## Page Type To Layout Mapping

| Page type | Allowed layouts |
|---|---|
| Learning objectives | L13 or L05 |
| Concept explanation | L01 / L03 / L04 |
| Process / how-to | L07 or L08 |
| Compare options | L06 |
| Menu / module select | L12 |
| MCQ knowledge check | L09 |
| Scenario decision | L10 |
| Branching roleplay / simulation | L10 |
| Drag/match, ordering, classification | L11 |
| Wrap-up / summary | L14 |
| Hero / section intro | L02 |

## Component To Layout Mapping

| Layout | Primary components | Avoid |
|---|---|---|
| L01 | Text | Media, interactive elements |
| L02 | Text, media hero, action button | Multiple CTAs |
| L03 | Text and graphic, media, video stream | More than one media item |
| L04 | Text and graphic, media, video stream | More than one media item |
| L05 | Flip card, icon, text | Accordion, video |
| L06 | Text, icon | Complex interactive components |
| L07 | Icon, text | Media, long descriptions |
| L08 | Text, icon | Horizontal layout when chronology is vertical |
| L09 | Multiple choice, radio group | Decorative graphics, video |
| L10 | Branching, dialogue simulation, roleplay, advisor response, key insight, action button | MCQ-style recall options |
| L11 | Drag and drop, matching, ordering, sorting | Text-heavy content |
| L12 | Action button, icon, graphic, tabs, accordion, hotspots | Long text in the menu items |
| popup | Text, media, key message, nested reveal | Treating popups as standalone production slides |
| L13 | Icon, text | Media, interactions |
| L14 | Text, action button | New content introduction |

## Placeholder Naming Convention

Use standardized placeholder names in storyboard specs and templates when
content is not final:

| Placeholder | Description | Example |
|---|---|---|
| `{{TITLE}}` | Slide/screen title | `Planning procurement` |
| `{{SUBTITLE}}` | Optional subtitle or section label | `Module 2 of 6` |
| `{{BODY}}` | Main text block | Paragraph content |
| `{{BULLETS}}` | Bulleted list items | `- Item 1\n- Item 2` |
| `{{MEDIA_1}}`, `{{MEDIA_2}}` | Numbered images/videos | `[Image: workflow diagram]` |
| `{{ICON_1}}`, `{{ICON_2}}` | Numbered icons | `[Icon: checklist]` |
| `{{STEM}}` | Assessment question text | `Which model is best for...?` |
| `{{OPT_A}}`-`{{OPT_D}}` | Answer options | `Design-Bid-Build` |
| `{{FEEDBACK_CORRECT}}` | Correct feedback | `That's right...` |
| `{{FEEDBACK_INCORRECT}}` | Incorrect feedback | `Not quite...` |
| `{{CTA}}` | Button text | `Continue` |
| `{{NARRATION}}` | Voiceover script | Full VO script |
| `{{DEV_NOTES}}` | Developer/build notes | Trigger and state notes |

## Anti-Patterns

| Do not | Why | Use instead |
|---|---|---|
| Put MCQ (L09) with decorative graphics | Distracts from the question and clutters the layout | Clean L09; save graphics for content slides |
| Exceed 3-5 concise takeaways on L14 | Defeats the purpose of a summary | Pick the highest-value takeaways |
| Use L05 cards for more than 3 items | Cards become narrow and text truncates | Use L12 menu or split content |
| Put video in L05 cards | Cards are for scannable content, not media | Use L03/L04 |
| Stack multiple interactions on one screen | Confuses learner and complicates state tracking | One interaction type per screen |
| Use EY yellow as the primary color | EY-Parthenon visual system is blue-led | Use yellow only as an accent |
| Use more than two heading levels per screen | Creates hierarchy confusion | Title plus one subheading |
| Place CTA buttons in the top half | Learners expect progression near the bottom | Bottom-right or bottom-center CTA |
| Mix numbered and bulleted lists in one block | Inconsistent visual language | Pick one list style per block |
| Use paragraphs in cards or steppers | Too much text for scannable formats | Max 2 lines per card; expand elsewhere |

## PowerPoint Master Library Guidance

When maintaining a PPT storyboard template, include:
- One slide per canonical layout, L01-L14 plus popup states.
- Named placeholders such as `TITLE`, `BODY`, `MEDIA`, `OPTIONS`, `FEEDBACK`.
- Notes repeating rules, allowed character limits, and line limits.

AI generation instruction:

```text
Use only canonical layouts from docs/reference/layout-contract.md. Each screen
must declare its LayoutID. Populate known placeholders only. Do not invent new
regions. If content does not fit, split it or return to storyboard review.
```

## Quick Reference Card

```text
LAYOUT RULES
- Use only canonical layouts from docs/reference/layout-contract.md.
- Each screen must declare a LayoutID.
- Populate placeholders only; do not invent new regions.
- If content does not fit, split it or return for storyboard review.
- Default to L01 only when the instructional pattern is unclear.

BRANDING
- Primary accent: Parthenon blue.
- Text: charcoal for body in light-theme artifacts.
- Background: white in light-theme artifacts; dark theme may use approved shell tokens.
- Font: EYInterstate, with Arial/Helvetica fallback.

LIMITS
- Max about 150 words per screen.
- Max 7 +/- 2 visible elements.
- Cards: no more than two body lines.
- Bullets: usually no more than five items.
- Questions: usually no more than four options.
```

## Artifact Rule

All artifacts should use the same canonical layout ID when they mean the same
pattern.

Storyboard specs use:

```yaml
layout: L06
runtime_notes: "Render as compare 2-up; no fallback unless user approves."
```

Production content files use:

```yaml
layout: L06
```

Do not invent separate names such as `storyboard_layout` vs `runtime_layout`.
Those names hide gaps instead of fixing them.

## Gap Rule

When a new pattern appears:

1. Add it to the canonical registry.
2. Add or update the storyboard representation.
3. Add or update the runtime schema and renderer.
4. Add or update tests/fixtures when the pattern affects build behavior.

Temporary adaptation is allowed only as an explicit, user-approved exception:

```yaml
layout: L01
adapted_from: L06
adaptation_reason: "Runtime compare renderer deferred for this pilot."
```

The default path is to close the gap, not normalize the workaround.

## Runtime Field Shapes

Runtime field shapes live in `shell/content.schema.md`. Storyboard specs may
include richer notes, voiceover, and visual direction, but any screen intended
for production must eventually be expressible with the canonical runtime fields.

If the storyboard cannot be expressed by the runtime fields for its canonical
layout, that is a schema/runtime gap to fix.
