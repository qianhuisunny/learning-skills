# eLearning Pipeline MVP Implementation Plan

> **Status note (updated):** This original plan described a three-skill flow that
> mixed storyboarding into `/build-html`. The current repo contract is now the
> four-skill flow in `README.md` and
> `docs/specs/2026-04-10-elearning-pipeline-design.md`:
> `/content-map` → `/storyboard` → `/build-html` → `/scorm-pack`.
> Treat the detailed tasks below as historical implementation notes unless they
> have been updated to match that four-skill boundary.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a three-skill Claude Code pipeline (`/content-map` → `/build-html` → `/scorm-pack`) that transforms a lesson brief into a SCORM 1.2 package, and pilot it end-to-end with Module 2.5 uploaded to SCORM Cloud.

**Architecture:** A shared HTML/CSS/JS shell template lives in `~/Desktop/elearning-workspace/shell/`. Each module gets its own folder under `modules/<slug>/` with three staged artifacts: `content-map.md` (O-A-P-P alignment table), `content/*.md` (per-slide authoring files with YAML frontmatter), `build/` (runnable HTML = shell files copied + merged `content.json`). Python build scripts do the mechanical work (merge, template-fill, zip). Three skills orchestrate the flow through four human review gates (G1–G4) with git auto-commit after each. Two high-risk items (SCORM manifest validity, dark-theme CSS fidelity) are de-risked in Phase 1 before shell integration.

**Tech Stack:**
- Runtime: HTML5 / CSS3 / vanilla ES6 (no build step, no npm)
- SCORM: SCORM 1.2 + pipwerks SCORM API wrapper (BSD-licensed, vendored)
- Build scripts: Python 3 + jinja2 + pyyaml + pytest + stdlib (zipfile, json, xml.etree, re)
- LMS target: SCORM Cloud (cloud.scorm.com, free tier)
- Workspace: `~/Desktop/elearning-workspace/` (new, separate from this repo)
- Skill install path: `~/.claude/skills/{content-map,build-html,scorm-pack}/` (symlinked from `~/Desktop/elearning-workspace/skills-src/`)

---

## How to read this plan (for Qianhui)

You don't need to read the code blocks. Claude Code executes tasks; you review at four checkpoints:

- **C1** — Hello World SCO uploads to SCORM Cloud and launches (5 min of your time)
- **C2** — `test-layouts.html` shows all 6 layouts looking right in the browser (10 min, possibly iterated)
- **C3** — `shell/index.html` with bundled sample content runs end-to-end in the browser (10 min)
- **C4** — Real Module 2.5 pipeline runs, zip uploads to SCORM Cloud, shows Completed + Score (15 min)

Between checkpoints, Claude Code works autonomously. If anything breaks, it's caught within the current phase before touching the next.

---

## Phase 0 — Workspace setup

Goal: Create the workspace tree, init git, install Python deps, vendor pipwerks + SCORM 1.2 XSDs.

### Task 0.1: Create directory tree

**Files:**
- Create: `~/Desktop/elearning-workspace/` (entire tree)

- [ ] **Step 1: Create tree**

```bash
mkdir -p ~/Desktop/elearning-workspace/{shell/{css,js,schemas,assets},modules,scripts/tests,dev/hello-world-sco,skills-src/{content-map,build-html,scorm-pack}}
```

- [ ] **Step 2: Verify**

```bash
find ~/Desktop/elearning-workspace -type d | sort
```

Expected: 13 directories (workspace root + 12 subdirs).

### Task 0.2: Initialize git + .gitignore + stub README

**Files:**
- Create: `~/Desktop/elearning-workspace/.gitignore`
- Create: `~/Desktop/elearning-workspace/README.md`

- [ ] **Step 1: git init**

```bash
cd ~/Desktop/elearning-workspace && git init -b main
```

- [ ] **Step 2: Write .gitignore**

```
__pycache__/
*.pyc
.pytest_cache/
.DS_Store
modules/*/dist/*.zip
```

- [ ] **Step 3: Write stub README.md**

```markdown
# eLearning pipeline workspace

Three-skill Claude Code pipeline that produces SCORM 1.2 packages.

Design spec + plan: `~/Desktop/elearning-storyboard/docs/superpowers/`.

## Layout
- `shell/` — shared HTML/CSS/JS + SCORM wrapper + XSD schemas (the "master template")
- `modules/` — one folder per module; each contains content-map, content files, build, dist
- `scripts/` — Python build helpers (merge, manifest-fill, pack)
- `skills-src/` — source for the three skills (symlinked into `~/.claude/skills/`)
- `dev/` — throwaway test harnesses (hello-world SCO, test-layouts.html)
```

- [ ] **Step 4: Initial commit**

```bash
cd ~/Desktop/elearning-workspace
git add .gitignore README.md
git commit -m "chore: init workspace"
```

### Task 0.3: Install Python deps

**Files:**
- Create: `~/Desktop/elearning-workspace/requirements.txt`

- [ ] **Step 1: Write requirements.txt**

```
jinja2>=3.1
pytest>=8.0
pyyaml>=6.0
```

- [ ] **Step 2: Install**

```bash
pip3 install -r ~/Desktop/elearning-workspace/requirements.txt
```

- [ ] **Step 3: Verify**

```bash
python3 -c "import jinja2, pytest, yaml; print('ok')"
```

Expected: `ok`.

- [ ] **Step 4: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add requirements.txt
git commit -m "chore: add python deps"
```

### Task 0.4: Vendor pipwerks SCORM wrapper

**Files:**
- Create: `~/Desktop/elearning-workspace/shell/js/pipwerks_scorm.js`

- [ ] **Step 1: Download**

```bash
curl -fsSL https://raw.githubusercontent.com/pipwerks/scorm-api-wrapper/master/src/JavaScript/SCORM_API_wrapper.js \
  -o ~/Desktop/elearning-workspace/shell/js/pipwerks_scorm.js
```

- [ ] **Step 2: Sanity check**

```bash
wc -l ~/Desktop/elearning-workspace/shell/js/pipwerks_scorm.js
head -5 ~/Desktop/elearning-workspace/shell/js/pipwerks_scorm.js
```

Expected: ~600+ lines; first lines reference pipwerks / SCORM. If download fails, resolve an alternate source for `pipwerks/scorm-api-wrapper` at execution time.

- [ ] **Step 3: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add shell/js/pipwerks_scorm.js
git commit -m "chore: vendor pipwerks SCORM 1.2 wrapper"
```

### Task 0.5: Vendor SCORM 1.2 XSD schemas

**Files:**
- Create: `~/Desktop/elearning-workspace/shell/schemas/adlcp_rootv1p2.xsd`
- Create: `~/Desktop/elearning-workspace/shell/schemas/ims_xml.xsd`
- Create: `~/Desktop/elearning-workspace/shell/schemas/imscp_rootv1p1p2.xsd`
- Create: `~/Desktop/elearning-workspace/shell/schemas/imsmd_rootv1p2p1.xsd`

SCORM 1.2 XSDs are public-domain ADL conformance files. Resolve a working source at execution time.

- [ ] **Step 1: Try ADL / community mirror**

```bash
cd ~/Desktop/elearning-workspace/shell/schemas
for f in adlcp_rootv1p2.xsd ims_xml.xsd imscp_rootv1p1p2.xsd imsmd_rootv1p2p1.xsd; do
  curl -fsSL -o "$f" "https://raw.githubusercontent.com/adlnet/SCORM-1.2-Sample-Content-Package/master/Schemas/$f" || echo "MISSING: $f"
done
ls -la
```

- [ ] **Step 2: If any file is missing or empty**, locate from an alternate mirror (Sakai SCORM module, moodle SCORM plugin, or scorm.com sample packages). Criterion: each file starts with `<?xml` and is > 1KB.

- [ ] **Step 3: Verify**

```bash
for f in ~/Desktop/elearning-workspace/shell/schemas/*.xsd; do
  head -2 "$f" | tr -d '\n' | cut -c1-80
  echo
done
```

Expected: each line begins with `<?xml`.

- [ ] **Step 4: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add shell/schemas/
git commit -m "chore: vendor SCORM 1.2 XSD schemas"
```

---

## Phase 1A — De-risk SCORM manifest + packaging (Hello World SCO)

Goal: Prove manifest format + packaging flow work against SCORM Cloud before touching real content.

### Task 1A.1: Write Hello World index.html

**Files:**
- Create: `~/Desktop/elearning-workspace/dev/hello-world-sco/index.html`

- [ ] **Step 1: Write HTML**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Hello World SCO</title>
  <script src="pipwerks_scorm.js"></script>
  <style>
    body { font-family: sans-serif; background: #1C2333; color: #fff; padding: 48px; }
    button { padding: 12px 24px; font-size: 16px; margin-top: 20px; cursor: pointer; background: #1A9AFA; color: #fff; border: none; }
    .status { margin-top: 16px; color: #B4BCD0; }
  </style>
</head>
<body>
  <h1>Hello World SCO</h1>
  <p>Minimal SCORM 1.2 package used to verify manifest + packaging against SCORM Cloud.</p>
  <div class="status">Status: <span id="status">(loading)</span></div>
  <button id="finishBtn">Finish and exit</button>

  <script>
    const scorm = pipwerks.SCORM;
    scorm.version = "1.2";

    window.addEventListener("load", () => {
      const ok = scorm.init();
      document.getElementById("status").textContent = ok ? "initialized (LMS detected)" : "standalone (no LMS)";
      if (ok) {
        scorm.set("cmi.core.lesson_status", "completed");
        scorm.save();
      }
    });

    document.getElementById("finishBtn").addEventListener("click", () => {
      if (scorm.connection.isActive) scorm.quit();
      try { window.close(); } catch (e) {}
    });
  </script>
</body>
</html>
```

- [ ] **Step 2: Copy pipwerks into SCO dir**

```bash
cp ~/Desktop/elearning-workspace/shell/js/pipwerks_scorm.js \
   ~/Desktop/elearning-workspace/dev/hello-world-sco/pipwerks_scorm.js
```

### Task 1A.2: Write Hello World imsmanifest.xml

**Files:**
- Create: `~/Desktop/elearning-workspace/dev/hello-world-sco/imsmanifest.xml`

- [ ] **Step 1: Write manifest**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="com.qianhui.helloworld" version="1.0"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd
                              http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 imsmd_rootv1p2p1.xsd
                              http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>
  <organizations default="DEFAULT_ORG">
    <organization identifier="DEFAULT_ORG">
      <title>Hello World SCO</title>
      <item identifier="ITEM_01" identifierref="RES_01" isvisible="true">
        <title>Hello World</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES_01" type="webcontent" adlcp:scormtype="sco" href="index.html">
      <file href="index.html"/>
      <file href="pipwerks_scorm.js"/>
    </resource>
  </resources>
</manifest>
```

- [ ] **Step 2: Copy XSDs into SCO dir**

```bash
cp ~/Desktop/elearning-workspace/shell/schemas/*.xsd \
   ~/Desktop/elearning-workspace/dev/hello-world-sco/
```

### Task 1A.3: Verify manifest XML is well-formed

- [ ] **Step 1: Parse**

```bash
python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('$HOME/Desktop/elearning-workspace/dev/hello-world-sco/imsmanifest.xml')
root = tree.getroot()
print('root:', root.tag)
print('children:', [c.tag.split('}')[-1] for c in root])
"
```

Expected output includes `manifest` root and children `metadata`, `organizations`, `resources`.

### Task 1A.4: Package as zip

**Files:**
- Create: `~/Desktop/elearning-workspace/dev/hello-world-sco.zip`

- [ ] **Step 1: Zip**

```bash
cd ~/Desktop/elearning-workspace/dev/hello-world-sco
rm -f ../hello-world-sco.zip
zip -r ../hello-world-sco.zip . -x "*.DS_Store"
```

- [ ] **Step 2: Verify contents at root of zip (not nested)**

```bash
unzip -l ~/Desktop/elearning-workspace/dev/hello-world-sco.zip
```

Expected top-level entries: `imsmanifest.xml`, `index.html`, `pipwerks_scorm.js`, 4 `.xsd` files — NOT nested under `hello-world-sco/`.

- [ ] **Step 3: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add dev/hello-world-sco/
git commit -m "feat(dev): hello-world SCO for manifest de-risk"
```

### Task 1A.5: 🛑 CHECKPOINT C1 — User uploads Hello World to SCORM Cloud

- [ ] **Step 1: Present to Qianhui**

> **Your turn (5 min):**
> 1. Open https://cloud.scorm.com → sign up for a free account if you don't have one.
> 2. Click "Add Content" → "Upload a SCORM package".
> 3. Upload `~/Desktop/elearning-workspace/dev/hello-world-sco.zip`.
> 4. If the import fails with "invalid manifest" or any error, copy-paste the error back to me.
> 5. Click **Launch**. You should see "Hello World SCO" and status "initialized (LMS detected)".
> 6. Click "Finish and exit".
> 7. In SCORM Cloud: go to the course → Registrations → click the registration → open the API Log. Confirm you see `LMSInitialize`, `LMSSetValue("cmi.core.lesson_status", "completed")`, `LMSFinish`, all returning `"true"`.
> 8. Tell me "C1 passed" or paste the error.

- [ ] **Step 2: Wait for confirmation.** If fail, debug manifest / packaging / pipwerks before Phase 1B. If pass, proceed.

---

## Phase 1B — De-risk dark-theme CSS (test-layouts.html)

Goal: Build `shell/css/theme-dark.css` and `shell/css/layouts.css` to full visual satisfaction. By end of phase, these files are the canonical styles used by the shell.

### Task 1B.1: Write theme-dark.css

**Files:**
- Create: `~/Desktop/elearning-workspace/shell/css/theme-dark.css`

- [ ] **Step 1: Write theme**

```css
/* EY-Parthenon dark theme — shared across all modules */
:root {
  --bg-primary: #1C2333;
  --bg-secondary: #252D42;
  --bg-elevated: #2E384F;
  --brand-blue: #1A9AFA;
  --brand-blue-dim: #1578C4;
  --text-primary: #FFFFFF;
  --text-secondary: #B4BCD0;
  --text-muted: #7A8299;
  --accent-yellow: #FFC83D;
  --feedback-correct: #2ECC71;
  --feedback-incorrect: #E74C3C;

  --space-xs: 6px;
  --space-sm: 12px;
  --space-md: 20px;
  --space-lg: 32px;
  --space-xl: 48px;

  --font-sans: "Helvetica Neue", "Arial", sans-serif;
  --font-size-body: 18px;
  --font-size-h1: 42px;
  --font-size-h2: 28px;
  --font-size-h3: 22px;
  --line-height-body: 1.5;

  --slide-width: 1280px;
  --slide-height: 720px;
  --slide-padding: 64px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: var(--font-sans);
  font-size: var(--font-size-body);
  line-height: var(--line-height-body);
  min-height: 100vh;
}

.slide {
  width: var(--slide-width);
  min-height: var(--slide-height);
  padding: var(--slide-padding);
  margin: 0 auto;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

h1 { font-size: var(--font-size-h1); font-weight: 700; margin-bottom: var(--space-md); }
h2 { font-size: var(--font-size-h2); font-weight: 600; margin-bottom: var(--space-sm); }
h3 { font-size: var(--font-size-h3); font-weight: 600; margin-bottom: var(--space-sm); }
p  { margin-bottom: var(--space-md); }

.module-label {
  display: inline-block;
  padding-left: var(--space-sm);
  border-left: 4px solid var(--brand-blue);
  color: var(--text-secondary);
  font-size: 14px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: var(--space-md);
}

ul.bullets { list-style: none; padding: 0; }
ul.bullets li {
  padding-left: var(--space-md);
  margin-bottom: var(--space-sm);
  position: relative;
}
ul.bullets li::before {
  content: "–";
  position: absolute;
  left: 0;
  color: var(--brand-blue);
}
```

### Task 1B.2: Write layouts.css (all 6 MVP layouts)

**Files:**
- Create: `~/Desktop/elearning-workspace/shell/css/layouts.css`

- [ ] **Step 1: Write layouts**

```css
/* ========== L01 — Text only ========== */
.layout-l01 .body { max-width: 960px; margin-top: var(--space-md); }

/* ========== L03 — 60/40 media + text ========== */
.layout-l03 .grid {
  display: grid;
  grid-template-columns: 60% 40%;
  gap: var(--space-lg);
  margin-top: var(--space-md);
  align-items: start;
}
.layout-l03 .media {
  background: var(--bg-secondary);
  border: 1px dashed var(--text-muted);
  min-height: 360px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  text-align: center;
  padding: var(--space-md);
}

/* ========== L09 — MCQ ========== */
.layout-l09 .stem {
  max-width: 960px;
  margin: var(--space-md) 0 var(--space-lg);
  font-size: var(--font-size-h3);
}
.layout-l09 .options { list-style: none; padding: 0; max-width: 720px; }
.layout-l09 .options li {
  padding: var(--space-md) var(--space-lg);
  margin-bottom: var(--space-sm);
  background: var(--bg-secondary);
  border: 2px solid transparent;
  cursor: pointer;
  transition: border-color 120ms ease, background 120ms ease;
}
.layout-l09 .options li:hover { background: var(--bg-elevated); }
.layout-l09 .options li.selected { border-color: var(--brand-blue); background: var(--bg-elevated); }
.layout-l09 .options li.correct-answer { border-color: var(--feedback-correct); }
.layout-l09 .options li.wrong-answer { border-color: var(--feedback-incorrect); }
.layout-l09 .options li.disabled { pointer-events: none; opacity: 0.85; }
.layout-l09 .submit-btn {
  margin-top: var(--space-lg);
  padding: var(--space-sm) var(--space-lg);
  background: var(--brand-blue);
  color: #fff;
  border: none;
  font-size: var(--font-size-body);
  cursor: pointer;
}
.layout-l09 .submit-btn:disabled { background: var(--text-muted); cursor: not-allowed; }

.layout-l09.submitted .l09-split {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-lg);
  align-items: start;
}
.layout-l09 .feedback-panel {
  background: var(--bg-secondary);
  border-left: 4px solid var(--brand-blue);
  padding: var(--space-lg);
}
.layout-l09 .feedback-panel.correct { border-left-color: var(--feedback-correct); }
.layout-l09 .feedback-panel.incorrect { border-left-color: var(--feedback-incorrect); }
.layout-l09 .feedback-panel h3 { color: var(--brand-blue); }
.layout-l09 .feedback-panel.correct h3 { color: var(--feedback-correct); }
.layout-l09 .feedback-panel.incorrect h3 { color: var(--feedback-incorrect); }

/* ========== L12 — Menu hub (vertical bars + popup overlay) ========== */
.layout-l12 .bars { list-style: none; padding: 0; max-width: 960px; margin-top: var(--space-md); }
.layout-l12 .bar {
  display: flex;
  align-items: center;
  padding: var(--space-md) var(--space-lg);
  background: var(--bg-secondary);
  border-left: 4px solid var(--brand-blue);
  margin-bottom: var(--space-sm);
  cursor: pointer;
  transition: background 120ms ease;
}
.layout-l12 .bar:hover { background: var(--bg-elevated); }
.layout-l12 .bar .num {
  font-size: var(--font-size-h3);
  color: var(--brand-blue);
  font-weight: 700;
  width: 60px;
}
.layout-l12 .bar .title-text { flex: 1; color: var(--text-primary); }
.layout-l12 .bar .check {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--feedback-correct);
  color: #fff;
  display: none;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}
.layout-l12 .bar.visited .check { display: flex; }
.layout-l12 .bar.visited .num { color: var(--text-muted); }

.layout-l12 .popup-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(12, 16, 28, 0.72);
  display: none;
  align-items: center;
  justify-content: center;
  padding: var(--space-xl);
  z-index: 100;
}
.layout-l12.popup-open .popup-backdrop { display: flex; }
.layout-l12 .popup-panel {
  background: var(--bg-secondary);
  border: 2px solid var(--brand-blue);
  max-width: 900px;
  width: 100%;
  padding: var(--space-lg);
  position: relative;
  max-height: 80vh;
  overflow-y: auto;
}
.layout-l12 .popup-header {
  display: flex;
  align-items: center;
  margin-bottom: var(--space-md);
  padding-bottom: var(--space-sm);
  border-bottom: 1px solid var(--bg-elevated);
}
.layout-l12 .popup-header .num { color: var(--brand-blue); font-size: var(--font-size-h3); font-weight: 700; width: 60px; }
.layout-l12 .popup-header .popup-title { flex: 1; font-size: var(--font-size-h3); font-weight: 600; }
.layout-l12 .popup-close {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 24px;
  cursor: pointer;
  padding: 0 var(--space-sm);
}
.layout-l12 .popup-body { color: var(--text-primary); }
.layout-l12 .popup-body p { margin-bottom: var(--space-sm); }
.layout-l12 .popup-key-message {
  margin-top: var(--space-md);
  padding: var(--space-sm) var(--space-md);
  border-left: 4px solid var(--accent-yellow);
  background: rgba(255, 200, 61, 0.08);
  color: var(--accent-yellow);
}

/* ========== L13 — Objectives ========== */
.layout-l13 .objectives {
  list-style: none;
  padding: 0;
  max-width: 960px;
  margin-top: var(--space-md);
  counter-reset: obj;
}
.layout-l13 .objectives li {
  padding: var(--space-md) var(--space-lg) var(--space-md) 80px;
  background: var(--bg-secondary);
  margin-bottom: var(--space-sm);
  border-left: 4px solid var(--brand-blue);
  position: relative;
  counter-increment: obj;
}
.layout-l13 .objectives li::before {
  content: counter(obj, decimal-leading-zero);
  position: absolute;
  left: var(--space-lg);
  top: 50%;
  transform: translateY(-50%);
  color: var(--brand-blue);
  font-size: var(--font-size-h3);
  font-weight: 700;
}

/* ========== L14 — Summary ========== */
.layout-l14 .takeaways {
  list-style: none;
  padding: 0;
  max-width: 960px;
  margin-top: var(--space-md);
}
.layout-l14 .takeaways li {
  padding: var(--space-md) var(--space-lg);
  background: var(--bg-secondary);
  border-left: 4px solid var(--accent-yellow);
  margin-bottom: var(--space-sm);
}
```

### Task 1B.3: Write test-layouts.html + test-layouts.js

**Files:**
- Create: `~/Desktop/elearning-workspace/dev/test-layouts.html`
- Create: `~/Desktop/elearning-workspace/dev/test-layouts.js`

- [ ] **Step 1: Write test-layouts.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Layout test harness</title>
  <link rel="stylesheet" href="../shell/css/theme-dark.css">
  <link rel="stylesheet" href="../shell/css/layouts.css">
  <style>
    body { padding: 40px 0; }
    .test-section { margin-bottom: 80px; }
    .test-section h2.label {
      color: var(--brand-blue);
      max-width: var(--slide-width);
      margin: 0 auto var(--space-sm);
      padding: 0 var(--slide-padding);
    }
  </style>
</head>
<body>
  <section class="test-section">
    <h2 class="label">L01 — Text only</h2>
    <div id="test-l01"></div>
  </section>

  <section class="test-section">
    <h2 class="label">L03 — 60/40 media + text</h2>
    <div id="test-l03"></div>
  </section>

  <section class="test-section">
    <h2 class="label">L09 — MCQ (default / selected / correct / incorrect)</h2>
    <div id="test-l09-default"></div>
    <div id="test-l09-selected"></div>
    <div id="test-l09-correct"></div>
    <div id="test-l09-incorrect"></div>
  </section>

  <section class="test-section">
    <h2 class="label">L12 — Menu hub (fresh / midway / popup open)</h2>
    <div id="test-l12-fresh"></div>
    <div id="test-l12-midway"></div>
    <div id="test-l12-popup"></div>
  </section>

  <section class="test-section">
    <h2 class="label">L13 — Objectives</h2>
    <div id="test-l13"></div>
  </section>

  <section class="test-section">
    <h2 class="label">L14 — Summary</h2>
    <div id="test-l14"></div>
  </section>

  <script src="test-layouts.js"></script>
</body>
</html>
```

- [ ] **Step 2: Write test-layouts.js**

```js
// Sample renderers — one per MVP layout state. Must match the exact class names / structure
// that shell/js/app.js will produce in Phase 2. Keep these in sync.

// L01
document.getElementById("test-l01").innerHTML = `
  <div class="slide layout-l01">
    <span class="module-label">Module 2.5</span>
    <h1>Why procurement planning matters</h1>
    <div class="body">
      <p>Procurement decisions shape cost, risk, and delivery timing across the entire project.</p>
      <ul class="bullets">
        <li>Sets the commercial framework for every vendor relationship</li>
        <li>Locks in trade-offs between speed, cost, and quality</li>
        <li>Determines which risks you own and which transfer to suppliers</li>
      </ul>
    </div>
  </div>
`;

// L03
document.getElementById("test-l03").innerHTML = `
  <div class="slide layout-l03">
    <span class="module-label">Module 2.5</span>
    <h1>What is a procurement plan</h1>
    <div class="grid">
      <div class="media">{{MEDIA_1}}<br>photo of signed contract on desk</div>
      <div class="text">
        <ul class="bullets">
          <li>A document that defines how purchases will be managed</li>
          <li>Covers vendor selection, contract type, and delivery timing</li>
          <li>Lives across the project lifecycle — not a one-time artifact</li>
        </ul>
      </div>
    </div>
  </div>
`;

// L09 — 4 states
const l09Options = [
  "Team sprint cadence and ceremonies",
  "Stakeholder communication schedule",
  "Contract type (fixed-price vs time-and-materials)",
  "Risk register ownership"
];
function renderL09(mount, { selectedIdx = null, submitted = false, isCorrect = null }) {
  const correctIdx = 2;
  const opts = l09Options.map((o, i) => {
    const cls = [];
    if (submitted) cls.push("disabled");
    if (selectedIdx === i && !submitted) cls.push("selected");
    if (submitted && i === correctIdx) cls.push("correct-answer");
    if (submitted && selectedIdx === i && i !== correctIdx) cls.push("wrong-answer");
    return `<li class="${cls.join(' ')}">${o}</li>`;
  }).join("");
  const quiz = `
    <span class="module-label">Knowledge check</span>
    <h1>Which of these belongs in a procurement plan?</h1>
    <p class="stem">Select the statement that is most clearly a procurement-plan concern, not a project-plan concern.</p>
    <ul class="options">${opts}</ul>
    ${!submitted ? `<button class="submit-btn" ${selectedIdx == null ? 'disabled' : ''}>Submit</button>` : ''}
  `;
  if (!submitted) {
    document.getElementById(mount).innerHTML = `<div class="slide layout-l09">${quiz}</div>`;
  } else {
    const fbClass = isCorrect ? "correct" : "incorrect";
    const fbTitle = isCorrect ? "Correct" : "Not quite";
    const fbText = isCorrect
      ? "Contract type is a core procurement-plan decision — it shapes risk allocation and payment structure."
      : "That option is a general project-management concern. The green-outlined option is the procurement-plan answer.";
    document.getElementById(mount).innerHTML = `
      <div class="slide layout-l09 submitted">
        <div class="l09-split">
          <div>${quiz}</div>
          <aside class="feedback-panel ${fbClass}">
            <h3>${fbTitle}</h3>
            <p>${fbText}</p>
            <button class="submit-btn">Continue</button>
          </aside>
        </div>
      </div>
    `;
  }
}
renderL09("test-l09-default", {});
renderL09("test-l09-selected", { selectedIdx: 2 });
renderL09("test-l09-correct", { selectedIdx: 2, submitted: true, isCorrect: true });
renderL09("test-l09-incorrect", { selectedIdx: 1, submitted: true, isCorrect: false });

// L12 — 3 states
const l12Bars = [
  { num: "01", title: "Objectives and criteria" },
  { num: "02", title: "Scope and packaging" },
  { num: "03", title: "Procurement method" },
  { num: "04", title: "Contract type" },
  { num: "05", title: "Evaluation approach" },
  { num: "06", title: "Risk and contingency" },
  { num: "07", title: "Schedule and milestones" },
  { num: "08", title: "Governance and approvals" }
];
function renderL12(mountId, visitedIdxs, popupIdx) {
  const bars = l12Bars.map((b, i) => `
    <li class="bar${visitedIdxs.includes(i) ? ' visited' : ''}">
      <span class="num">${b.num}</span>
      <span class="title-text">${b.title}</span>
      <span class="check">✓</span>
    </li>
  `).join("");
  const popup = popupIdx != null ? `
    <div class="popup-backdrop">
      <div class="popup-panel">
        <div class="popup-header">
          <span class="num">${l12Bars[popupIdx].num}</span>
          <span class="popup-title">${l12Bars[popupIdx].title}</span>
          <button class="popup-close">×</button>
        </div>
        <div class="popup-body">
          <ul class="bullets">
            <li>Clear measurable targets aligned to sponsor expectations</li>
            <li>Evaluation criteria weighted by strategic priority</li>
            <li>Acceptance thresholds agreed with the steering group</li>
          </ul>
          <div class="popup-key-message">Tie every criterion back to a sponsor-owned success measure.</div>
        </div>
      </div>
    </div>
  ` : '';
  const cls = popupIdx != null ? 'popup-open' : '';
  document.getElementById(mountId).innerHTML = `
    <div class="slide layout-l12 ${cls}">
      <span class="module-label">Plan structure</span>
      <h1>Explore each component of the plan</h1>
      <ul class="bars">${bars}</ul>
      ${popup}
    </div>
  `;
}
renderL12("test-l12-fresh", [], null);
renderL12("test-l12-midway", [0, 2, 5], null);
renderL12("test-l12-popup", [0, 2], 0);

// L13
document.getElementById("test-l13").innerHTML = `
  <div class="slide layout-l13">
    <span class="module-label">Module 2.5</span>
    <h1>What you will be able to do</h1>
    <ul class="objectives">
      <li>Differentiate a procurement plan from a project plan using concrete scope examples</li>
      <li>Select the appropriate packaging strategy for a given set of project constraints</li>
      <li>Justify contract-type choice (fixed-price vs T&amp;M) against risk allocation trade-offs</li>
    </ul>
  </div>
`;

// L14
document.getElementById("test-l14").innerHTML = `
  <div class="slide layout-l14">
    <span class="module-label">Module 2.5 — Summary</span>
    <h1>Key takeaways</h1>
    <ul class="takeaways">
      <li>A procurement plan answers "how will we buy?" — separate from the project plan's "what and when?"</li>
      <li>Packaging and contract type decisions shape risk allocation before any vendor is involved</li>
      <li>Every criterion should trace back to a sponsor-owned success measure</li>
    </ul>
  </div>
`;
```

- [ ] **Step 3: Open in browser for sanity check**

```bash
open ~/Desktop/elearning-workspace/dev/test-layouts.html
```

- [ ] **Step 4: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add shell/css/ dev/test-layouts.html dev/test-layouts.js
git commit -m "feat(shell): dark-theme CSS + 6 MVP layouts + test harness"
```

### Task 1B.4: 🛑 CHECKPOINT C2 — User visual review of all 6 layouts

- [ ] **Step 1: Present to Qianhui**

> **Your turn (10 min):**
> 1. `open ~/Desktop/elearning-workspace/dev/test-layouts.html`
> 2. Scroll through all 6 sections.
> 3. Things to look at:
>    - Colors (BG #1C2333, Parthenon Blue #1A9AFA)
>    - L01 dash bullets with blue dash
>    - L03 60/40 split (media left, bullets right)
>    - L09 option states (default / selected border-blue / correct green / incorrect red), feedback panel on right 1/3
>    - L12 bars stacked vertically with blue left border, "01" num + title, checkmark on visited bars, popup = dark panel with blue border
>    - L13 objectives with "01/02/03" big blue numbers
>    - L14 takeaways with yellow accent bar
> 4. If something's wrong, describe it plainly — don't fix CSS yourself. I route to the right file.
> 5. When all 6 look right, say "C2 passed".

- [ ] **Step 2: Iterate on CSS based on feedback.** Each fix = edit `shell/css/theme-dark.css` or `shell/css/layouts.css` → ask user to refresh browser → confirm.

- [ ] **Step 3: Commit on approval**

```bash
cd ~/Desktop/elearning-workspace
git add shell/css/
git commit -m "feat(shell): C2 visual review passed — CSS locked"
```

---

## Phase 2 — Shell runtime (content.json schema + index.html + app.js)

Goal: Build the JS runtime that reads a `content.json` file and renders slides using the CSS from Phase 1B. By the end, `shell/index.html` + a bundled `content.sample.json` runs the full flow in the browser with navigation, MCQ state, L12 state, and SCORM integration.

### Task 2.1: Document content.json schema

**Files:**
- Create: `~/Desktop/elearning-workspace/shell/content.schema.md`

- [ ] **Step 1: Write schema doc**

````markdown
# content.json schema (MVP, intentionally loose)

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

### L01 — text only
- `body` (array of strings) — each item is a paragraph OR a bullet (bullet starts with `- `)

### L03 — 60/40 media + text
- `media` (object): `{ "placeholder": "alt text" }`
- `bullets` (array of strings)

### L09 — MCQ
- `stem` (string)
- `options` (array of strings)
- `correct_index` (number, 0-based)
- `feedback_correct` (string)
- `feedback_incorrect` (string)
- `points` (number, default 25) — contribution to final score (0–100)

### L12 — menu hub
- `bars` (array of objects): each `{ "num": "01", "title": "...", "popup_slide_id": "id-of-popup-slide" }`
- Popup content is stored in separate slides with `layout: "popup"` — referenced via `popup_slide_id`.

### popup — internal, used only as L12 popup target
- `body` (array of strings, same bullet convention as L01)
- `key_message` (string, optional) — rendered as yellow accent bar

### L13 — objectives
- `objectives` (array of strings)

### L14 — summary
- `takeaways` (array of strings)
- On entry, runtime sets `cmi.core.lesson_status = "completed"` and writes score.

## Navigation rules
- Visible slides = all slides except `layout: "popup"` (popups are rendered inline on their host L12).
- Previous/Next advance between visible slides.
- On L09: Next disabled until MCQ submitted.
- On L12: Next disabled until all bars visited.
- On L14 first entry: mark complete + write score to SCORM.
- Clicking "Finish" on last slide → LMSFinish.
````

### Task 2.2: Write shell/index.html + nav.css

**Files:**
- Create: `~/Desktop/elearning-workspace/shell/index.html`
- Create: `~/Desktop/elearning-workspace/shell/css/nav.css`

- [ ] **Step 1: Write index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>eLearning module</title>
  <link rel="stylesheet" href="css/theme-dark.css">
  <link rel="stylesheet" href="css/layouts.css">
  <link rel="stylesheet" href="css/nav.css">
  <script src="js/pipwerks_scorm.js"></script>
</head>
<body>
  <div id="app"></div>
  <nav id="nav">
    <button id="btn-prev">Previous</button>
    <span id="progress"></span>
    <button id="btn-next">Next</button>
    <button id="btn-exit">Exit</button>
  </nav>
  <script src="js/app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Write nav.css**

```css
#nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg-secondary);
  padding: var(--space-sm) var(--space-lg);
  display: flex;
  align-items: center;
  gap: var(--space-md);
  border-top: 1px solid var(--bg-elevated);
  z-index: 50;
}
#nav button {
  padding: var(--space-sm) var(--space-lg);
  background: var(--brand-blue);
  color: #fff;
  border: none;
  font-size: 16px;
  cursor: pointer;
}
#nav button:disabled { background: var(--text-muted); cursor: not-allowed; }
#nav #progress { margin-left: auto; margin-right: var(--space-md); color: var(--text-secondary); }
#nav #btn-exit { background: var(--bg-elevated); }
body { padding-bottom: 80px; }
```

### Task 2.3: Write shell/js/app.js — core runtime

**Files:**
- Create: `~/Desktop/elearning-workspace/shell/js/app.js`

- [ ] **Step 1: Write app.js**

```js
(function () {
  "use strict";

  const scorm = pipwerks.SCORM;
  scorm.version = "1.2";

  // ---------- Module state ----------
  const state = {
    content: null,
    currentIdx: 0,
    mcqState: {},   // slide_id → { selectedIdx, submitted, isCorrect }
    menuState: {},  // slide_id → { visited: Set<number>, openBar: number|null }
    scormActive: false,
    totalScore: 0,
    maxScore: 0,
    completed: false
  };

  // ---------- Load content.json ----------
  async function loadContent() {
    const resp = await fetch("content.json");
    if (!resp.ok) throw new Error("Failed to load content.json: " + resp.status);
    return resp.json();
  }

  // ---------- Init ----------
  async function init() {
    try {
      state.content = await loadContent();
    } catch (e) {
      document.getElementById("app").innerHTML =
        `<div class="slide"><h1>Error loading module</h1><p>${e.message}</p></div>`;
      return;
    }
    document.title = state.content.module.title;

    state.maxScore = state.content.slides
      .filter(s => s.layout === "L09")
      .reduce((sum, s) => sum + (s.points != null ? s.points : 25), 0);

    state.scormActive = scorm.init();
    if (state.scormActive) {
      scorm.set("cmi.core.lesson_status", "incomplete");
      scorm.save();
    }

    bindNav();
    renderSlide();
    window.addEventListener("beforeunload", onExit);
  }

  // ---------- Helpers ----------
  function visibleSlides() {
    return state.content.slides.filter(s => s.layout !== "popup");
  }
  function findSlideById(id) {
    return state.content.slides.find(s => s.id === id);
  }
  function currentSlide() {
    return visibleSlides()[state.currentIdx];
  }

  // ---------- Render ----------
  function renderSlide() {
    const slide = currentSlide();
    const app = document.getElementById("app");
    app.innerHTML = "";
    app.appendChild(renderByLayout(slide));

    const visible = visibleSlides();
    document.getElementById("progress").textContent =
      `Slide ${state.currentIdx + 1} of ${visible.length}`;
    document.getElementById("btn-prev").disabled = state.currentIdx === 0;

    const nextBtn = document.getElementById("btn-next");
    nextBtn.disabled = !canAdvance();
    nextBtn.textContent = state.currentIdx === visible.length - 1 ? "Finish" : "Next";

    // Summary triggers completion on first visit
    if (slide.layout === "L14" && !state.completed) {
      markComplete();
    }
  }

  function canAdvance() {
    const slide = currentSlide();
    if (slide.layout === "L09") {
      const mcq = state.mcqState[slide.id];
      return !!(mcq && mcq.submitted);
    }
    if (slide.layout === "L12") {
      const menu = state.menuState[slide.id] || { visited: new Set() };
      return menu.visited.size >= slide.bars.length;
    }
    return true;
  }

  function renderByLayout(slide) {
    switch (slide.layout) {
      case "L01": return renderL01(slide);
      case "L03": return renderL03(slide);
      case "L09": return renderL09(slide);
      case "L12": return renderL12(slide);
      case "L13": return renderL13(slide);
      case "L14": return renderL14(slide);
      default:
        const el = document.createElement("div");
        el.className = "slide";
        el.textContent = `Unknown layout: ${slide.layout}`;
        return el;
    }
  }

  function moduleLabelHtml() {
    return `<span class="module-label">${esc(state.content.module.module_label || "")}</span>`;
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderBodyLines(lines) {
    const bullets = [];
    const paras = [];
    let currentBullets = null;
    const parts = [];
    lines.forEach(line => {
      if (line.startsWith("- ")) {
        if (!currentBullets) { currentBullets = []; parts.push({ type: "bullets", items: currentBullets }); }
        currentBullets.push(line.slice(2));
      } else {
        currentBullets = null;
        parts.push({ type: "p", text: line });
      }
    });
    return parts.map(p => {
      if (p.type === "p") return `<p>${esc(p.text)}</p>`;
      return `<ul class="bullets">${p.items.map(i => `<li>${esc(i)}</li>`).join("")}</ul>`;
    }).join("");
  }

  // ---------- Layout renderers ----------
  function renderL01(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l01";
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <div class="body">${renderBodyLines(slide.body || [])}</div>
    `;
    return el;
  }

  function renderL03(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l03";
    const media = slide.media || { placeholder: "media placeholder" };
    const bullets = (slide.bullets || []).map(b => `<li>${esc(b)}</li>`).join("");
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <div class="grid">
        <div class="media">{{MEDIA_1}}<br>${esc(media.placeholder)}</div>
        <div class="text"><ul class="bullets">${bullets}</ul></div>
      </div>
    `;
    return el;
  }

  function renderL09(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l09";
    const mcq = state.mcqState[slide.id] || { selectedIdx: null, submitted: false, isCorrect: null };

    function draw() {
      if (!mcq.submitted) {
        const opts = slide.options.map((o, i) => {
          const cls = mcq.selectedIdx === i ? "selected" : "";
          return `<li class="${cls}" data-idx="${i}">${esc(o)}</li>`;
        }).join("");
        el.classList.remove("submitted");
        el.innerHTML = `
          ${moduleLabelHtml()}
          <h1>${esc(slide.title)}</h1>
          <p class="stem">${esc(slide.stem)}</p>
          <ul class="options">${opts}</ul>
          <button class="submit-btn" ${mcq.selectedIdx == null ? "disabled" : ""}>Submit</button>
        `;
        el.querySelectorAll(".options li").forEach(li => {
          li.addEventListener("click", () => {
            mcq.selectedIdx = parseInt(li.dataset.idx, 10);
            state.mcqState[slide.id] = mcq;
            draw();
          });
        });
        el.querySelector(".submit-btn").addEventListener("click", () => {
          if (mcq.selectedIdx == null) return;
          mcq.submitted = true;
          mcq.isCorrect = mcq.selectedIdx === slide.correct_index;
          state.mcqState[slide.id] = mcq;
          if (mcq.isCorrect) {
            state.totalScore += (slide.points != null ? slide.points : 25);
          }
          draw();
          // Re-evaluate Next button
          const nextBtn = document.getElementById("btn-next");
          if (nextBtn) nextBtn.disabled = !canAdvance();
        });
      } else {
        const opts = slide.options.map((o, i) => {
          const cls = ["disabled"];
          if (i === slide.correct_index) cls.push("correct-answer");
          if (mcq.selectedIdx === i && i !== slide.correct_index) cls.push("wrong-answer");
          return `<li class="${cls.join(' ')}">${esc(o)}</li>`;
        }).join("");
        const fbClass = mcq.isCorrect ? "correct" : "incorrect";
        const fbTitle = mcq.isCorrect ? "Correct" : "Not quite";
        const fbText = mcq.isCorrect ? slide.feedback_correct : slide.feedback_incorrect;
        el.classList.add("submitted");
        el.innerHTML = `
          <div class="l09-split">
            <div>
              ${moduleLabelHtml()}
              <h1>${esc(slide.title)}</h1>
              <p class="stem">${esc(slide.stem)}</p>
              <ul class="options">${opts}</ul>
            </div>
            <aside class="feedback-panel ${fbClass}">
              <h3>${fbTitle}</h3>
              <p>${esc(fbText)}</p>
            </aside>
          </div>
        `;
      }
    }
    draw();
    return el;
  }

  function renderL12(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l12";
    const menu = state.menuState[slide.id] || { visited: new Set(), openBar: null };
    state.menuState[slide.id] = menu;

    function draw() {
      const bars = slide.bars.map((b, i) => `
        <li class="bar${menu.visited.has(i) ? ' visited' : ''}" data-idx="${i}">
          <span class="num">${esc(b.num)}</span>
          <span class="title-text">${esc(b.title)}</span>
          <span class="check">✓</span>
        </li>
      `).join("");

      let popupHtml = "";
      if (menu.openBar != null) {
        const bar = slide.bars[menu.openBar];
        const popupSlide = findSlideById(bar.popup_slide_id);
        if (popupSlide) {
          const body = renderBodyLines(popupSlide.body || []);
          const keyMsg = popupSlide.key_message
            ? `<div class="popup-key-message">${esc(popupSlide.key_message)}</div>`
            : "";
          popupHtml = `
            <div class="popup-backdrop">
              <div class="popup-panel">
                <div class="popup-header">
                  <span class="num">${esc(bar.num)}</span>
                  <span class="popup-title">${esc(bar.title)}</span>
                  <button class="popup-close">×</button>
                </div>
                <div class="popup-body">${body}${keyMsg}</div>
              </div>
            </div>
          `;
        }
      }

      el.classList.toggle("popup-open", menu.openBar != null);
      el.innerHTML = `
        ${moduleLabelHtml()}
        <h1>${esc(slide.title)}</h1>
        <ul class="bars">${bars}</ul>
        ${popupHtml}
      `;

      el.querySelectorAll(".bars .bar").forEach(li => {
        li.addEventListener("click", () => {
          menu.openBar = parseInt(li.dataset.idx, 10);
          menu.visited.add(menu.openBar);
          draw();
          const nextBtn = document.getElementById("btn-next");
          if (nextBtn) nextBtn.disabled = !canAdvance();
        });
      });
      const closeBtn = el.querySelector(".popup-close");
      if (closeBtn) {
        closeBtn.addEventListener("click", () => {
          menu.openBar = null;
          draw();
        });
      }
    }

    draw();
    return el;
  }

  function renderL13(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l13";
    const items = (slide.objectives || []).map(o => `<li>${esc(o)}</li>`).join("");
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <ul class="objectives">${items}</ul>
    `;
    return el;
  }

  function renderL14(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l14";
    const items = (slide.takeaways || []).map(t => `<li>${esc(t)}</li>`).join("");
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <ul class="takeaways">${items}</ul>
    `;
    return el;
  }

  // ---------- Navigation ----------
  function bindNav() {
    document.getElementById("btn-prev").addEventListener("click", () => {
      if (state.currentIdx > 0) { state.currentIdx--; renderSlide(); }
    });
    document.getElementById("btn-next").addEventListener("click", () => {
      if (!canAdvance()) return;
      const visible = visibleSlides();
      if (state.currentIdx < visible.length - 1) {
        state.currentIdx++;
        renderSlide();
      } else {
        onExit();
      }
    });
    document.getElementById("btn-exit").addEventListener("click", onExit);
  }

  // ---------- SCORM ----------
  function markComplete() {
    state.completed = true;
    if (!state.scormActive) return;
    scorm.set("cmi.core.lesson_status", "completed");
    if (state.maxScore > 0) {
      const pct = Math.max(0, Math.min(100, Math.round((state.totalScore / state.maxScore) * 100)));
      scorm.set("cmi.core.score.raw", String(pct));
      scorm.set("cmi.core.score.min", "0");
      scorm.set("cmi.core.score.max", "100");
    }
    scorm.save();
  }

  function onExit() {
    if (state.scormActive) {
      scorm.save();
      scorm.quit();
      state.scormActive = false;
    }
    try { window.close(); } catch (e) {}
  }

  document.addEventListener("DOMContentLoaded", init);
})();
```

### Task 2.4: Write a hand-built content.sample.json for shell testing

**Files:**
- Create: `~/Desktop/elearning-workspace/shell/content.sample.json`

- [ ] **Step 1: Write sample**

```json
{
  "module": {
    "id": "sample",
    "title": "Shell runtime test",
    "module_label": "Sample",
    "scorm_identifier": "com.qianhui.sample"
  },
  "slides": [
    {
      "id": "01-objectives",
      "layout": "L13",
      "title": "What you will be able to do",
      "objectives": [
        "Differentiate a procurement plan from a project plan",
        "Select a packaging strategy for given constraints"
      ]
    },
    {
      "id": "02-intro",
      "layout": "L01",
      "title": "Why this matters",
      "body": [
        "Procurement shapes cost, risk, and timing across the whole project.",
        "- Sets the commercial framework for every vendor relationship",
        "- Locks in risk allocation before any vendor is chosen",
        "- Determines delivery leverage for the life of the project"
      ]
    },
    {
      "id": "03-what-is",
      "layout": "L03",
      "title": "What is a procurement plan",
      "media": { "placeholder": "photo of signed contract on desk" },
      "bullets": [
        "A document that defines how purchases will be managed",
        "Covers vendor selection, contract type, and delivery timing",
        "Lives across the project lifecycle"
      ]
    },
    {
      "id": "04-menu",
      "layout": "L12",
      "title": "Explore the plan components",
      "bars": [
        { "num": "01", "title": "Objectives and criteria", "popup_slide_id": "04p-objectives" },
        { "num": "02", "title": "Scope and packaging", "popup_slide_id": "04p-scope" }
      ]
    },
    {
      "id": "04p-objectives",
      "layout": "popup",
      "title": "Objectives and criteria",
      "body": [
        "- Clear measurable targets aligned to sponsor expectations",
        "- Weighted evaluation criteria",
        "- Agreed acceptance thresholds"
      ],
      "key_message": "Tie every criterion to a sponsor-owned success measure."
    },
    {
      "id": "04p-scope",
      "layout": "popup",
      "title": "Scope and packaging",
      "body": [
        "- Decide single-package vs multi-package procurement",
        "- Balance integration risk against vendor leverage"
      ]
    },
    {
      "id": "05-check",
      "layout": "L09",
      "title": "Knowledge check",
      "stem": "Which of these belongs in a procurement plan, not a project plan?",
      "options": [
        "Sprint cadence and ceremonies",
        "Stakeholder communication schedule",
        "Contract type (fixed-price vs T&M)",
        "Risk register ownership"
      ],
      "correct_index": 2,
      "feedback_correct": "Contract type is a core procurement-plan decision — it shapes risk allocation.",
      "feedback_incorrect": "That is a general project-management concern. Contract type (option 3) is the procurement answer.",
      "points": 100
    },
    {
      "id": "06-summary",
      "layout": "L14",
      "title": "Key takeaways",
      "takeaways": [
        "A procurement plan answers 'how will we buy?' — distinct from the project plan",
        "Packaging and contract type allocate risk before any vendor is involved",
        "Every criterion should trace back to a sponsor-owned success measure"
      ]
    }
  ]
}
```

- [ ] **Step 2: Symlink sample → content.json for shell dry-run**

```bash
cd ~/Desktop/elearning-workspace/shell
ln -sf content.sample.json content.json
```

- [ ] **Step 3: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add shell/index.html shell/css/nav.css shell/js/app.js shell/content.schema.md shell/content.sample.json shell/content.json
git commit -m "feat(shell): runtime (index.html + nav + app.js + sample content)"
```

### Task 2.5: 🛑 CHECKPOINT C3 — User walks the shell sample in browser

Serving via `file://` works for most of app.js but `fetch("content.json")` may fail on some browsers due to CORS for local files. Use a local static server for the walkthrough.

- [ ] **Step 1: Start local static server**

```bash
cd ~/Desktop/elearning-workspace/shell
python3 -m http.server 8765 &
```

- [ ] **Step 2: Present to Qianhui**

> **Your turn (10 min):**
> 1. Open http://localhost:8765/ in your browser.
> 2. Walk through the whole module using Previous / Next / Finish:
>    - Slide 1: objectives (L13) — two items
>    - Slide 2: Why this matters (L01)
>    - Slide 3: What is a procurement plan (L03) — media placeholder left, bullets right
>    - Slide 4: menu hub (L12) — click both bars, open each popup, click × to close. Next button should only enable after BOTH bars are visited.
>    - Slide 5: knowledge check (L09) — try answering wrong first → red feedback on right. Refresh and try correct → green feedback. Next enabled after submit.
>    - Slide 6: summary (L14) — shows takeaways. Button reads "Finish".
> 3. Tell me any visible bugs (popup doesn't close, checkmark doesn't appear, Next button stuck, etc.)
> 4. Don't worry about SCORM yet — you're looking at content and interaction behavior.
> 5. When it all works, say "C3 passed".

- [ ] **Step 3: Iterate on bugs.** Fix in shell JS/CSS, refresh browser, re-verify.

- [ ] **Step 4: Stop the local server**

```bash
pkill -f "http.server 8765" || true
```

- [ ] **Step 5: Remove the symlink (it exists only for local testing; real modules wire in their own content.json)**

```bash
rm ~/Desktop/elearning-workspace/shell/content.json
```

- [ ] **Step 6: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add -A
git commit -m "feat(shell): C3 runtime walkthrough passed"
```

---

## Phase 3 — Build scripts

Goal: Write the three Python helpers that the skills will call: `merge_content.py`, `fill_manifest.py`, `pack_scorm.py`. Each is covered by pytest cases.

### Task 3.1: Write manifest-template.xml

**Files:**
- Create: `~/Desktop/elearning-workspace/shell/manifest-template.xml`

- [ ] **Step 1: Write Jinja template**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{{ identifier }}" version="{{ version }}"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
          xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://www.imsproject.org/xsd/imscp_rootv1p1p2 imscp_rootv1p1p2.xsd
                              http://www.imsglobal.org/xsd/imsmd_rootv1p2p1 imsmd_rootv1p2p1.xsd
                              http://www.adlnet.org/xsd/adlcp_rootv1p2 adlcp_rootv1p2.xsd">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>
  <organizations default="DEFAULT_ORG">
    <organization identifier="DEFAULT_ORG">
      <title>{{ title }}</title>
      <item identifier="ITEM_01" identifierref="RES_01" isvisible="true">
        <title>{{ title }}</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="RES_01" type="webcontent" adlcp:scormtype="sco" href="index.html">
{% for f in files %}      <file href="{{ f }}"/>
{% endfor %}    </resource>
  </resources>
</manifest>
```

### Task 3.2: Write merge_content.py + tests

**Files:**
- Create: `~/Desktop/elearning-workspace/scripts/merge_content.py`
- Create: `~/Desktop/elearning-workspace/scripts/tests/test_merge_content.py`

- [ ] **Step 1: Write merge_content.py**

```python
"""Merge content/*.md slide files into a single content.json.

Each slide file has YAML frontmatter + markdown body. The frontmatter is the
structured metadata (id, layout, title, layout-specific fields). The body is
parsed loosely into layout-specific fields if not already specified in the
frontmatter.

Usage:
    python3 merge_content.py <module_dir>

<module_dir> must contain:
    content/*.md   (slide files)
    module.yml     (module-level metadata: id, title, module_label, scorm_identifier)

Writes:
    build/content.json
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
import yaml


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def parse_slide_file(path: Path) -> dict:
    """Parse a single content/*.md slide file → dict suitable for content.json."""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"{path}: missing YAML frontmatter")
    frontmatter = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)

    slide = dict(frontmatter)
    if "id" not in slide:
        slide["id"] = path.stem
    if "layout" not in slide:
        raise ValueError(f"{path}: missing 'layout' in frontmatter")

    # If layout-specific fields are not already in frontmatter, try to extract
    # them from body sections (## On-screen, ## Body, etc.). For MVP we accept
    # frontmatter-only slides.
    return slide


def load_module_metadata(module_dir: Path) -> dict:
    module_yml = module_dir / "module.yml"
    if not module_yml.exists():
        raise FileNotFoundError(f"{module_yml} not found")
    return yaml.safe_load(module_yml.read_text(encoding="utf-8"))


def merge(module_dir: Path) -> dict:
    content_dir = module_dir / "content"
    if not content_dir.is_dir():
        raise FileNotFoundError(f"{content_dir} not found")
    slide_files = sorted(content_dir.glob("*.md"))
    if not slide_files:
        raise ValueError(f"no slide files in {content_dir}")
    slides = [parse_slide_file(p) for p in slide_files]
    return {
        "module": load_module_metadata(module_dir),
        "slides": slides,
    }


def write_content_json(module_dir: Path) -> Path:
    data = merge(module_dir)
    build_dir = module_dir / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    out = build_dir / "content.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 merge_content.py <module_dir>", file=sys.stderr)
        sys.exit(2)
    module_dir = Path(sys.argv[1]).expanduser().resolve()
    out = write_content_json(module_dir)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Write test_merge_content.py**

```python
import json
from pathlib import Path
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from merge_content import parse_slide_file, merge, write_content_json


def make_module(tmp_path: Path) -> Path:
    (tmp_path / "content").mkdir()
    (tmp_path / "module.yml").write_text(
        "id: test\ntitle: Test Module\nmodule_label: Test\nscorm_identifier: com.test\n"
    )
    return tmp_path


def test_parse_slide_minimal(tmp_path):
    f = tmp_path / "01-intro.md"
    f.write_text("---\nlayout: L01\ntitle: Intro\nbody:\n  - Hello\n---\n")
    slide = parse_slide_file(f)
    assert slide["id"] == "01-intro"
    assert slide["layout"] == "L01"
    assert slide["title"] == "Intro"
    assert slide["body"] == ["Hello"]


def test_parse_slide_missing_layout_raises(tmp_path):
    f = tmp_path / "01-intro.md"
    f.write_text("---\ntitle: Intro\n---\n")
    with pytest.raises(ValueError, match="layout"):
        parse_slide_file(f)


def test_parse_slide_missing_frontmatter_raises(tmp_path):
    f = tmp_path / "01-intro.md"
    f.write_text("Just some text, no frontmatter.")
    with pytest.raises(ValueError, match="frontmatter"):
        parse_slide_file(f)


def test_merge_produces_valid_structure(tmp_path):
    module_dir = make_module(tmp_path)
    (module_dir / "content" / "01-intro.md").write_text(
        "---\nlayout: L01\ntitle: Intro\nbody:\n  - Hello\n---\n"
    )
    (module_dir / "content" / "02-summary.md").write_text(
        "---\nlayout: L14\ntitle: Wrap\ntakeaways:\n  - Nice\n---\n"
    )
    data = merge(module_dir)
    assert data["module"]["id"] == "test"
    assert len(data["slides"]) == 2
    assert data["slides"][0]["layout"] == "L01"
    assert data["slides"][1]["layout"] == "L14"


def test_merge_sorts_by_filename(tmp_path):
    module_dir = make_module(tmp_path)
    for name, title in [("03-c.md", "C"), ("01-a.md", "A"), ("02-b.md", "B")]:
        (module_dir / "content" / name).write_text(
            f"---\nlayout: L01\ntitle: {title}\nbody: []\n---\n"
        )
    data = merge(module_dir)
    assert [s["title"] for s in data["slides"]] == ["A", "B", "C"]


def test_write_content_json(tmp_path):
    module_dir = make_module(tmp_path)
    (module_dir / "content" / "01.md").write_text(
        "---\nlayout: L01\ntitle: T\nbody: []\n---\n"
    )
    out = write_content_json(module_dir)
    assert out.exists()
    data = json.loads(out.read_text())
    assert data["module"]["id"] == "test"
    assert data["slides"][0]["title"] == "T"
```

- [ ] **Step 3: Run tests**

```bash
cd ~/Desktop/elearning-workspace
pytest scripts/tests/test_merge_content.py -v
```

Expected: all 5 tests pass.

- [ ] **Step 4: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add scripts/merge_content.py scripts/tests/test_merge_content.py shell/manifest-template.xml
git commit -m "feat(scripts): merge_content.py + tests + manifest template"
```

### Task 3.3: Write fill_manifest.py + tests

**Files:**
- Create: `~/Desktop/elearning-workspace/scripts/fill_manifest.py`
- Create: `~/Desktop/elearning-workspace/scripts/tests/test_fill_manifest.py`

- [ ] **Step 1: Write fill_manifest.py**

```python
"""Render shell/manifest-template.xml with module metadata + file list.

Usage:
    python3 fill_manifest.py <module_dir>

Reads <module_dir>/build/content.json for module metadata, enumerates files
under <module_dir>/build/ (excluding the manifest itself and the schemas dir),
renders the template, writes <module_dir>/build/imsmanifest.xml.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from jinja2 import Template


WORKSPACE = Path(__file__).parent.parent
TEMPLATE_PATH = WORKSPACE / "shell" / "manifest-template.xml"


def enumerate_files(build_dir: Path) -> list[str]:
    """List all files inside build/ as POSIX relative paths, excluding imsmanifest.xml."""
    files = []
    for p in sorted(build_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(build_dir).as_posix()
        if rel == "imsmanifest.xml":
            continue
        files.append(rel)
    return files


def render(module_meta: dict, files: list[str]) -> str:
    template = Template(TEMPLATE_PATH.read_text(encoding="utf-8"), keep_trailing_newline=True)
    return template.render(
        identifier=module_meta.get("scorm_identifier", module_meta["id"]),
        version="1.0",
        title=module_meta["title"],
        files=files,
    )


def write_manifest(module_dir: Path) -> Path:
    build_dir = module_dir / "build"
    content_json = build_dir / "content.json"
    if not content_json.exists():
        raise FileNotFoundError(f"{content_json} not found — run merge_content first")
    data = json.loads(content_json.read_text(encoding="utf-8"))
    files = enumerate_files(build_dir)
    manifest_xml = render(data["module"], files)
    out = build_dir / "imsmanifest.xml"
    out.write_text(manifest_xml, encoding="utf-8")
    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fill_manifest.py <module_dir>", file=sys.stderr)
        sys.exit(2)
    module_dir = Path(sys.argv[1]).expanduser().resolve()
    out = write_manifest(module_dir)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Write test_fill_manifest.py**

```python
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from fill_manifest import enumerate_files, render, write_manifest


def test_enumerate_files_skips_manifest(tmp_path):
    build = tmp_path / "build"
    build.mkdir()
    (build / "index.html").write_text("x")
    (build / "imsmanifest.xml").write_text("x")
    (build / "css").mkdir()
    (build / "css" / "theme.css").write_text("x")
    files = enumerate_files(build)
    assert "index.html" in files
    assert "css/theme.css" in files
    assert "imsmanifest.xml" not in files


def test_render_produces_valid_xml():
    meta = {"id": "m1", "title": "Test Module", "scorm_identifier": "com.test.m1"}
    files = ["index.html", "js/app.js", "css/theme.css"]
    xml = render(meta, files)
    root = ET.fromstring(xml)
    assert root.attrib["identifier"] == "com.test.m1"
    # Title appears at least once inside an <organization>
    assert "Test Module" in xml
    # File entries rendered
    assert 'href="index.html"' in xml
    assert 'href="js/app.js"' in xml
    assert 'href="css/theme.css"' in xml


def test_render_falls_back_to_id_when_no_scorm_identifier():
    meta = {"id": "m1", "title": "T"}
    xml = render(meta, ["index.html"])
    assert 'identifier="m1"' in xml


def test_write_manifest_end_to_end(tmp_path):
    module_dir = tmp_path / "mod"
    build = module_dir / "build"
    build.mkdir(parents=True)
    (build / "index.html").write_text("x")
    (build / "content.json").write_text(json.dumps({
        "module": {"id": "m1", "title": "Test", "scorm_identifier": "com.test.m1"},
        "slides": []
    }))
    out = write_manifest(module_dir)
    assert out.exists()
    root = ET.fromstring(out.read_text())
    assert root.tag.endswith("manifest")
```

- [ ] **Step 3: Run tests**

```bash
cd ~/Desktop/elearning-workspace
pytest scripts/tests/test_fill_manifest.py -v
```

Expected: all 4 tests pass.

- [ ] **Step 4: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add scripts/fill_manifest.py scripts/tests/test_fill_manifest.py
git commit -m "feat(scripts): fill_manifest.py + tests"
```

### Task 3.4: Write pack_scorm.py + tests

**Files:**
- Create: `~/Desktop/elearning-workspace/scripts/pack_scorm.py`
- Create: `~/Desktop/elearning-workspace/scripts/tests/test_pack_scorm.py`

- [ ] **Step 1: Write pack_scorm.py**

```python
"""Copy shell into <module_dir>/build/, merge content, fill manifest, zip.

Usage:
    python3 pack_scorm.py <module_dir>

Produces <module_dir>/dist/<module_id>.zip.
"""
from __future__ import annotations
import json
import shutil
import sys
import zipfile
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
SHELL_DIR = WORKSPACE / "shell"

sys.path.insert(0, str(Path(__file__).parent))
from merge_content import write_content_json
from fill_manifest import write_manifest


SHELL_COPY_ITEMS = ["index.html", "css", "js", "schemas", "assets"]


def copy_shell(module_dir: Path) -> None:
    build = module_dir / "build"
    build.mkdir(parents=True, exist_ok=True)
    for item in SHELL_COPY_ITEMS:
        src = SHELL_DIR / item
        if not src.exists():
            continue
        dst = build / item
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)


def zip_build(module_dir: Path, module_id: str) -> Path:
    build = module_dir / "build"
    dist = module_dir / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    out = dist / f"{module_id}.zip"
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(build.rglob("*")):
            if p.is_file():
                zf.write(p, p.relative_to(build).as_posix())
    return out


def validate_zip(zip_path: Path) -> list[str]:
    """Return a list of validation errors (empty if OK)."""
    errors = []
    if not zip_path.exists():
        return [f"zip file does not exist: {zip_path}"]
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if "imsmanifest.xml" not in names:
            errors.append("missing imsmanifest.xml at zip root")
        if "index.html" not in names:
            errors.append("missing index.html at zip root")
        # Manifest must be well-formed XML
        try:
            import xml.etree.ElementTree as ET
            with zf.open("imsmanifest.xml") as mf:
                ET.parse(mf)
        except Exception as e:
            errors.append(f"imsmanifest.xml not well-formed XML: {e}")
    return errors


def pack(module_dir: Path) -> Path:
    module_dir = module_dir.expanduser().resolve()
    copy_shell(module_dir)
    write_content_json(module_dir)
    write_manifest(module_dir)
    data = json.loads((module_dir / "build" / "content.json").read_text())
    module_id = data["module"]["id"]
    zip_path = zip_build(module_dir, module_id)
    errors = validate_zip(zip_path)
    if errors:
        raise RuntimeError("zip validation failed:\n" + "\n".join(errors))
    return zip_path


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 pack_scorm.py <module_dir>", file=sys.stderr)
        sys.exit(2)
    zip_path = pack(Path(sys.argv[1]))
    size_kb = zip_path.stat().st_size // 1024
    with zipfile.ZipFile(zip_path) as zf:
        file_count = len(zf.namelist())
    print(f"SCORM package built: {zip_path} ({size_kb} KB, {file_count} files)")
    print("Next step: upload to https://cloud.scorm.com → Add Content → Upload")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Write test_pack_scorm.py**

```python
import json
import zipfile
from pathlib import Path
import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from pack_scorm import pack, validate_zip


WORKSPACE = Path(__file__).parent.parent.parent


@pytest.fixture
def mini_module(tmp_path):
    module_dir = tmp_path / "mini"
    (module_dir / "content").mkdir(parents=True)
    (module_dir / "module.yml").write_text(
        "id: mini\ntitle: Mini Module\nmodule_label: Mini\nscorm_identifier: com.test.mini\n"
    )
    (module_dir / "content" / "01-intro.md").write_text(
        "---\nlayout: L01\ntitle: Hello\nbody:\n  - Hi\n---\n"
    )
    (module_dir / "content" / "02-summary.md").write_text(
        "---\nlayout: L14\ntitle: Wrap\ntakeaways:\n  - Done\n---\n"
    )
    return module_dir


def test_pack_produces_zip(mini_module):
    # The test relies on the real ~/Desktop/elearning-workspace/shell/ being present.
    # Skip gracefully if not.
    if not (WORKSPACE / "shell" / "index.html").exists():
        pytest.skip("shell not set up")
    zip_path = pack(mini_module)
    assert zip_path.exists()
    assert zip_path.name == "mini.zip"


def test_validate_zip_passes_on_good_zip(tmp_path):
    zpath = tmp_path / "ok.zip"
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("imsmanifest.xml", "<?xml version='1.0'?><manifest/>")
        zf.writestr("index.html", "<html/>")
    assert validate_zip(zpath) == []


def test_validate_zip_flags_missing_manifest(tmp_path):
    zpath = tmp_path / "bad.zip"
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("index.html", "<html/>")
    errors = validate_zip(zpath)
    assert any("imsmanifest.xml" in e for e in errors)


def test_validate_zip_flags_malformed_manifest(tmp_path):
    zpath = tmp_path / "bad.zip"
    with zipfile.ZipFile(zpath, "w") as zf:
        zf.writestr("imsmanifest.xml", "not xml at all")
        zf.writestr("index.html", "<html/>")
    errors = validate_zip(zpath)
    assert any("well-formed" in e.lower() for e in errors)
```

- [ ] **Step 3: Run tests**

```bash
cd ~/Desktop/elearning-workspace
pytest scripts/tests/ -v
```

Expected: all tests pass (test_pack_produces_zip will actually run since shell is present).

- [ ] **Step 4: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add scripts/pack_scorm.py scripts/tests/test_pack_scorm.py
git commit -m "feat(scripts): pack_scorm.py + tests"
```

---

## Phase 4 — The three skills

Goal: Write the three `SKILL.md` files that Claude invokes, symlink them into `~/.claude/skills/`.

### Task 4.1: Write content-map/SKILL.md

**Files:**
- Create: `~/Desktop/elearning-workspace/skills-src/content-map/SKILL.md`

- [ ] **Step 1: Write skill**

````markdown
---
name: content-map
description: Use when starting a new eLearning module — turns a brief, lesson plan, or seed content into a 4-column O-A-P-P (Objective / Assessment / Practice / Presentation) alignment table. First stage of the eLearning pipeline.
---

# /content-map

## Overview

Transforms a lesson brief into a tight alignment table. Every row links one learning objective to its assessment, its practice, and its presentation content. Forces alignment thinking BEFORE any slide design.

## When to use

- User invokes `/content-map`, or
- User asks to "map out content" / "plan a module" / "build a course on X"

## Input

Any of:
- A one-line brief ("30-min module on procurement planning for PMs")
- A lesson plan document (PDF, Word, pasted text)
- A seed example + user's ID intuition

## Workflow

1. **Parse the input.** Identify topic, audience, scope, duration target.
2. **Ask targeted alignment questions.** One at a time. Keep terse.
   - What should the learner be able to *do* at the end? (not "know" — action verbs only)
   - How will each objective be assessed?
   - What practice should precede the assessment?
   - What content teaches the practice?
3. **Draft the 4-column O-A-P-P table.**
4. **Run quality checklist:**
   - Every objective starts with an action verb (differentiate, select, justify, prioritize, classify, calculate, design, diagnose, apply, recommend)
   - NO "understand", "know", "be aware of", "appreciate"
   - Every assessment is concretely specifiable (MCQ, scenario, performance task)
   - Every row's assessment-practice-presentation is aligned (no gaps, no "nice to know" padding)
   - Scope fits duration target (rule of thumb: 1 objective per 8–10 min of module time)
5. **Write output** to `modules/<module-slug>/content-map.md`.
6. **git auto-commit** with message `G1: content-map approved for <module-slug>` (this happens AFTER the user reviews and approves; not automatic on write).
7. **Stop for G1 review.** Present the table. Ask user to verify alignment, scope, action verbs. Do NOT proceed to `/build-html` — let the user invoke it next.

## Output format

```markdown
# Module <id> — <title>

**Target learner:** <description>
**Duration target:** ~<n> min
**Assessment strategy:** <summary>

| Objective | Assessment | Practice | Presentation |
|-----------|------------|----------|--------------|
| **<verb>** ... | <assessment type + content> | <practice description or —> | <content summary> |
| ... | ... | ... | ... |

## Notes
- <anything surfaced during alignment work>
```

## Rules

1. One question at a time during alignment dialogue.
2. Action verbs only for objectives.
3. Every row must align end-to-end.
4. Max ~6 objectives for a 30-min module (fewer is fine).
5. Output goes to `modules/<slug>/content-map.md` — not chat.
6. On approval, git auto-commit: `cd ~/Desktop/elearning-workspace && git add modules/<slug>/content-map.md && git commit -m "G1: content-map approved for <slug>"`
7. Stop after writing + committing. Do not auto-trigger `/build-html`.

## Reference

- Quality checklist lives alongside this skill (or in `~/Desktop/elearning-storyboard/content-mapping-best-practices.md` if the user references it).
- Module 2.5 pilot seed: use the worked example from `~/Desktop/elearning-storyboard/SKILL.md` (title, objectives, menu hub with 8 tiles, knowledge check, summary).
````

### Task 4.2: Write build-html/SKILL.md

**Files:**
- Create: `~/Desktop/elearning-workspace/skills-src/build-html/SKILL.md`

- [ ] **Step 1: Write skill**

````markdown
---
name: build-html
description: Use after /content-map — transforms the O-A-P-P table into per-slide markdown files (phase 1) and then merges them with the shared shell into runnable HTML (phase 2). Second stage of the eLearning pipeline.
---

# /build-html

## Overview

Two-phase skill with a review gate between them.

- **Phase 1 (storyboard thinking):** Read `content-map.md` → produce one markdown file per slide in `content/` + a summary table. STOP for G2 review.
- **Phase 2 (build step):** Merge `content/*.md` + copy shell → produce runnable `build/index.html`. STOP for G3 review.

## When to use

- User invokes `/build-html` after `/content-map` has been approved (G1)
- User says "continue" / "build the slides" / "generate the HTML"

## Input

- `modules/<slug>/content-map.md` (from `/content-map`)
- Existing `modules/<slug>/content/` if user is re-running phase 1 after edits

## Phase 1 — Storyboard thinking

1. Read `content-map.md`. For each row, decide:
   - How many slides are needed (usually 1–4 slides per objective)
   - Which layout each slide uses (L01, L03, L09, L12, L13, L14)
2. Produce one markdown file per slide in `modules/<slug>/content/NN-slug.md` with YAML frontmatter matching the `content.json` schema (`shell/content.schema.md`).
3. Also write `modules/<slug>/module.yml` with module-level metadata:
   ```yaml
   id: 2.5-procurement-plan
   title: Developing the procurement plan
   module_label: Module 2.5
   scorm_identifier: com.qianhui.m2-5-procurement-plan
   ```
4. Present a summary table to the user:

   ```
   | Slide # | File | Title | Layout | Type | Notes |
   | ... | ... | ... | ... | ... | ... |
   ```

5. **STOP for G2 review.** User verifies slide count, layouts, order. User can hand-edit any `content/*.md` or describe changes for Claude to apply. Do NOT run phase 2 yet.
6. On user approval (user says "G2 pass" / "continue" / "phase 2"), git auto-commit:
   ```bash
   cd ~/Desktop/elearning-workspace && git add modules/<slug>/content/ modules/<slug>/module.yml && git commit -m "G2: content files approved for <slug>"
   ```

## Phase 2 — Build step

1. Run the merge + copy:
   ```bash
   python3 ~/Desktop/elearning-workspace/scripts/merge_content.py ~/Desktop/elearning-workspace/modules/<slug>
   cp -r ~/Desktop/elearning-workspace/shell/index.html ~/Desktop/elearning-workspace/shell/css ~/Desktop/elearning-workspace/shell/js ~/Desktop/elearning-workspace/shell/schemas ~/Desktop/elearning-workspace/shell/assets ~/Desktop/elearning-workspace/modules/<slug>/build/ 2>/dev/null || true
   ```
   (The `pack_scorm.py` script does all of this + manifest + zip; for a build-only step, run `python3 ~/Desktop/elearning-workspace/scripts/pack_scorm.py <module_dir>` and stop after it writes the zip — or call `copy_shell` + `write_content_json` directly.)

   For phase 2 we want the build/ to be runnable in a browser. Simplest: invoke pack_scorm.py but ignore the zip output; the `build/` directory is populated as a side effect.

2. Start a local server so the user can walk through:
   ```bash
   cd ~/Desktop/elearning-workspace/modules/<slug>/build && python3 -m http.server 8765 &
   ```

3. Tell the user: "Open http://localhost:8765/ in your browser and walk through the module."

4. **STOP for G3 review.** User walks through the full module. Routes feedback via natural language:
   - Content fix ("slide 4 title should be X") → edit `content/*.md`, re-run phase 2.
   - Layout fix ("slide 6 should be L06") → change `layout:` in frontmatter + rewrite body, re-run phase 2. (Note: L06 is not in MVP — push back if requested.)
   - Shell visual fix ("all popup borders too thin") → edit `shell/css/layouts.css`, confirm with user that change affects all future modules, re-run phase 2.
   - Shell behavior fix ("checkmark doesn't appear") → edit `shell/js/app.js`, re-run phase 2.

5. On G3 approval, stop the local server and git auto-commit:
   ```bash
   pkill -f "http.server 8765" || true
   cd ~/Desktop/elearning-workspace && git add modules/<slug>/build/ shell/ && git commit -m "G3: browser walkthrough passed for <slug>"
   ```

## Rules

1. Phase 1 and phase 2 are separate — STOP for G2 in between.
2. One slide per file in `content/`.
3. Use only MVP layouts: L01, L03, L09, L12, L13, L14, popup. If content calls for L02/L04/L05/L06/L07/L08/L10/L11, push back — those are deferred.
4. Slide filenames: `NN-slug.md`, zero-padded, numeric prefix for ordering.
5. Popups for L12 use `layout: popup` and are referenced by `popup_slide_id` from the menu bars.
6. Respect the content.json schema in `shell/content.schema.md`.
7. Route user feedback to the right layer (content vs shell) — don't make the user pick files.
8. On shell-level changes, warn the user that the change affects all future modules.
9. Do not auto-trigger `/scorm-pack` after G3 — let the user invoke it.
````

### Task 4.3: Write scorm-pack/SKILL.md

**Files:**
- Create: `~/Desktop/elearning-workspace/skills-src/scorm-pack/SKILL.md`

- [ ] **Step 1: Write skill**

````markdown
---
name: scorm-pack
description: Use after /build-html — packages a built module into a SCORM 1.2 zip for upload to SCORM Cloud. Third and final stage of the eLearning pipeline.
---

# /scorm-pack

## Overview

Wraps a built module in a SCORM 1.2 manifest + zip. Near-automatic. Produces `modules/<slug>/dist/<slug>.zip`.

## When to use

- User invokes `/scorm-pack` after `/build-html` phase 2 has been approved (G3)

## Input

- A built module folder at `modules/<slug>/` containing:
  - `module.yml`
  - `content/*.md` (approved at G2)
  - `build/` (populated at G3)

## Workflow

1. Run the pack script:
   ```bash
   python3 ~/Desktop/elearning-workspace/scripts/pack_scorm.py ~/Desktop/elearning-workspace/modules/<slug>
   ```

2. Capture the script output (file count, size, next-step instructions).

3. Verify the zip was created and passed validation:
   ```bash
   ls -la ~/Desktop/elearning-workspace/modules/<slug>/dist/
   ```

4. Print a report to the user:

   ```
   SCORM package built: modules/<slug>/dist/<slug>.zip (<size> KB, <n> files)

   Expected SCORM API calls on run:
     LMSInitialize("")                              → "true"
     LMSSetValue("cmi.core.lesson_status", "incomplete") → "true"
     LMSSetValue("cmi.core.score.raw", "<n>")       → "true"
     LMSSetValue("cmi.core.lesson_status", "completed") → "true"
     LMSCommit("")                                  → "true"
     LMSFinish("")                                  → "true"

   Next step: upload to https://cloud.scorm.com → Add Content → Upload the zip
   ```

5. git auto-commit:
   ```bash
   cd ~/Desktop/elearning-workspace && git add modules/<slug>/dist/ && git commit -m "G4: SCORM package built for <slug>"
   ```

6. **STOP for G4 review.** User uploads to SCORM Cloud, launches, verifies API log + registration status. If failure, debug (usually manifest format, missing file, or CMI field format).

## Rules

1. Do not modify `content/` or `shell/` — those should be locked before `/scorm-pack` runs.
2. If the pack script raises a validation error, report it exactly and do not retry until fixed.
3. Do not upload the zip for the user — uploading is a manual G4 step.
4. On G4 failure, check: manifest well-formed? file list matches zip contents? score.raw in 0–100 range?
````

### Task 4.4: Symlink skills into ~/.claude/skills/

**Files:**
- Create: `~/.claude/skills/content-map` (symlink)
- Create: `~/.claude/skills/build-html` (symlink)
- Create: `~/.claude/skills/scorm-pack` (symlink)

- [ ] **Step 1: Create symlinks**

```bash
mkdir -p ~/.claude/skills
ln -sfn ~/Desktop/elearning-workspace/skills-src/content-map ~/.claude/skills/content-map
ln -sfn ~/Desktop/elearning-workspace/skills-src/build-html ~/.claude/skills/build-html
ln -sfn ~/Desktop/elearning-workspace/skills-src/scorm-pack ~/.claude/skills/scorm-pack
```

- [ ] **Step 2: Verify**

```bash
ls -la ~/.claude/skills/ | grep -E "(content-map|build-html|scorm-pack)"
```

Expected: three symlinks pointing back to the workspace.

- [ ] **Step 3: Commit skill sources**

```bash
cd ~/Desktop/elearning-workspace
git add skills-src/
git commit -m "feat(skills): content-map, build-html, scorm-pack"
```

---

## Phase 5 — Pilot Module 2.5 end-to-end

Goal: Run the three skills against the real Module 2.5 seed, hit all four review gates, produce a zip that passes on SCORM Cloud.

### Task 5.1: Create module folder

**Files:**
- Create: `~/Desktop/elearning-workspace/modules/2.5-procurement-plan/`

- [ ] **Step 1: Create skeleton**

```bash
mkdir -p ~/Desktop/elearning-workspace/modules/2.5-procurement-plan/content
```

### Task 5.2: Invoke /content-map (G1)

Seed = the worked example in `~/Desktop/elearning-storyboard/SKILL.md` (storyboard skill): Module 2.5 "Developing the procurement plan", audience = project managers, ~30 min, includes L13 objectives, L12 menu hub with 8 components, L09 knowledge check, L14 summary.

- [ ] **Step 1: Start the content-map dialogue**

Prompt: "/content-map for Module 2.5 Developing the procurement plan. Seed = the worked example in ~/Desktop/elearning-storyboard/SKILL.md. Target: project managers, ~30 min, assessment = MCQ knowledge check."

- [ ] **Step 2: Work through the alignment questions with the user.** Keep it terse. Expect 3–5 objectives.

- [ ] **Step 3: Write the O-A-P-P table to `modules/2.5-procurement-plan/content-map.md`.**

- [ ] **Step 4: Present table for G1 review.** Iterate until user says "G1 pass".

- [ ] **Step 5: git commit**

```bash
cd ~/Desktop/elearning-workspace
git add modules/2.5-procurement-plan/content-map.md
git commit -m "G1: content-map approved for 2.5-procurement-plan"
```

### Task 5.3: Invoke /build-html phase 1 (G2)

- [ ] **Step 1: Prompt** "/build-html phase 1 for 2.5-procurement-plan"

- [ ] **Step 2: Generate `modules/2.5-procurement-plan/module.yml` + `content/*.md` files.** Expected slide count: 10–15 (objectives, intro, concept, menu hub + 8 popups, knowledge check, summary).

- [ ] **Step 3: Present summary table for G2 review.** Iterate on content/layout feedback until user says "G2 pass".

- [ ] **Step 4: git commit**

```bash
cd ~/Desktop/elearning-workspace
git add modules/2.5-procurement-plan/module.yml modules/2.5-procurement-plan/content/
git commit -m "G2: content files approved for 2.5-procurement-plan"
```

### Task 5.4: Invoke /build-html phase 2 (G3)

- [ ] **Step 1: Prompt** "/build-html phase 2" (or "continue")

- [ ] **Step 2: Run the build**

```bash
python3 ~/Desktop/elearning-workspace/scripts/pack_scorm.py ~/Desktop/elearning-workspace/modules/2.5-procurement-plan
```

(The pack script is idempotent — running it here populates `build/` and `dist/` both, but at this gate we only care about `build/`.)

- [ ] **Step 3: Start local server**

```bash
cd ~/Desktop/elearning-workspace/modules/2.5-procurement-plan/build && python3 -m http.server 8766 &
```

- [ ] **Step 4: Ask user to walk through at http://localhost:8766/**

- [ ] **Step 5: Iterate on bugs / visual issues.** Route by layer (content vs shell). Re-run pack_scorm.py after each fix.

- [ ] **Step 6: On G3 pass, stop server + commit**

```bash
pkill -f "http.server 8766" || true
cd ~/Desktop/elearning-workspace
git add modules/2.5-procurement-plan/build/ shell/
git commit -m "G3: browser walkthrough passed for 2.5-procurement-plan"
```

### Task 5.5: Invoke /scorm-pack (builds zip)

- [ ] **Step 1: Prompt** "/scorm-pack 2.5-procurement-plan"

- [ ] **Step 2: Run pack script (also re-runs to get the fresh zip)**

```bash
python3 ~/Desktop/elearning-workspace/scripts/pack_scorm.py ~/Desktop/elearning-workspace/modules/2.5-procurement-plan
```

- [ ] **Step 3: Verify zip exists and passes validation**

```bash
ls -la ~/Desktop/elearning-workspace/modules/2.5-procurement-plan/dist/
unzip -l ~/Desktop/elearning-workspace/modules/2.5-procurement-plan/dist/2.5-procurement-plan.zip | head -20
```

- [ ] **Step 4: Print the SCORM API call report to the user** (see scorm-pack SKILL.md for format).

- [ ] **Step 5: git commit**

```bash
cd ~/Desktop/elearning-workspace
git add modules/2.5-procurement-plan/dist/
git commit -m "G4: SCORM package built for 2.5-procurement-plan"
```

### Task 5.6: 🛑 CHECKPOINT C4 — User uploads real module to SCORM Cloud

- [ ] **Step 1: Present to Qianhui**

> **Your turn (15 min) — the big one:**
> 1. Open https://cloud.scorm.com.
> 2. Add Content → Upload SCORM package.
> 3. Upload `~/Desktop/elearning-workspace/modules/2.5-procurement-plan/dist/2.5-procurement-plan.zip`.
> 4. Import should succeed (we validated manifest at C1 with Hello World, and pack_scorm.py validates each package).
> 5. Click Launch.
> 6. Walk through the full module — objectives, intro, concept, menu hub (click all 8 bars + popups), knowledge check (submit an answer), summary.
> 7. The summary slide should trigger completion; the knowledge check should record a score.
> 8. Finish and exit.
> 9. In SCORM Cloud: go to Registrations → click the registration → check:
>    - **API Log** shows all the expected calls (see below)
>    - **Registration Detail** shows `Status = Completed` and `Score = <your score>`
>
> Expected API calls in the log:
> - `LMSInitialize("")` → `"true"` (once)
> - `LMSSetValue("cmi.core.lesson_status", "incomplete")` → `"true"`
> - `LMSSetValue("cmi.core.score.raw", "<n>")` → `"true"` (after knowledge check)
> - `LMSSetValue("cmi.core.lesson_status", "completed")` → `"true"` (at summary)
> - `LMSCommit("")` → `"true"`
> - `LMSFinish("")` → `"true"` (once)
>
> Tell me "C4 passed" or paste any error / unexpected behavior.

- [ ] **Step 2: If failures,** debug and loop. Most common: score format (must be `"0"`–`"100"` string), missing file in zip, manifest schema path.

- [ ] **Step 3: On pass, final commit**

```bash
cd ~/Desktop/elearning-workspace
git commit --allow-empty -m "MVP: end-to-end passed on SCORM Cloud for 2.5-procurement-plan"
```

---

## Phase 6 — Wrap

### Task 6.1: Write README for the workspace

**Files:**
- Modify: `~/Desktop/elearning-workspace/README.md`

- [ ] **Step 1: Replace stub with usage guide**

```markdown
# eLearning pipeline workspace

Three-skill Claude Code pipeline that produces SCORM 1.2 packages for SCORM Cloud.

## Install

Python deps:
```bash
pip3 install -r requirements.txt
```

Skills are auto-discovered via symlinks in `~/.claude/skills/` pointing to `skills-src/`. To re-link after a fresh clone:
```bash
ln -sfn "$PWD/skills-src/content-map" ~/.claude/skills/content-map
ln -sfn "$PWD/skills-src/build-html" ~/.claude/skills/build-html
ln -sfn "$PWD/skills-src/scorm-pack" ~/.claude/skills/scorm-pack
```

## Make a new module

1. In Claude Code: `/content-map` → dialogue → review table → approve (G1)
2. `/build-html` → phase 1 → review content files → approve (G2)
3. Continue → phase 2 → walk through in browser → approve (G3)
4. `/scorm-pack` → upload the zip to SCORM Cloud → verify (G4)

Each gate auto-commits to git.

## MVP layouts

- L01 text-only
- L03 60/40 media + text
- L09 MCQ (default / selected / submitted + feedback)
- L12 menu hub with popups
- L13 objectives list
- L14 summary (triggers completion)

Adding a new layout post-MVP:
1. Add CSS block in `shell/css/layouts.css`
2. Add render function in `shell/js/app.js` (switch case in `renderByLayout`)
3. Document field shape in `shell/content.schema.md`
4. Update the build-html skill's layout list

## Deferred (post-MVP)

Layouts L02, L04, L05, L06, L07, L08, L10, L11. Responsive design. Accessibility. Multi-module nav chrome. Audio VO playback. xAPI. Light theme.

See `~/Desktop/elearning-storyboard/docs/superpowers/specs/2026-04-10-elearning-pipeline-design.md` for the full design spec.
```

- [ ] **Step 2: Commit**

```bash
cd ~/Desktop/elearning-workspace
git add README.md
git commit -m "docs: workspace README"
```

### Task 6.2: Capture reference screenshots of the 6 MVP layouts

- [ ] **Step 1: Open test-layouts.html**

```bash
open ~/Desktop/elearning-workspace/dev/test-layouts.html
```

- [ ] **Step 2: Ask user to screenshot each section** (L01, L03, L09, L12, L13, L14) and save to `~/Desktop/elearning-workspace/dev/reference-screenshots/`. These become the "golden" visual reference for future modules.

```bash
mkdir -p ~/Desktop/elearning-workspace/dev/reference-screenshots
```

- [ ] **Step 3: Commit whatever screenshots the user provides**

```bash
cd ~/Desktop/elearning-workspace
git add dev/reference-screenshots/
git commit -m "docs: reference screenshots for 6 MVP layouts"
```

### Task 6.3: Final MVP done commit

- [ ] **Step 1: Tag**

```bash
cd ~/Desktop/elearning-workspace
git tag -a mvp-1.0 -m "MVP 1.0 — pipeline pilot on Module 2.5 passed SCORM Cloud"
```

- [ ] **Step 2: Show log to user**

```bash
git log --oneline
```

Expected: clean history with commits named for each gate (G1, G2, G3, G4), chore commits for setup, and the final `mvp-1.0` tag.

---

## Done

MVP is complete when:
- All C1–C4 checkpoints passed
- Module 2.5 shows Completed + Score in SCORM Cloud
- Git log shows the full iteration history
- `mvp-1.0` tag exists

Post-MVP next candidates (from the deferred list in the spec): pick 1–2 layouts to add based on Qianhui's actual next module.
