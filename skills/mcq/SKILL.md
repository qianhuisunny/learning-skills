---
name: mcq
description: Use when writing, reviewing, or revising multiple-choice questions for eLearning assessments, knowledge checks, scenario checks, or L09 storyboard screens. Generates Bloom-aligned MCQs with parallel answer construction, plausible distractors, feedback, and L09 layout/state notes.
---

# /mcq

## Overview

Creates and reviews multiple-choice questions for eLearning. This skill owns
item quality: objective alignment, Bloom level, answer construction,
distractors, feedback, and L09 assessment-state notes.

It does not decide the full lesson sequence. `/content-map` owns objective and
assessment strategy; `/storyboard` owns screen flow.

## When to use

- User invokes `/mcq`
- User asks for multiple-choice questions, knowledge checks, quiz items, or
  assessment questions
- `/storyboard` needs L09 MCQ screens for a lesson or module checkpoint
- Existing MCQs need quality review or rewrite

## Inputs

Required:
- Learning objective
- Target learner
- Source content or approved content map row

Optional:
- Bloom level, if already specified
- Scenario/case facts to reuse
- Number of questions requested
- Constraints from the authoring tool

## Default Output

Unless the user requests otherwise, create **two MCQs per lesson or module
assessment checkpoint**.

Each MCQ must include:
- Objective alignment
- Bloom level
- Stem
- Four answer options: A, B, C, D
- Correct answer
- Feedback for correct response
- Feedback explaining why each distractor is wrong
- L09 storyboard notes that reference the required states in
  `docs/reference/layout-contract.md`

## MCQ Design Workflow

1. **Identify the target behavior.** Restate what the objective asks the learner
   to do on the job.
2. **Infer or confirm Bloom level.** Use the objective verb and task:
   - Remember: recall a fact, term, or label
   - Understand: explain, summarize, distinguish
   - Apply: choose the right action in a familiar situation
   - Analyze: diagnose, compare evidence, identify cause or pattern
   - Evaluate: judge the best option against criteria
   - Create: usually not suitable for MCQ; use a performance task or scenario
3. **Choose question type.** Use scenario-based MCQs for Apply, Analyze, and
   Evaluate objectives when realistic context is available. Use direct MCQs only
   for focused concept checks.
4. **Write the stem.** Make the task clear before the options. Avoid trick
   wording, double negatives, and irrelevant detail.
5. **Write four parallel options.** All options should have the same grammar,
   comparable length, and the same level of specificity.
6. **Write plausible distractors.** Distractors should represent common errors,
   misconceptions, incomplete reasoning, or tempting but unsafe shortcuts.
7. **Write feedback.** Explain why the correct answer works and why each
   distractor fails. Feedback should teach reasoning, not just mark correctness.
8. **Run the quality check.** Rewrite until the item passes all checks below.

## Item Quality Rules

1. Use four options: A, B, C, D.
2. Keep options parallel in grammar and construction.
3. Keep option lengths similar enough that length does not signal the answer.
4. Make exactly one option clearly best.
5. Avoid "all of the above", "none of the above", joke answers, absolutes, and
   clues caused by repeated words from the stem.
6. Avoid one obviously detailed answer among three vague answers.
7. Avoid testing reading tricks instead of the objective.
8. Align the cognitive demand to the Bloom level. Do not use recall questions
   for objectives that require application, analysis, or judgement.
9. Use scenario-based stems when the learner needs to make a job-like decision.
10. Use source-grounded content. If an item depends on inferred facts, add an SME
    validation note and questions to validate the assumption.

## L09 Layout Boundary

Use canonical layout `L09` from `docs/reference/layout-contract.md`. This skill
does not redefine the L09 layout. It supplies the item text, answer key,
distractor rationale, feedback text, and any item-specific notes needed to
populate the L09 states.

## Output Format

```markdown
## MCQ <n>

**Objective alignment:** <objective>
**Bloom level:** <level>
**Question type:** Direct / Scenario-based

**Stem:**
<question>

**Options:**
A. <option>
B. <option>
C. <option>
D. <option>

**Correct answer:** <letter>

**Feedback:**
- Correct: <why the answer works>
- A: <why this option is right/wrong>
- B: <why this option is right/wrong>
- C: <why this option is right/wrong>
- D: <why this option is right/wrong>

**L09 storyboard notes:**
- State notes: <item-specific behavior beyond the standard L09 contract>
- Retry/remediation: <state or not applicable>

**SME/source note:** <only if needed>
```

## Review Checklist

- [ ] Two MCQs are provided unless the user or content map requests a different
      number.
- [ ] Each MCQ maps to a specific objective and Bloom level.
- [ ] Scenario-based questions are used when the objective requires application,
      analysis, or judgement.
- [ ] A/B/C/D options are parallel and similar in length.
- [ ] Distractors are plausible and diagnose meaningful misconceptions.
- [ ] Feedback explains reasoning for correct and incorrect options.
- [ ] L09 states are specified for storyboard/build use.
