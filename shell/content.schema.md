# content.json schema (MVP — intentionally loose)

## Top level

```json
{
  "module": {
    "id": "2.5-procurement-plan",
    "title": "Developing the procurement plan",
    "module_label": "Module 2.5",
    "scorm_identifier": "com.qianhui.m2-5-procurement-plan"
  },
  "slides": [ ... ]
}
```

## Slide shape

Every slide:
- `id` (string, unique within module)
- `layout` (string): one of `L01`, `L03`, `L09`, `L12`, `L13`, `L14`, `popup`
- `title` (string)
- plus layout-specific fields below

### L01 — text only
- `body` (array of strings). A line starting with `- ` renders as a bullet; other lines render as paragraphs.

### L03 — 60/40 media + text
- `media` (object): `{ "placeholder": "alt text describing the image" }`
- `bullets` (array of strings)

### L09 — MCQ
- `stem` (string)
- `options` (array of strings)
- `correct_index` (number, 0-based)
- `feedback_correct` (string)
- `feedback_incorrect` (string)
- `points` (number, default 25) — contribution to the 0–100 final score

### L12 — menu hub
- `bars` (array of objects): `{ "num": "01", "title": "...", "popup_slide_id": "id-of-popup-slide" }`
- Popup content lives in separate slides with `layout: "popup"`, referenced via `popup_slide_id`.

### popup — internal, used only as L12 popup target
- `body` (array of strings, same bullet convention as L01)
- `key_message` (string, optional) — rendered as a coral accent bar

### L13 — objectives
- `objectives` (array of strings)

### L14 — summary
- `takeaways` (array of strings)
- On first entry, runtime sets `cmi.core.lesson_status = "completed"` and writes the score.

## Navigation rules
- Visible slides = all slides EXCEPT those with `layout: "popup"`. Popups are rendered as overlays on their L12 host.
- Previous / Next advance between visible slides.
- On an L09 slide: Next is disabled until the MCQ is submitted.
- On an L12 slide: Next is disabled until all bars have been visited.
- On first visit to an L14 slide: runtime marks completion + writes score to SCORM.
- Clicking "Finish" on the last slide calls `LMSFinish`.

## Slide frame rule
Every slide is LOCKED to 16:9 (1280 × 720). If content overflows, the body region scrolls internally inside the slide frame — the slide itself never grows taller than 720px.
