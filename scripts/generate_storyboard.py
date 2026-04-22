"""Generate a PPT storyboard from a content-map.md file.

Reads the content-map's Presentation column to determine slide sequence,
layouts, and content, then uses storyboard-template.py to produce a .pptx.

Usage:
    python3 generate_storyboard.py <module_dir>

Reads:  <module_dir>/content-map.md
Writes: <module_dir>/storyboard.pptx
"""
from __future__ import annotations
import sys
from pathlib import Path

# Add the repo root so we can import the template
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

import importlib
storyboard_template = importlib.import_module("storyboard-template")
StoryboardBuilder = storyboard_template.StoryboardBuilder


def build_module_2_5(module_dir: Path) -> Path:
    """Build storyboard for Module 2.5 — Developing the procurement plan.

    This is hand-coded from the approved content-map. Future versions will
    parse the content-map.md automatically, but for MVP we wire it directly
    from the approved slide sequence.
    """
    sb = StoryboardBuilder("Module 2.5 — Developing the procurement plan")

    # ── Slide 1: Title ──
    sb.add_title_slide(
        "Module 2.5",
        "Developing the procurement plan",
        "For project managers responsible for procurement decisions"
    )

    # ── Slide 2: L13 Objectives ──
    sb.add_L13(
        "2.5-1", "What you will be able to do",
        objectives=[
            "Differentiate a procurement plan from a project plan by scope and purpose",
            "Identify the 8 components of a procurement plan and their role",
            "Select the appropriate contract type given project constraints",
        ],
        notes=sb._format_notes(
            vo="By the end of this module, you'll be able to do three things. "
               "First, you'll differentiate a procurement plan from a project plan. "
               "Second, you'll identify the eight components every procurement plan needs. "
               "And third, you'll select the right contract type for a given project.",
            visual="Three objectives listed with numbered badges.",
            interaction="No interaction. Click Next to continue."
        )
    )

    # ── Slide 3: L01 Activate prior knowledge ──
    sb.add_L01(
        "2.5-2", "You already use a project plan",
        body="Before we talk about procurement plans, let's anchor to something familiar.",
        bullets=[
            "A project plan covers scope, timeline, resources, and deliverables",
            "It answers: what are we building, and when?",
            "Every PM creates one — it's the backbone of project execution",
        ],
        notes=sb._format_notes(
            vo="You already work with project plans every day. A project plan covers "
               "scope, timeline, resources, and deliverables. It answers the question: "
               "what are we building, and when will it be done?",
            visual="Text slide with three dash bullets on dark background.",
            interaction="No interaction. Click Next to continue."
        )
    )

    # ── Slide 4: L03 Introduce procurement plan concept ──
    sb.add_L03(
        "2.5-3", "What is a procurement plan",
        media_label="Visual: procurement plan as a subset document that feeds into the project plan",
        heading="A different question",
        body="A procurement plan answers: how will we buy, and from whom?",
        bullets=[
            "Defines how purchases will be managed across the project",
            "Covers vendor selection, contract type, and delivery timing",
            "Lives alongside the project plan — not inside it",
        ],
        notes=sb._format_notes(
            vo="A procurement plan answers a different question: not what are we building, "
               "but how will we buy what we need? It defines how purchases will be managed, "
               "what contract types you'll use, and how you'll select vendors.",
            visual="Left: diagram showing procurement plan as a parallel document to the "
                   "project plan, with arrows showing how procurement feeds into project "
                   "timeline. Right: three key bullets.",
            interaction="No interaction. Click Next to continue."
        )
    )

    # ── Slide 5: L01 Contrast ──
    sb.add_L01(
        "2.5-4", "Project plan vs procurement plan",
        body="Two documents, two questions, one project.",
        bullets=[
            "Project plan asks: WHAT are we building and WHEN?",
            "Procurement plan asks: HOW do we buy and FROM WHOM?",
            "Project plan owns scope and schedule — procurement plan owns commercial strategy",
        ],
        notes=sb._format_notes(
            vo="Here's the key contrast. Your project plan asks what and when. "
               "Your procurement plan asks how and from whom. The project plan "
               "owns scope and schedule. The procurement plan owns commercial strategy — "
               "vendor selection, contract structure, and risk allocation.",
            visual="Three bullet points with contrasting pairs. Each bullet "
                   "highlights the scope boundary between the two documents.",
            interaction="No interaction. Click Next to continue."
        )
    )

    # ── Slide 6: L01 Organizing framework ──
    sb.add_L01(
        "2.5-5", "Three phases of a procurement plan",
        body="Before we explore all eight components, here's how they organize.",
        bullets=[
            "Define — what to buy (objectives, scope, method)",
            "Execute — how to buy (contract type, evaluation, risk)",
            "Govern — who decides (schedule, governance, approvals)",
        ],
        notes=sb._format_notes(
            vo="A procurement plan has eight components, but don't worry — they "
               "group into three phases. Define: what are we buying. Execute: how "
               "are we buying it. Govern: who makes the decisions. This framework "
               "will help you keep track as we explore each component.",
            visual="Three dash bullets, each representing a phase with 2-3 "
                   "component names in parentheses.",
            interaction="No interaction. Click Next to continue."
        )
    )

    # ── Slide 7: L12 Menu hub ──
    tiles = [
        ("📋", "Objectives and criteria"),
        ("📦", "Scope and packaging"),
        ("🔍", "Procurement method"),
        ("📝", "Contract type"),
        ("⚖️", "Evaluation approach"),
        ("⚠️", "Risk and contingency"),
        ("📅", "Schedule and milestones"),
        ("🏛️", "Governance and approvals"),
    ]
    sb.add_anchor(
        "2.5-6", "Explore each component",
        tiles=tiles,
        subtitle="Click each component to learn more. Visit all eight to continue.",
        notes=sb._format_notes(
            vo="Now let's explore each of the eight components. Click on any "
               "component to open it. You'll need to visit all eight before "
               "you can move on.",
            visual="Eight horizontal bars stacked vertically, each with a "
                   "number badge and component name.",
            interaction="L12 menu hub. Learner clicks each bar to open a popup. "
                        "Next button disabled until all 8 are visited. "
                        "Visited bars show a green checkmark."
        )
    )

    # ── Popups for each component ──
    popup_data = [
        ("2.5-6-01", 1, "Objectives and criteria",
         "Tie every criterion back to a sponsor-owned success measure.",
         ["Clear measurable targets aligned to sponsor expectations",
          "Evaluation criteria weighted by strategic priority",
          "Acceptance thresholds agreed with the steering group"]),
        ("2.5-6-02", 2, "Scope and packaging",
         "Packaging is your first risk allocation decision — get it right before vendors are involved.",
         ["Decide single-package vs multi-package procurement",
          "Balance integration risk against vendor leverage",
          "Map each package to a delivery milestone"]),
        ("2.5-6-03", 3, "Procurement method",
         "Match the method to the market — don't default to open tender for every package.",
         ["Open tender: maximum competition, higher admin effort",
          "Restricted tender: pre-qualified shortlist, faster",
          "Direct appointment: speed, but must justify sole-source"]),
        ("2.5-6-04", 4, "Contract type",
         "Contract type is the single biggest risk-allocation lever in the plan.",
         ["Fixed-price: risk sits with the vendor, less flexibility for changes",
          "Time-and-materials: flexibility for the buyer, risk on cost overruns",
          "Hybrid (capped T&M): shared risk, caps protect the buyer"]),
        ("2.5-6-05", 5, "Evaluation approach",
         "Weight criteria before you see proposals — not after.",
         ["Technical merit: does the solution meet requirements?",
          "Price competitiveness: is the cost reasonable for the market?",
          "Risk profile: what could go wrong with this vendor?",
          "Past performance: has this vendor delivered similar work?"]),
        ("2.5-6-06", 6, "Risk and contingency",
         "Risk allocation happens in the contract — if it's not written down, you own it.",
         ["Identify procurement-specific risks (vendor insolvency, supply chain disruption)",
          "Assign risk to the party best positioned to manage it",
          "Build contingency into timeline and budget — not just cost"]),
        ("2.5-6-07", 7, "Schedule and milestones",
         "Procurement delay is the #1 cause of project schedule slip in complex programs.",
         ["Map procurement timeline to project critical path",
          "Build in lead times for tender, evaluation, and mobilization",
          "Identify dependencies between packages"]),
        ("2.5-6-08", 8, "Governance and approvals",
         "Clear governance prevents the 'who approved this?' conversation six months in.",
         ["Define approval authority levels (who signs what value)",
          "Establish the evaluation panel composition",
          "Set escalation path for disputes and variations"]),
    ]

    for slide_num, comp_num, comp_title, key_msg, bullets in popup_data:
        sb.add_popup_text(
            slide_num,
            anchor_title="Explore each component",
            comp_num=comp_num,
            comp_title=comp_title,
            body=key_msg,
            bullets=bullets,
            notes=sb._format_notes(
                vo=f"Let's look at {comp_title.lower()}. " +
                   " ".join(bullets) + f" Remember: {key_msg.lower()}",
                visual=f"Pop-up panel over the menu hub. Component {comp_num}: "
                       f"{comp_title}. Key message at top, bullets below.",
                interaction=f"Pop-up overlay on anchor slide 2.5-6. "
                            f"X button closes and returns to anchor with checkmark on bar {comp_num}."
            )
        )

    # Anchor visited state
    sb.add_anchor_visited(
        "2.5-6-v", "Explore each component",
        tiles=tiles,
        visited=set(range(8)),
        notes=sb._format_notes(
            vo="",
            visual="All 8 bars show green checkmarks. Continue button active.",
            interaction="All tiles visited. Next button now enabled."
        )
    )

    # ── Slide 8: L09 MCQ default ──
    stem = ("You're managing a construction project with a well-defined scope, "
            "a fixed deadline, and an experienced vendor pool. "
            "Which contract type best fits this situation?")
    options = [
        "Time-and-materials — maximum flexibility for scope changes",
        "Fixed-price — risk transferred to vendor, scope is locked",
        "Capped T&M — shared risk with a cost ceiling",
        "Cost-plus — vendor reimbursed for all costs plus a fee",
    ]
    sb.add_L09_default(
        "2.5-7a", "Knowledge check",
        stem=stem,
        options=options,
        notes=sb._format_notes(
            vo="Time to check your understanding. Read the scenario and "
               "select the contract type that best fits.",
            visual="MCQ with 4 options. Submit button at bottom.",
            interaction="L09 MCQ. Learner selects one option, then clicks Submit. "
                        "Next is disabled until submitted."
        )
    )

    # ── Slide 9: L09 MCQ feedback ──
    sb.add_L09_feedback(
        "2.5-7b", "Knowledge check",
        stem=stem,
        options=options,
        correct_idx=1,
        feedback_correct=(
            "Fixed-price is the right choice here. The scope is well-defined "
            "and the deadline is fixed — that means scope changes are unlikely, "
            "so transferring delivery risk to the vendor makes sense. "
            "The experienced vendor pool means vendors can price accurately."
        ),
        feedback_incorrect=(
            "With a well-defined scope and fixed deadline, fixed-price is "
            "the strongest fit. T&M gives flexibility you don't need here, "
            "and cost-plus removes the vendor's incentive to control costs. "
            "Remember: match the contract type to the project's risk profile."
        ),
        notes=sb._format_feedback_notes(
            vo="Let's see how you did.",
            correct="Fixed-price is the right choice. Well-defined scope plus "
                    "fixed deadline means scope changes are unlikely.",
            incorrect="Fixed-price was the better fit here. T&M gives flexibility "
                      "you don't need, and cost-plus removes cost control incentive.",
            dev="Left 2/3 shows the question with the learner's selection marked. "
                "Right 1/3 shows feedback panel (green for correct, red for incorrect). "
                "Score recorded via cmi.core.score.raw."
        )
    )

    # ── Slide 10: L14 Summary ──
    sb.add_L14(
        "2.5-8", "Key takeaways",
        takeaways=[
            "A procurement plan answers 'how will we buy?' — distinct from the project plan's 'what and when?'",
            "Eight components group into three phases: Define, Execute, Govern",
            "Contract type is the biggest risk-allocation lever — match it to scope certainty and timeline pressure",
        ],
        cta="Finish module",
        notes=sb._format_notes(
            vo="Let's recap. A procurement plan answers how will we buy — "
               "that's separate from your project plan. The eight components "
               "fall into three phases: define, execute, and govern. And "
               "contract type is your single biggest lever for allocating risk.",
            visual="Three takeaway cards with yellow left border. "
                   "Finish button at bottom.",
            interaction="L14 summary. On entry, triggers cmi.core.lesson_status = 'completed'. "
                        "Finish button calls LMSFinish."
        )
    )

    out = module_dir / "storyboard.pptx"
    sb.save(str(out))
    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generate_storyboard.py <module_dir>", file=sys.stderr)
        sys.exit(2)
    module_dir = Path(sys.argv[1]).expanduser().resolve()
    out = build_module_2_5(module_dir)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
