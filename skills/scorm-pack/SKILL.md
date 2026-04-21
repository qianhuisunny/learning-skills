---
name: scorm-pack
description: Use after /build-html — packages a built module into a SCORM 1.2 zip for upload to SCORM Cloud. Fourth and final skill in the eLearning pipeline.
---

# /scorm-pack

## Overview

Wraps a built module in a SCORM 1.2 manifest + zip. Near-automatic. Produces `modules/<slug>/dist/<slug>.zip`.

## When to use

- User invokes `/scorm-pack` after `/build-html` phase 2 has been approved (G3)

## Input

A built module folder at `modules/<slug>/` containing:
- `module.yml`
- `content/*.md` (approved at G2)
- `build/` (populated and verified at G3)

## Workflow

1. Run the pack script:
   ```bash
   python3 ~/Desktop/elearning-skills/scripts/pack_scorm.py ~/Desktop/elearning-skills/modules/<slug>
   ```

2. Verify:
   ```bash
   ls -la ~/Desktop/elearning-skills/modules/<slug>/dist/
   ```

3. Print report to the user:

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

4. Git auto-commit:
   ```bash
   cd ~/Desktop/elearning-skills && git add modules/<slug>/dist/ && git commit -m "G4: SCORM package built for <slug>"
   ```

5. **STOP for G4 review.** User uploads to SCORM Cloud, launches, verifies API log + registration status.

## Rules

1. Do not modify `content/` or `shell/` — those should be locked before `/scorm-pack` runs.
2. If the pack script raises a validation error, report it exactly. Do not retry until fixed.
3. Do not upload the zip for the user — uploading is a manual G4 step.
4. On G4 failure, check: manifest well-formed? file list matches zip? score.raw in 0–100?
