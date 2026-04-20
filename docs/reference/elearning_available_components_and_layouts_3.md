# eLearning Available Components and Layouts

---

# Global Defaults & EY-Parthenon Branding

## Slide Dimensions
- **Canvas:** 1920 × 1080px (16:9 widescreen)
- **Safe margins:** 5% all sides (96px left/right, 54px top/bottom)
- **Max content per slide:** 1 idea, ~150 words, 7±2 visual elements

## EY-Parthenon Brand Colors

> **Note:** EY-Parthenon uses a distinct blue-themed palette, separate from the main EY yellow brand. Update the hex values below with your internal brand guidelines if available.

| Role | Name | Hex | RGB | Usage |
|------|------|-----|-----|-------|
| **Primary** | EY-Parthenon Blue | `#1A9AFA` | (26, 154, 250) | Headers, titles, accent bars, component bars, primary CTAs |
| **Secondary** | EY Yellow (accent only) | `#FFE600` | (255, 230, 0) | Sparingly for EY co-branding, optional |
| **Neutral** | Charcoal | `#2C3E50` | (44, 62, 80) | Body text, primary text |
| **Neutral** | Dark Gray | `#4A4A4A` | (74, 74, 74) | Secondary text, labels |
| **Neutral** | Medium Gray | `#7F8C8D` | (127, 140, 141) | Captions, muted text |
| **Neutral** | Light Gray | `#D5D8DC` | (213, 216, 220) | Borders, dividers |
| **Neutral** | Faint Gray | `#F4F6F7` | (244, 246, 247) | Card backgrounds, content panels |
| **Background** | White | `#FFFFFF` | (255, 255, 255) | Slide background |
| **Feedback** | Success Green | `#27AE60` | (39, 174, 96) | Correct feedback panels |
| **Feedback** | Error Red | `#C0392B` | (192, 57, 43) | Incorrect feedback panels |

### Color Application Rules
- **EY-Parthenon Blue (#1A9AFA):** Slide titles, section headers, accent bars, component bars, icons, buttons, interactive elements
- **Charcoal (#2C3E50):** All body copy and paragraph text
- **Light Gray (#D5D8DC):** Borders, divider lines, inactive UI elements
- **White (#FFFFFF):** Primary slide background
- **EY Yellow:** Use sparingly if EY co-branding required; avoid as primary color

## EY-Parthenon Typography

| Element | Font | Weight | Size | Line Height | Color |
|---------|------|--------|------|-------------|-------|
| Slide Title | EYInterstate | Bold | 32pt | 40pt | #1A3E6F (Parthenon Blue Dark) |
| Section Heading | EYInterstate | Bold | 24pt | 32pt | #1A3E6F |
| Body Copy | EYInterstate | Regular | 18pt | 28pt | #2C3E50 (Charcoal) |
| Card/Module Text | EYInterstate | Light | 14pt | 22pt | #4A4A4A |
| Captions/Labels | EYInterstate | Light | 12pt | 18pt | #7F8C8D |
| Button Text | EYInterstate | Bold | 14pt | — | #FFFFFF (on blue) |

### Typography Rules
- **Fallback font:** If EYInterstate unavailable, use **Arial** or **Helvetica**
- **Never use more than 2 font weights** on a single slide
- **Minimum font size:** 12pt (anything smaller is illegible on projection)
- **Title case** for slide titles; **Sentence case** for body text and bullets

## Default Fallback
- If layout is unclear, use **L01 (1C Text)**
- If color is unclear, default to **Charcoal (#2C3E50)** for text, **White (#FFFFFF)** for background

---

# Available Components

## Presentation components (content display)
* Audio, Code, Dialog, Gif, Graphic, Icon, iFrame, Media, Media Grid, Table, Text, Text & Graphic, Video Stream, etc.

## Interaction components (click/reveal + input)
* Accordion, Tabs, Flip Card / Single Flip Card, Gallery, Hot Graphic (hotspots), Image Slider, Infographic, Interactive Video, Links, Narrative, Text Reveal
* Plus input-style components like Checkbox Group, Radio Group, Select, Number Input, Text Area, Open Input, Sliders/Confidence sliders (and linked variants), Survey, Checklist, Action Button

## Question components (practice/assessment/game)
* Branching, Drag and Drop, Matching, Ordering, Sorting, Multiple Choice (incl. graphic MCQ), Text Input, Game, Card Drop, etc.

---

# Layout Palette

## A. Layout Palette (10–15 layouts max)
Each layout has an ID, structure specification, and usage guidance.

---

### Core Content Layouts

#### L01: 1C Text
- **Structure:** Single column, full width (100%), vertically stacked
- **Anatomy:**
  - Title: 1 line, bold, top-aligned, left or centered
  - Body: max 120–160 words (~6–8 lines), regular weight, left-aligned
- **Spacing:** 5% left/right margins, 24px gap between title and body
- **Use for:** definitions, introductions, explanations, policy statements, any text-heavy content without visuals

---

#### L02: 1C Hero + Body
- **Structure:** Single column, stacked vertically (hero top, body below)
- **Anatomy:**
  - Hero image/banner: 100% width, 16:9 aspect ratio, top of content area
  - Subheading: 1 line, bold, below hero
  - Body: max 60–80 words (~3–4 lines), regular weight, left-aligned
  - CTA button: optional, right-aligned or centered below body
- **Spacing:** 5% left/right margins, 16px gap between elements
- **Use for:** module openers, section intros, high-impact announcements, welcome screens

---

#### L03: 2C 60/40 (Media Left)
- **Structure:** 2 columns — left 60%, right 40%
- **Anatomy:**
  - Left column: image or video, 4:3 or 16:9 aspect ratio, vertically centered
  - Right column:
    - Heading: 1 line, bold, top-aligned
    - Body: max 80–100 words (~4–5 lines), regular weight
    - Bullets: optional, max 3–4 items, 1 line each
- **Spacing:** 24px gap between columns, 5% outer margins
- **Use for:** concept explanation with visual support, feature highlights, process introductions

---

#### L04: 2C 40/60 (Media Right)
- **Structure:** 2 columns — left 40%, right 60%
- **Anatomy:**
  - Left column:
    - Heading: 1 line, bold, top-aligned
    - Body: max 80–100 words (~4–5 lines), regular weight
    - Bullets: optional, max 3–4 items, 1 line each
  - Right column: image or video, 4:3 or 16:9 aspect ratio, vertically centered
- **Spacing:** 24px gap between columns, 5% outer margins
- **Use for:** concept explanation with visual support (alternate layout), case study introductions

---

#### L05: 3-up Cards
- **Structure:** 3 equal columns (33% each), horizontally centered
- **Card anatomy:**
  - Icon: 60x60px, square, centered at top of card
  - Heading: 1 line, bold, centered below icon
  - Body: max 2 lines, regular weight, centered
- **Spacing:** 24px gap between cards, 5% left/right margins
- **Use for:** learning objectives, key concepts, module overview, benefits/features list

---

#### L06: Compare 2-up
- **Structure:** 2 equal columns (50/50), side by side
- **Column anatomy:**
  - Column header: 1 line, bold, centered or left-aligned, distinct background color per column
  - Bullet list: 3–5 parallel items, 1 line each, aligned between columns
  - Optional icon: 40x40px above header
- **Spacing:** 16px gap between columns, 5% outer margins, 12px between bullets
- **Use for:** pros/cons, before/after, option A vs option B, method comparisons

---

### Process / Sequence Layouts

#### L07: Stepper (1→4)
- **Structure:** Horizontal row of 3–5 steps, equal width, connected by line/arrow
- **Step anatomy:**
  - Step number: circle (40x40px) with number, centered above
  - Label: 1 line, bold, centered below circle
  - Caption: max 1–2 lines, regular weight, centered below label
- **Connector:** horizontal line or arrow between circles
- **Spacing:** Equal distribution across width, 5% outer margins, 8px between label and caption
- **Use for:** sequential processes, workflows, phase overviews, how-to steps

---

#### L08: Timeline
- **Structure:** Vertical line (centered or left-aligned) with 4–6 nodes
- **Node anatomy:**
  - Node marker: circle (24x24px) on the line
  - Date/label: 1 line, bold, opposite side of content
  - Content: max 2–3 lines, regular weight, beside the node
- **Spacing:** 40px vertical gap between nodes, 5% outer margins
- **Use for:** project phases, historical progression, milestones, chronological events

---

### Interaction / Practice Layouts

#### L09: Knowledge Check MCQ
- **Structure:** Stacked vertically — stem top, options middle, feedback bottom
- **Anatomy:**
  - Stem/question: max 2–3 lines, bold, top area
  - Options: 4 choices (A–D), each max 1–2 lines, left-aligned with radio button/checkbox
  - Feedback area: hidden until submission, max 3 lines, distinct background (green correct / red incorrect)
  - Submit button: right-aligned below options
- **Spacing:** 16px between stem and options, 12px between each option, 24px above feedback
- **Use for:** knowledge checks, quizzes, formative assessments, recall questions
- **States:**
  - Default: All options visible, feedback hidden, Submit button inactive
  - Selected: Highlight chosen option with Parthenon Blue (#2D5F9A) border
  - Submitted: Disable options, show feedback panel (correct=#27AE60 bg, incorrect=#C0392B bg)
  - Retry (if allowed): Reset to Default state, clear selection
- **Branching:** Linear (none) unless specified; optionally "If incorrect → show hint layer"

---

#### L10: Scenario Choice
- **Structure:** 2 regions — prompt/context (top 40%), choices + consequence (bottom 60%)
- **Anatomy:**
  - Context panel: scenario description, max 3–4 lines, may include character image (optional, left-aligned 80x80px)
  - Choices: 2–3 buttons or cards, horizontally arranged, each max 2 lines
  - Consequence panel: hidden until selection, shows outcome text (max 3 lines) + feedback
- **Spacing:** 24px between context and choices, 16px between choice buttons
- **Use for:** decision-based scenarios, branching simulations, application exercises, judgment calls
- **States:**
  - Default: Context visible, choice buttons enabled, consequence hidden
  - Hover: Button border highlight (Parthenon Blue #2D5F9A)
  - Selected: Disable other choices, reveal consequence panel
  - Consequence: Show outcome + "Continue" CTA
- **Branching:** Specify destination per choice (e.g., "Choice A → Slide 12, Choice B → Slide 14")

---

#### L11: Drag/Match
- **Structure:** 3 regions — instruction bar (top), draggable items (left 40%), drop targets (right 60%)
- **Anatomy:**
  - Instruction bar: 1 line, bold, full width, top
  - Draggable items: 4–6 items, each a card (max 1–2 lines), stacked vertically
  - Drop targets: 4–6 labeled zones, each with border/placeholder, stacked or grid
  - Feedback area: bottom, hidden until completion
- **Spacing:** 16px between items, 24px gap between left and right regions, 5% outer margins
- **Use for:** matching exercises, categorization, sequencing (if vertical targets), term-definition pairing
- **States:**
  - Default: All items in source area, targets empty (dashed border)
  - Dragging: Item follows cursor, target highlights on hover
  - Dropped: Item snaps to target, border changes to solid
  - Complete: All items placed, Submit button activates
  - Feedback: Show correct/incorrect per item (green check / red X), overall score
- **Branching:** Linear; optionally "If score < 80% → retry"

---

### Navigation / Framing Layouts

#### L12: Menu
- **Structure:** Grid of 4–8 tiles (2x2, 2x3, or 2x4 arrangement)
- **Tile anatomy:**
  - Icon or thumbnail: 80x80px or 16:9 thumbnail, centered top
  - Title: 1 line, bold, centered below icon
  - Subtitle: optional, 1 line, regular weight, below title
  - Clickable: entire tile is interactive
- **Spacing:** 24px gap between tiles, 5% outer margins, centered grid
- **Use for:** module selection, topic menu, lesson navigation, dashboard home

---

#### L13: Objective / Agenda
- **Structure:** Single column with 3–5 stacked objective rows
- **Row anatomy:**
  - Icon: 40x40px, left-aligned
  - Objective text: 1–2 lines, regular weight, beside icon
  - Optional numbering: "1.", "2.", etc. before icon
- **Spacing:** 16px between rows, 5% outer margins, 12px gap between icon and text
- **Use for:** learning objectives screen, agenda/outline, "what you'll learn" intro, module goals

---

#### L14: Summary
- **Structure:** Single column, stacked — heading, key takeaways, CTA
- **Anatomy:**
  - Heading: 1 line (e.g., "Key Takeaways"), bold, top
  - Takeaways: 3 bullet points, each 1–2 lines, regular weight
  - CTA button: "Next" or "Continue", right-aligned or centered, bottom
- **Spacing:** 24px between heading and bullets, 12px between bullets, 32px above CTA
- **Use for:** module wrap-up, section summary, lesson recap, transition to next section

---

> This palette covers 90% of screens without "creative drift."

---

## B. Layout Rules
Attach these rules to the palette to maintain consistency:

* **Grid:** Use a 12-column grid (or at least "left/right split at 60/40")
* **Margins:** Fixed margins (e.g., 5–7% safe margins)
* **Text limits:** Max lines per region (e.g., "card body ≤ 2 lines")
* **Image aspect ratios:** 16:9 hero, 4:3 inline, square icon
* **Default fallback:** L01 if unsure

---

## C. Page Type → Layout Mapping
For each page archetype, choose from a subset of layouts:

| Page Type | Allowed Layouts |
|-----------|-----------------|
| Learning objectives | L13 (Objective) or L05 (3-up cards) |
| Concept explanation | L01 / L03 / L04 |
| Process/how-to | L07 (Stepper) or L08 (Timeline) |
| Compare options | L06 (Compare) |
| Menu / module select | L12 (Menu) |
| MCQ knowledge check | L09 (MCQ) |
| Scenario decision | L10 (Scenario) |
| Wrap-up | L14 (Summary) |

> This prevents "MCQ screens that look like marketing slides."

---

## D. PowerPoint Master Library (Implementation Artifact)
Create one PPT that contains:

* **1 slide per layout** (L01–L14)
* **Named placeholders:** "TITLE", "BODY", "MEDIA", "OPTIONS", "FEEDBACK"
* **Note block** repeating rules + allowed character/line limits

### Instruction for AI generation:
> "Use only layouts L01–L14 from the Layout Palette. Each slide must declare its LayoutID. Populate placeholders only; don't invent new regions. If content doesn't fit, split into another slide."

This works whether you later implement in Storyline (as slide masters + states/layers) or keep it as a storyboard spec.

---

## E. Component-to-Layout Mapping

| Layout | Primary Components | Avoid |
|--------|-------------------|-------|
| L01 | Text | Media, interactive elements |
| L02 | Text, Media (hero), Action Button | Multiple CTAs |
| L03 | Text & Graphic, Media, Video Stream | More than 1 media item |
| L04 | Text & Graphic, Media, Video Stream | More than 1 media item |
| L05 | Flip Card, Icon, Text | Accordion, Video |
| L06 | Text, Icon | Interactive components |
| L07 | Icon, Text | Media, long descriptions |
| L08 | Text, Icon | Horizontal layout |
| L09 | Multiple Choice, Radio Group | Decorative graphics, video |
| L10 | Branching, Action Button | MCQ options |
| L11 | Drag and Drop, Matching | Text-heavy content |
| L12 | Action Button, Icon, Graphic | Long text, interactions |
| L13 | Icon, Text | Media, interactions |
| L14 | Text, Action Button | New content introduction |

---

## F. Placeholder Naming Convention

Use these standardized placeholder names for consistent AI output:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{TITLE}}` | Slide title | "Planning Procurement" |
| `{{SUBTITLE}}` | Optional subtitle or section label | "Module 2 of 6" |
| `{{BODY}}` | Main text block | Paragraph content |
| `{{BULLETS}}` | Bulleted list items | "• Item 1\n• Item 2" |
| `{{MEDIA_1}}`, `{{MEDIA_2}}` | Images/videos (numbered if multiple) | "[Image: workflow diagram]" |
| `{{ICON_1}}`, `{{ICON_2}}`, `{{ICON_3}}` | Icons (numbered) | "[Icon: checklist]" |
| `{{STEM}}` | Question text for assessments | "Which procurement model is best for...?" |
| `{{OPT_A}}`, `{{OPT_B}}`, `{{OPT_C}}`, `{{OPT_D}}` | Answer options | "Design-Bid-Build" |
| `{{FEEDBACK_CORRECT}}` | Correct answer feedback | "That's right! DBB is..." |
| `{{FEEDBACK_INCORRECT}}` | Incorrect answer feedback | "Not quite. Consider that..." |
| `{{CTA}}` | Button text | "Continue" |
| `{{NARRATION}}` | Voiceover script (if applicable) | Full VO script for slide |
| `{{DEV_NOTES}}` | Developer/build notes | "Trigger animation on click" |

---

## G. Anti-patterns (Avoid)

These combinations cause usability or visual issues:

| Don't | Why | Instead |
|-------|-----|---------|
| Put MCQ (L09) with decorative graphics | Distracts from question, clutters layout | Use clean L09; save graphics for content slides |
| Exceed 3 bullets on L14 Summary | Defeats purpose of summary | Pick top 3 takeaways; link to details |
| Use L05 Cards for more than 3 items | Cards become too narrow, text truncates | Use L12 Menu grid for 4+ items |
| Put video in L05 Cards | Cards are for scannable content, not media | Use L03/L04 for video + text |
| Stack multiple interactions on one slide | Confuses learner, hard to track state | One interaction type per slide |
| Use EY Yellow as primary color | EY-Parthenon has its own blue identity | Use Yellow only for EY co-branding if required |
| Use Parthenon Blue as text color on white | Good contrast, but reserve for titles only | Use Charcoal #2C3E50 for body text |
| Use more than 2 heading levels per slide | Creates visual hierarchy confusion | Title + one subheading max |
| Place CTA buttons in top half of slide | Users expect progression at bottom | CTAs always bottom-right or bottom-center |
| Mix numbered and bulleted lists | Inconsistent visual language | Pick one per content block |
| Use full paragraphs in cards or steppers | Too much text for scannable formats | Max 2 lines per card; expand in separate slide |

---

## H. Quick Reference Card

### For AI Prompt Inclusion:

```
LAYOUT RULES:
- Use only L01–L14 from Layout Palette
- Each slide must declare LayoutID
- Populate placeholders only; don't invent new regions
- If content doesn't fit, split into another slide
- Default to L01 if layout unclear

BRANDING (EY-Parthenon):
- Primary accent: Parthenon Blue #1A3E6F (dark), #2D5F9A (medium)
- Text: Charcoal #2C3E50 (body), Blue #1A3E6F (titles)
- Background: White #FFFFFF
- Font: EYInterstate (fallback: Arial)
- Title: 32pt Bold, Body: 18pt Regular

LIMITS:
- Max 150 words per slide
- Max 7±2 visual elements
- Cards: ≤2 lines body text
- Bullets: ≤5 items, 1 line each
- Questions: ≤4 options
```
