# eLearning Pipeline MVP — Design Spec

**Date:** 2026-04-10
**Status:** Approved (brainstorming phase complete; ready for implementation plan)
**Pilot module:** 2.5 — Developing the procurement plan

## Context

Build a personal pipeline that takes a module brief and produces a SCORM 1.2 package ready to upload to SCORM Cloud (cloud.scorm.com). The pipeline is three Claude Code skills chained through human review gates. Output is dark-themed HTML/CSS/JS in the EY-Parthenon visual style.

MVP is one pilot module (Module 2.5), six layouts, one LMS target (SCORM Cloud). Everything else is deferred by explicit decision.

---

## Section 1 — Architecture & Asset Topology

### Pipeline shape

```
Raw input         /content-map      /build-html       /scorm-pack
(topic / PDF / → ────────────  → ────────────  →  ────────────  →
 lesson plan)    content-map.md    content/*.md      dist/*.zip
                                   build/ (HTML)
```

Between every stage sits a **human review gate** — no skill auto-triggers the next. Four review gates total:

1. **G1** — after `/content-map`: review the O-A-P-P table
2. **G2** — after `/build-html` phase 1: review slide list + individual content files
3. **G3** — after `/build-html` phase 2: walk the full module in the browser
4. **G4** — after `/scorm-pack`: upload zip to SCORM Cloud, verify Launch + API log

### Per-module folder

Each module lives in its own folder. Copying the folder = cloning the module.

```
modules/
  2.5-procurement-plan/
    content-map.md               ← Stage 1 output
    content/                     ← Stage 2 phase 1 output (authoring layer)
      00-title.md                each slide = one markdown file
      01-objectives.md           YAML frontmatter + body
      ...
      15-summary.md
    build/                       ← Stage 2 phase 2 output (runnable)
      index.html                 copied from shell
      content.json               merged from content/*.md
      css/ js/ assets/           copied from shell
    dist/                        ← Stage 3 output
      2.5-procurement-plan.zip   SCORM package
```

### Shared shell (the master template)

Written once, reused by every module. Analogous to a Storyline player + slide master, or a PowerPoint `.potx`. When the visual style needs to change, edit the shell once and every module inherits on next build.

```
~/Desktop/elearning-workspace/shell/
  index.html               SCO entry point — reads content.json, renders slides
  css/
    theme-dark.css         EY-Parthenon dark theme (BG #1C2333, Blue #1A9AFA)
    layouts.css            L01–L14 styles (MVP: L01, L03, L09, L12, L13, L14)
  js/
    app.js                 Render engine + navigation + state machine
    pipwerks_scorm.js      SCORM 1.2 wrapper (pipwerks, BSD license)
  schemas/                 SCORM 1.2 XSD schemas (from ADL)
    adlcp_rootv1p2.xsd
    ims_xml.xsd
    imscp_rootv1p1p2.xsd
    imsmd_rootv1p2p1.xsd
  manifest-template.xml    imsmanifest.xml Jinja template (used by /scorm-pack)
```

The `/build-html` phase 2 step is effectively `cp -r shell/* modules/<name>/build/` followed by merging `content/*.md` into `build/content.json`.

**Decisions locked in this section:**

- **Shared shell** (not per-module). One visual source of truth.
- **Shell location** = `~/Desktop/elearning-workspace/shell/` (workspace alongside modules, not bundled inside `~/.claude/skills/`). Shell is a production asset that belongs in a workspace the user can file-manage, git-track, and back up with normal tools. Skills are triggers only.

### Design principles

1. **Shell is asset, not code.** Skills call into the shell; they do not regenerate it.
2. **Each skill is a pure translator.** Input artifact → output artifact. No hidden state between skills.
3. **Every intermediate artifact is human-readable text** (md, json, xml). No binary middle-files. Open any file in any editor, hand-edit, and the next stage picks up from the edited version.
4. **Modules are fully independent.** No cross-module dependencies in MVP. Duplicate a folder = clone a module.

### Where the skills live

Installed as personal skills (not a plugin):

```
~/.claude/skills/
  content-map/SKILL.md
  build-html/SKILL.md
  scorm-pack/SKILL.md
```

Source lives in `~/Desktop/elearning-workspace/skills-src/`; the `~/.claude/skills/` entries can be symlinks back to source for easier editing.

---

## Section 2 — Skill Contracts

Each skill is conversational: user invokes the slash command, Claude dialogues, produces an artifact, stops for review.

### Skill 1 — `/content-map` (alignment thinking)

**Role:** Force objective ↔ assessment ↔ practice ↔ presentation alignment before any slide design.

**Input (any of):**
- A one-line module brief ("30-min module on procurement planning for PMs")
- A lesson plan / source material (PDF, Word, pasted text)
- A seed idea + user's ID intuition

**Behavior:**
1. Read input, identify topic / audience / scope.
2. Dialogue to pin down each objective (action verb; not "understand" / "know").
3. For each objective ask: how is it assessed? what practice enables it? what presentation teaches it?
4. Produce a 4-column **O-A-P-P** markdown table.
5. Run the quality checklist from `content-mapping-best-practices.md` (action verbs? alignment gaps? safe-to-fail practice?).
6. Write output to `modules/<name>/content-map.md`.

**Output:** `modules/<name>/content-map.md` — markdown header (target learner, duration, assessment strategy) plus the 4-column table.

**G1 review:** User verifies every row uses action verbs, alignment is tight end-to-end, no "nice to know" padding, scope is appropriate.

### Skill 2 — `/build-html` (storyboard thinking + HTML generation)

Two phases with a review gate between them.

#### Phase 1 — Storyboard thinking (one slide per file)

**Input:** `content-map.md` + optional reference material.

**Behavior:**
1. Read the O-A-P-P table. For each row decide how many slides and which layout each slide uses.
2. For each slide produce one markdown file with YAML frontmatter:

   ```
   ---
   id: 03-concept-what-is-pp
   layout: L03
   title: What is a procurement plan
   ---

   ## On-screen
   **Title:** What is a procurement plan
   **Body bullets:**
   - A document that defines how purchases will be managed
   - Covers vendor selection, contract type, delivery timing
   - Living document, updated through project lifecycle
   **Media:** {{MEDIA_1}} — photo of signed contract on desk

   ## Voiceover
   [~20 sec conversational VO]

   ## Interaction & dev notes
   - No interaction, click Continue
   - Visited state tracked
   ```

3. Write `modules/<name>/content/NN-slug.md` for each slide.
4. Present a summary table to the user (slide #, file, title, layout, type, notes).

**G2 review:** User reviews slide count, layout choices, order, individual content. Two ways to fix: hand-edit any `content/*.md` directly, or describe problems in natural language and let Claude route the edits.

#### Phase 2 — Build step (near-automatic)

**Behavior:**
1. Merge `content/*.md` into `build/content.json`.
2. Copy `shell/*` into `modules/<name>/build/`.
3. Done — `build/index.html` is runnable by double-click.

**Output:** `modules/<name>/build/` (a runnable HTML module).

**G3 review:** User double-clicks `build/index.html`, walks through the full module in the browser. Verifies every layout, pop-up interaction, MCQ behavior, and dark theme consistency.

**Feedback loop at G3 (important):** User describes problems in plain language. Claude routes the fix to the correct layer:

- **Content fix** ("slide 4 title should be X") → edit the specific `content/*.md`, re-run phase 2.
- **Layout fix** ("slide 6 should be L06 not L03") → change `layout:` in frontmatter + rewrite body to fit the new layout, re-run phase 2.
- **Shell visual fix** ("all pop-up borders are too thin") → edit `shell/css/layouts.css`, re-run phase 2. **Claude confirms first**, because shell changes affect every future module.
- **Shell behavior fix** ("visited checkmark doesn't show after pop-up close") → edit `shell/js/app.js`, re-run phase 2.

User never has to know which file to edit — they describe the problem, Claude routes it.

### Skill 3 — `/scorm-pack` (package & ship)

**Role:** Package a built module into a SCORM 1.2 zip. Near-automatic.

**Input:** A built module folder (`modules/<name>/` with `build/` populated). Optional metadata: title, SCORM identifier, version.

**Behavior:**
1. Read `build/content.json` for module title etc.
2. Fill `shell/manifest-template.xml` → write `build/imsmanifest.xml`.
3. Copy `shell/schemas/*.xsd` → `build/schemas/`.
4. Zip `build/` → `dist/<name>.zip`.
5. Print a report: file count, size, expected SCORM API call sequence on run.

**Output:** `dist/<name>.zip` — directly uploadable to SCORM Cloud.

**G4 review:** User uploads zip to SCORM Cloud, clicks Launch, verifies API log and registration status.

### Git auto-commit (in scope for MVP)

At every review gate, the skill commits the current state of `modules/<name>/` (or `shell/` for shell-level changes) with a structured message like `G2: content files approved for 2.5-procurement-plan`. This gives a free time-machine — the user does not need to learn git to benefit from it.

### Pilot input for Module 2.5

Seed content = the worked example already in `SKILL.md` of the storyboard skill (title, objectives, menu hub with 8 tiles, knowledge check, summary). `/content-map` expands this seed into the full O-A-P-P table during Stage 1.

---

## Section 3 — Success Criteria, Testing, Scope, Risks, Phases

### Must-pass criteria (all required for MVP "done")

- `/content-map` produces `modules/2.5-procurement-plan/content-map.md` with a complete 4-column O-A-P-P table that passes the quality checklist (all action verbs, no alignment gaps).
- `/build-html` produces `content/*.md` (slide-level files) and `build/` (runnable HTML).
- Double-clicking `build/index.html` walks the full module start-to-finish in the browser.
- All **6 MVP layouts** render correctly:
  - **L01** (text only)
  - **L03** (60/40 media + text)
  - **L09** (MCQ) — default state, selected state, submitted state, feedback shown, score recorded
  - **L12** (menu hub) — menu renders, pop-ups open/close, visited checkmarks appear
  - **L13** (objectives list)
  - **L14** (summary) — entry triggers `lesson_status = "completed"`
- Dark theme consistent everywhere (BG `#1C2333`, Parthenon Blue `#1A9AFA`, pop-up = dark panel with blue border).
- `/scorm-pack` produces `dist/2.5-procurement-plan.zip`.
- Zip uploads to SCORM Cloud successfully.
- SCORM Cloud Launch starts the module normally.
- SCORM Cloud API Log shows exactly:
  - `LMSInitialize("")` → `"true"` (once at start)
  - `LMSSetValue("cmi.core.lesson_status", "incomplete")` → `"true"`
  - `LMSSetValue("cmi.core.score.raw", "...")` → `"true"` (after MCQ)
  - `LMSSetValue("cmi.core.lesson_status", "completed")` → `"true"` (at summary)
  - `LMSCommit("")` → `"true"`
  - `LMSFinish("")` → `"true"` (once at end)
- SCORM Cloud Registration Detail shows `Status = Completed`, `Score = <MCQ score>`.

### Should-pass (not hard blocks, but expected to work)

- Every review gate produces a git auto-commit; `git log` shows the full iteration history.
- `build/index.html` runs standalone in the browser (no LMS) — SCORM wrapper silently falls back rather than crashing.
- Re-running the pipeline after editing one slide produces stable, consistent output.

### Per-stage verification strategy

| Stage | How to verify | Time |
|---|---|---|
| `/content-map` | Eyeball `content-map.md` against quality checklist (action verbs, alignment, gaps) | 2–3 min |
| `/build-html` phase 1 | Check summary table (slide count, layouts); spot-check a few `content/*.md` | 5 min |
| `/build-html` phase 2 | Double-click `build/index.html`, walk through in browser, verify each layout + pop-up + MCQ | 10 min |
| `/scorm-pack` | Verify `dist/` has zip; Claude runs basic self-check (zip opens, manifest XML valid, `index.html` entry exists) | 1 min |
| End-to-end on SCORM Cloud | Upload → Launch → full walkthrough → read API log → check registration status | 10–15 min |

Each stage is independently debuggable. Breakage in Stage 3 but browser works at Stage 2 → problem is in manifest or packaging. Broken at both → problem is in shell or `content.json`. "Bisect from the back" is a side-effect of the pipeline shape.

### Out of MVP scope (deferred by explicit decision)

**Deferred layouts (8):** L02 Hero, L04 Media-right, L05 3-up cards, L06 Compare, L07 Stepper, L08 Timeline, L10 Scenario, L11 Drag/Match. Adding one post-MVP = one block of CSS in `layouts.css` + one render function in `app.js`. No architectural change.

**Deferred features:**

- Cross-module shared assets (image libraries) — each module stays self-contained
- Module prerequisites / locking — single SCO doesn't need it
- Multi-language support — one language only
- Nav chrome (left menu, progress bar, breadcrumbs) — Previous / Next / Exit only
- Audio VO playback — VO stays as script in speaker notes only; recording is a separate post-pipeline step (voiceover artist or TTS)
- xAPI / `cmi.interactions` detail / per-slide visit tracking — MVP tracks only basic CMI fields (`lesson_status`, `score.raw`, `session_time`)
- Responsive design — desktop only (1920×1080)
- Accessibility (ARIA, screen reader) — no a11y pass in MVP
- Print-friendly export
- Light theme / theme toggle — dark only

**Deferred skill polish:**

- No TDD framework for the skills themselves — manual verification only
- No multi-environment support — single-machine (user's mac)
- Error handling covers the happy path plus obvious failures; not every edge case

**Why deferred, not ignored:** the point of MVP is to prove pipeline viability, not production polish. Once the pilot runs end-to-end, the user will have clearer signal on which deferred items are real requirements vs speculation — then re-prioritize.

### Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| SCORM Cloud rejects manifest as invalid | Medium | Blocks Stage 3 | **Hello World first** — build a 1-page SCO, upload, verify manifest + packaging flow before touching 2.5 |
| pipwerks wrapper can't find `window.API` on SCORM Cloud | Low | All LMS calls fail | pipwerks is mature; bump `findAPITries` config if needed |
| CMI field format error (e.g., score out of range) | Medium | `SetValue` returns false | SCORM 1.2 `cmi.core.score.raw` must be `"0"`–`"100"`; SCORM Cloud log states this explicitly |
| Dark theme renders differently than expected | **High** | Visual off | **`test-layouts.html` first** — one standalone page with all 6 MVP layouts, no SCORM, no pipeline. Iterate CSS in isolation until happy, then integrate |
| L12 menu-hub state machine (visited / current / popup-open) too tangled | Medium | Stage 2 bug hunt | Build L12 as a standalone mini-demo first — menu + pop-ups only, no other slides, no SCORM. Get state right, then integrate |
| `content.json` schema under-designed, needs restructure when adding layouts | Medium | Small refactor | Keep MVP schema as an open JSON object (loose); tighten only after pilot is stable |
| Module 2.5 real content is bigger than the skill's worked example | Low | Slide count overrun | Split into sub-modules or truncate scope if it happens |
| SCORM Cloud free tier registration limit | Low | Test count capped | Free tier gives 10 registrations — enough for MVP. Second account if needed |

**Top two worries** (both must be handled before integration, not during):

1. **SCORM manifest invalid** → Hello World first
2. **Dark theme CSS iteration** → `test-layouts.html` first

Both become front-loaded tasks in Phase 1 of the implementation plan.

### Rough phase order (shape, not the plan)

The detailed step-by-step plan will come from the `writing-plans` skill after this spec is approved. This is just a rough shape of the work.

- **Phase 0 — Setup.** Create `~/Desktop/elearning-workspace/`, `git init`, download pipwerks + SCORM 1.2 XSD schemas.
- **Phase 1 — De-risk.** Hello World SCORM package → upload → verify. `test-layouts.html` → iterate all 6 MVP layout CSS to satisfaction.
- **Phase 2 — Shell.** Merge Phase 1 outputs. Write `app.js` render engine (switch on `layout_id`). Write L12 menu-hub state machine. Write L09 MCQ state + SCORM score hookup.
- **Phase 3 — Three skills.** `/content-map`, `/build-html` (both phases), `/scorm-pack`. Install to `~/.claude/skills/`.
- **Phase 4 — Pilot Module 2.5 end-to-end.** Run the pipeline. Review. Fix. Re-run. Upload to SCORM Cloud. Verify.
- **Phase 5 — Wrap.** README for the pipeline. Final commit. Reference screenshots for each MVP layout.

Phase 1 is deliberately ahead of Phase 2 — the two highest-risk items get isolated treatment before they can contaminate shell integration.

---

## Decisions locked during brainstorm

- **Pipeline shape:** three skills (not one mega-skill, not five micro-skills) separated by human review gates.
- **Shell model:** shared shell, not per-module.
- **Shell location:** `~/Desktop/elearning-workspace/shell/`.
- **Skill location:** `~/.claude/skills/` (personal skills, not a plugin).
- **LMS target:** SCORM 1.2 → SCORM Cloud only (not SCORM 2004, not a real LMS).
- **MVP layouts:** L01, L03, L09, L12, L13, L14. Eight others deferred.
- **Pilot module:** 2.5 Developing the procurement plan. Seed = worked example already in the storyboard skill's `SKILL.md`.
- **Git auto-commit** at every review gate — in scope for MVP.
- **SCORM wrapper:** pipwerks (mature, BSD-licensed).
- **Two high-risk items front-loaded** in Phase 1: Hello World SCO, `test-layouts.html`.
- **Four review gates** total: G1 (content-map), G2 (content/*.md), G3 (browser walkthrough), G4 (SCORM Cloud).

---

## Next step

After spec self-review + user review of this file → invoke `superpowers:writing-plans` skill to produce the step-by-step implementation plan.
