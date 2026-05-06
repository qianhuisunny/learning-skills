---
name: scorm-pack
description: Use after /build-html approval — packages an approved HTML module into a SCORM 1.2 zip for upload to SCORM Cloud. Fourth and final skill in the eLearning pipeline.
---

# /scorm-pack

## Overview

Wraps an already approved HTML build in a SCORM 1.2 manifest + zip. Near-automatic. Produces `modules/<slug>/dist/<slug>.zip`.

This skill owns packaging only. It does not rewrite content files, rebuild the
HTML shell, redesign screens, or change learner-facing text.

## When to use

- User invokes `/scorm-pack` after `/build-html` has been approved (G3)

## Input

A built module folder at `modules/<slug>/` containing:
- `module.yml`
- `storyboard/` (approved at G2)
- `content/*.md` (approved at G3 as part of the HTML build)
- `build/` (populated and verified at G3)

## Workflow

1. Confirm `modules/<slug>/build/index.html` and
   `modules/<slug>/build/content.json` exist.

2. Run the packaging script:
   ```bash
   python3 ~/Desktop/elearning-skills/scripts/package_scorm.py ~/Desktop/elearning-skills/modules/<slug>
   ```

3. Verify:
   ```bash
   ls -la ~/Desktop/elearning-skills/modules/<slug>/dist/
   ```

4. Print report to the user:

   ```
   SCORM package built: modules/<slug>/dist/<slug>.zip (<size> KB, <n> files)

   Expected SCORM API calls on run:
     LMSInitialize("")                                    → "true"
     LMSSetValue("cmi.core.lesson_status", "incomplete")  → "true"
     LMSSetValue("cmi.core.score.raw", "<n>")             → "true"
     LMSSetValue("cmi.core.lesson_status", "completed")   → "true"
     LMSCommit("")                                        → "true"
     LMSFinish("")                                        → "true"

   Next step: upload to https://cloud.scorm.com → Add Content → Upload
   ```

5. Git auto-commit:
   ```bash
   cd ~/Desktop/elearning-skills && git add modules/<slug>/build/imsmanifest.xml modules/<slug>/dist/ && git commit -m "G4: SCORM package built for <slug>"
   ```

6. **STOP for G4 review.** User uploads to SCORM Cloud, launches, verifies API log + registration status.

## Rules

1. Do not modify `content/`, `storyboard/`, or `shell/` — those should be locked before `/scorm-pack` runs.
2. If the packaging script raises a validation error, report it exactly. Do not retry until fixed.
3. Do not upload the zip for the user — uploading is a manual G4 step.
4. On G4 failure, check: manifest well-formed? file list matches zip? score.raw in 0–100?
