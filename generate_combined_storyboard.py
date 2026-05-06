#!/usr/bin/env python3
"""Generate combined storyboard — course scaffold + eLearning 1 + eLearning 2."""

import importlib.util
spec = importlib.util.spec_from_file_location(
    "storyboard_template",
    "/Users/qianhuisun/Desktop/elearning-skills/storyboard-template.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
StoryboardBuilder = mod.StoryboardBuilder

sb = StoryboardBuilder(
    module_name="Procurement advisory eLearning programme",
    date_str="4 May 2026")

# ═══════════════════════════════════════════════════════════════
# COURSE SCAFFOLDING
# ═══════════════════════════════════════════════════════════════

sb.add_title_slide(
    "Course",
    "Tendering to close",
    "A defensible pathway from procurement planning to preferred proponent, award, and contract close")

sb.add_L01("C-01", "How to complete this course",
    body="This course is complete when the learner has reviewed the core content, opened the required interactions, completed the practice moments, and reached the programme summary.",
    bullets=[
        "Visit every required button, tab, hotspot, or menu item before continuing",
        "Complete each knowledge check or scenario before moving to the next lesson",
        "Use the simulations to practise judgement, not just recall process labels",
        "Completion is triggered on the final programme summary screen",
    ],
    notes=sb._format_notes(
        vo="Before you begin, here is how completion works. Review the core content, open the required interactions, complete the practice moments, and finish at the programme summary.",
        visual="Course rules screen with four concise completion rules and a progress/completion icon treatment.",
        interaction="Course scaffolding screen. Rise build note: use a simple continue block after the learner reviews the rules. SCORM completion should remain tied to the final programme summary, not this screen."))

sb.add_L05("C-02", "Course contents", [
    ("MODULE 1", "Tender process and bidder evaluation",
     "Tender documents, the five-step tendering pathway, clarifications, evaluation criteria, consensus scoring, due diligence, and award documentation."),
    ("MODULE 2", "Exclusive contract negotiation",
     "Preferred proponent transition, commercial close, financial close, negotiation principles, and contract preparation inputs."),
    ("PRACTICE", "Scenario simulations",
     "Senior-audience decisions about bidder ambiguity, evidence gaps, timeline realism, financial deterioration, and defensible documentation."),
], notes=sb._format_notes(
    vo="The course has two modules and a set of practice moments. First, you will work through tendering and evaluation. Then you will move into exclusive negotiation and contract preparation.",
    visual="Three cards: Module 1, Module 2, and Practice. Each card has a short, scan-friendly description.",
    interaction="Table-of-contents screen. In Rise, implement as buttons/tabs if navigation is allowed; otherwise keep as a linear overview block."))

sb.add_L01("C-03", "Build notes for GD and SMR",
    body="These notes are not learner-facing. They define the build assumptions that keep the course aligned with the gold-style treatment.",
    bullets=[
        "Use Rise-friendly components by default: buttons, tabs, hotspots, accordions, and scenario blocks",
        "Keep process diagrams simple enough to rebuild in Rise; avoid bespoke pop-up overlays unless the production tool supports them",
        "Include hidden or reviewer-only interaction-diagram slides for branching simulations",
        "SMR review focus: procurement terminology, RFQ/PQQ vs RFP/ITT distinction, evaluation governance, standstill/debrief wording, and regional variants",
    ],
    notes=sb._format_notes(
        vo="",
        visual="Reviewer-only slide with a clear 'not learner-facing' treatment.",
        interaction="GD / SMR NOTE: Hide or remove from learner package. Use this slide to guide Rise block selection, branching simulation wiring, and SME review."))


# ═══════════════════════════════════════════════════════════════
# eLEARNING 1 — TENDER PROCESS AND BIDDER EVALUATION
# ═══════════════════════════════════════════════════════════════

# ── Title slide ──
sb.add_title_slide(
    "eLearning 1",
    "Tender process and bidder evaluation",
    "Understanding the end-to-end tendering lifecycle and how to evaluate bidders fairly")

# ── 1.1-1: Learning objectives ──
sb.add_L13("1.1-1", "Learning objectives", [
    "Explain the tender process and the purpose of tender documents",
    "Identify the five-step tendering pathway and where queries and clarifications sit",
    "Recognise regional variations in tender processes (MENA vs AUS)",
], notes=sb._format_notes(
    vo="Welcome to the first lesson. By the end of this section, you will be able to explain the purpose of tender documents, walk through a five-step tendering pathway, and recognise where queries, clarifications, and regional variations fit.",
    visual="Three objective bars with blue left-accent and numbered 01–03.",
    interaction="Static slide. No interaction. Continue button advances to next slide."))

# ── 1.1-2: Purpose of tender documents ──
sb.add_L04("1.1-2", "Purpose of tender documents",
    heading="Why tender documents matter",
    body="Tender documents are the foundation of a fair and transparent procurement process. They set the rules, define expectations, and protect all parties involved.",
    media_label="{{INFOGRAPHIC: Key purposes — Ensures transparency, Legal compliance, Clear evaluation criteria, Level playing field}}",
    bullets=[
        "Establish clear requirements so all bidders compete on equal terms",
        "Ensure compliance with legal and regulatory frameworks",
        "Provide a structured basis for evaluation and decision-making",
    ],
    notes=sb._format_notes(
        vo="Before we look at the stages, let's understand why tender documents matter in the first place. These documents are not just paperwork — they are the foundation of a fair process. They ensure transparency, keep the process legally compliant, and give evaluators a clear basis for their decisions.",
        visual="Left column: heading, body text, and three blue-dash bullets. Right column: infographic placeholder showing four key purposes as connected icons.",
        interaction="Static content slide. No interaction. Continue button."))

# ── 1.1-3: Five-step tendering pathway + clarifications (Anchor) ──
tender_stages = [
    ("📋", "Plan and prepare"),
    ("📣", "Market engagement"),
    ("🧾", "Prequalification RFQ/PQQ"),
    ("📨", "RFP/ITT"),
    ("🏆", "Evaluation to award"),
    ("?", "Queries and clarifications"),
]
sb.add_anchor("1.1-3", "The tendering pathway", tender_stages,
    subtitle="Explore the five-step pathway, then review how queries and clarifications run alongside it.",
    notes=sb._format_notes(
        vo="The tendering process is better understood as a pathway, not a generic six-stage list. Click through the five core steps, then review queries and clarifications as a control that runs through the bidder-facing stages.",
        visual="Six horizontal bars stacked vertically. Bars 01-05 are pathway steps; bar 06 is visually marked as a supporting control, not a stage.",
        interaction="Rise-friendly build: use buttons or tabs with one content block per item. Learner must open all six items before Continue activates."))

# ── 1.1-3-01 to 1.1-3-06: Pop-ups for pathway steps and clarifications ──
sb.add_popup_text_media("1.1-3-01", "The tendering pathway", 1, "Plan and prepare",
    body="The procuring entity defines the procurement strategy, requirements, governance route, tender documents, and evaluation approach before approaching the market.",
    bullets=[
        "Confirm business need, procurement route, timeline, and approvals",
        "Prepare the tender pack: scope, specifications, contract terms, response schedules, and evaluation plan",
        "Lock evaluation criteria, weighting, probity requirements, and governance roles before bidder responses are received",
        "Output examples: procurement plan, evaluation manual, draft RFP/ITT pack",
    ],
    media_label="{{MEDIA: Procurement plan + evaluation manual excerpts}}",
    notes=sb._format_notes(
        vo="The first step is plan and prepare. This is where the procurement route, tender pack, evaluation approach, and governance requirements are set. Defensibility starts here, because the evaluation rules need to be locked before bidder responses arrive.",
        visual="Dark pop-up panel with blue border. Left: body text and four dash bullets. Right: procurement plan and evaluation manual placeholder.",
        interaction="Pop-up overlay on anchor slide 1.1-3. X close returns to anchor. Tile 01 gets checkmark on close."))

sb.add_popup_text_media("1.1-3-02", "The tendering pathway", 2, "Market engagement",
    body="Market engagement tests market appetite, capability, and constraints before the formal request documents are issued.",
    bullets=[
        "Use EOI/ROI, market sounding, industry briefings, or supplier days where permitted",
        "Gather market feedback on scope, risk allocation, packaging, timing, and affordability",
        "Maintain equal access to information and avoid giving any future bidder an unfair advantage",
        "Output examples: market engagement report, industry briefing pack, Q&A log",
    ],
    media_label="{{MEDIA: Market sounding briefing / EOI notice}}",
    notes=sb._format_notes(
        vo="Market engagement happens before the formal tender response. It gives the buyer a view of market capacity and constraints, but it has to be handled carefully so all potential bidders remain on an equal footing.",
        visual="Dark pop-up panel. Left: body text and four dash bullets. Right: market sounding or EOI notice placeholder.",
        interaction="Pop-up overlay on anchor slide 1.1-3. X close returns to anchor. Tile 02 gets checkmark on close."))

sb.add_popup_text_media("1.1-3-03", "The tendering pathway", 3, "Prequalification RFQ/PQQ",
    body="The RFQ or PQQ stage screens capability and compliance before inviting shortlisted bidders to prepare full proposals.",
    bullets=[
        "Assess eligibility, experience, financial capacity, conflicts, mandatory documents, and minimum technical capability",
        "Use pass/fail and scored criteria to form a defensible shortlist",
        "Document the shortlist rationale and notify participants according to procurement rules",
        "Output examples: RFQ/PQQ document, prequalification matrix, shortlist recommendation",
    ],
    media_label="{{MEDIA: RFQ/PQQ scoring matrix and shortlist report}}",
    notes=sb._format_notes(
        vo="Prequalification separates basic capability from detailed proposal quality. The RFQ or PQQ stage checks whether bidders meet the minimum requirements and creates a shortlist for the RFP or ITT.",
        visual="Dark pop-up panel. Left: body text and four dash bullets. Right: RFQ/PQQ scoring matrix placeholder.",
        interaction="Pop-up overlay on anchor slide 1.1-3. X close returns to anchor. Tile 03 gets checkmark on close."))

sb.add_popup_text_media("1.1-3-04", "The tendering pathway", 4, "RFP/ITT",
    body="The RFP or ITT asks shortlisted bidders to submit detailed technical, commercial, and financial proposals against the defined requirements.",
    bullets=[
        "Issue detailed requirements, instructions to bidders, draft contract, pricing schedules, and response templates",
        "Run controlled bidder communications through the formal question process",
        "Receive sealed proposals by the deadline through the approved submission route",
        "Output examples: RFP/ITT pack, addenda, bid submission register",
    ],
    media_label="{{MEDIA: RFP/ITT pack and pricing schedule placeholder}}",
    notes=sb._format_notes(
        vo="The RFP or ITT is where shortlisted bidders prepare their full response. This stage needs strict control over communications, addenda, submission deadlines, and document versions.",
        visual="Dark pop-up panel. Left: body text and four dash bullets. Right: RFP/ITT pack and pricing schedule placeholder.",
        interaction="Pop-up overlay on anchor slide 1.1-3. X close returns to anchor. Tile 04 gets checkmark."))

sb.add_popup_text_media("1.1-3-05", "The tendering pathway", 5, "Evaluation to preferred proponent and award",
    body="Submitted proposals are evaluated against the approved method, moderated, documented, and taken through governance before award.",
    bullets=[
        "Evaluate technical, financial, commercial, and compliance responses against the locked criteria",
        "Use moderation or consensus to agree final scores and record the rationale",
        "Recommend a preferred proponent, complete approvals, observe standstill where required, and prepare debriefs",
        "Output examples: evaluation report, preferred proponent recommendation, standstill/debrief letters, award notice",
    ],
    media_label="{{MEDIA: Evaluation report and preferred proponent recommendation}}",
    notes=sb._format_notes(
        vo="The final pathway step is evaluation through to preferred proponent and award. This is where scoring, moderation, due diligence, governance approvals, standstill or debrief requirements, and the award decision come together.",
        visual="Dark pop-up panel. Left: body text and four dash bullets. Right: evaluation report and award documentation placeholder.",
        interaction="Pop-up overlay on anchor slide 1.1-3. X close returns to anchor. Tile 05 gets checkmark."))

sb.add_popup_text_media("1.1-3-06", "The tendering pathway", 6, "Queries and clarifications",
    body="Queries and clarifications are a control layer across the bidder-facing stages, not a separate tender stage.",
    bullets=[
        "Maintain a question log with owner, response, issue date, and affected document references",
        "Share material clarifications with all relevant bidders through formal addenda",
        "Use presentations or clarification meetings only to clarify the submitted offer, not to permit uncontrolled re-bidding",
        "Output examples: bidder Q&A log, addenda, clarification minutes, version-control register",
    ],
    media_label="{{MEDIA: Bidder Q&A log and addendum register}}",
    notes=sb._format_notes(
        vo="Queries and clarifications protect fairness. They give bidders a route to ask questions, but the process must be controlled, documented, and shared appropriately so one bidder does not receive an unfair advantage.",
        visual="Dark pop-up panel. Left: body text and four dash bullets. Right: Q&A log and addendum register placeholder. Header should identify this as a supporting control, not step six.",
        interaction="Pop-up overlay on anchor slide 1.1-3. X close returns to anchor. Tile 06 gets checkmark."))

sb.add_anchor_visited("1.1-3-visited", "The tendering pathway", tender_stages,
    subtitle="All items explored. Click Continue to proceed.",
    notes=sb._format_notes(
        vo="You have now explored the five-step pathway and the queries and clarifications control. Let's look at how the pathway can vary across different regions.",
        visual="Same six horizontal bars as the anchor, now all showing green checkmarks on the right.",
        interaction="All tiles visited. Continue button now active. Advances to next slide."))

# ── 1.1-4: Regional variations — MENA vs AUS ──
sb.add_L06("1.1-4", "Regional variations",
    col_a_header="MENA",
    col_a_items=[
        "Formal Expression of Interest (EOI) and RFQ/PQQ gateways are common",
        "Government procurement portals vary by country",
        "Pre-qualification requirements may be more prescriptive",
        "Compliance documentation expectations tend to be extensive",
    ],
    col_b_header="AUS",
    col_b_items=[
        "Register of Interest (ROI) approach used frequently",
        "Centralised procurement portals (e.g., AusTender)",
        "Value-for-money emphasis in evaluation criteria",
        "Indigenous procurement and local content policies may apply",
    ],
    notes=sb._format_notes(
        vo="While the pathway logic applies broadly, the details vary by region. In the MENA region, you may see formal EOI stages and more prescriptive prequalification requirements. In Australia, procurement often uses ROI approaches, central portals, and a strong value-for-money emphasis.",
        visual="Two-column comparison layout. Left column header: MENA. Right column header: AUS. Four dash-bullet items per column.",
        interaction="Rise-friendly build: use tabs for MENA and AUS, or a two-column comparison block if tabs are unavailable."))

# ── 1.1-4b: Practice — Match activities to pathway steps (L11) ──
sb.add_L11_default("1.1-4b", "Practice: Match activities to the pathway",
    instruction="Drag each activity to the correct tender pathway step or supporting control.",
    items=[
        "Confirm procurement strategy and evaluation plan",
        "Hold market sounding without advantaging any bidder",
        "Screen capability against pass/fail criteria",
        "Issue detailed requirements, pricing forms, and draft contract",
        "Run consensus evaluation and recommend the preferred proponent",
        "Publish written addendum answering bidder questions",
    ],
    targets=[
        "Plan and prepare",
        "Market engagement",
        "Prequalification RFQ/PQQ",
        "RFP/ITT",
        "Evaluation to award",
        "Queries and clarifications",
    ],
    notes=sb._format_notes(
        vo="Let's practise. Drag each activity to the right pathway step, or to the queries and clarifications control if it is not itself a stage.",
        visual="Left panel: six draggable activity cards. Right panel: six labelled drop targets. Instruction bar at top.",
        interaction="L11 drag-and-match default state. Learner drags items to targets. Submit button validates. Correct matches lock in green; incorrect show red with retry option.\n\nCORRECT MAPPING:\n• 'Confirm procurement strategy and evaluation plan' → Plan and prepare\n• 'Hold market sounding without advantaging any bidder' → Market engagement\n• 'Screen capability against pass/fail criteria' → Prequalification RFQ/PQQ\n• 'Issue detailed requirements, pricing forms, and draft contract' → RFP/ITT\n• 'Run consensus evaluation and recommend the preferred proponent' → Evaluation to award\n• 'Publish written addendum answering bidder questions' → Queries and clarifications"))

# ── 1.1-5: Lesson 1.1 summary ──
sb.add_L14("1.1-5", "Lesson 1.1 summary", [
    "Tender documents ensure transparency, compliance, and fair evaluation",
    "The tendering pathway is: plan and prepare → market engagement → RFQ/PQQ → RFP/ITT → evaluation, preferred proponent, and award",
    "Queries and clarifications are a documented control across bidder-facing stages, not a standalone tender stage",
    "Regional differences (MENA vs AUS) affect EOI/ROI approaches, prequalification, portals, and compliance expectations",
], notes=sb._format_notes(
    vo="Let's recap lesson 1.1. Tender documents are the backbone of a fair process. The pathway moves from planning and market engagement through RFQ or PQQ, RFP or ITT, evaluation, preferred proponent selection, and award. Queries and clarifications run alongside the bidder-facing stages as a documented fairness control.",
    visual="Four summary bars with yellow left-accent. Continue button at bottom-right.",
    interaction="Static summary slide. Continue button advances to Lesson 1.2."))


# ═══════════════════════════════════════════════════════════════
# LESSON 1.2 — Develop bidder evaluation criteria
# ═══════════════════════════════════════════════════════════════

sb.add_L13("1.2-1", "Learning objectives", [
    "Develop bidder evaluation criteria for technical and financial streams",
    "Explain how moderation and consensus scoring make evaluation decisions defensible",
    "Identify the seven steps from criteria through documented outcome and award",
], notes=sb._format_notes(
    vo="In this second lesson, we shift focus to evaluation. You will learn how criteria are developed, how moderation and consensus scoring work, and how the process moves from pre-qualification through documented outcome and award.",
    visual="Three objective bars with blue left-accent, numbered 01–03.",
    interaction="Static slide. Continue button."))

sb.add_L02("1.2-2", "The real cost of getting evaluation wrong",
    hero_label="{{MEDIA: Split-screen — Left: price tag icon | Right: checklist icon. Caption: 'Price vs. compliance — which matters more?'}}",
    body="Two bidders submit proposals. One offers the lowest price, the other meets every compliance requirement but costs slightly more. Which one wins? The answer is not as simple as you think. This is why structured evaluation criteria and compliance checks are critical in tendering. A single missing compliance document can disqualify a bid, even if the price is attractive.",
    cta="Let's explore →",
    notes=sb._format_notes(
        vo="Imagine this: two bidders submit proposals. One has the lowest price. The other meets every compliance requirement but costs a little more. Which one wins? The answer might surprise you. A single missing compliance document can disqualify an otherwise strong bid. That is why structured evaluation criteria matter — and that is what we will explore now.",
        visual="Hero area: split-screen image — price tag icon on left, checklist icon on right, with caption 'Price vs. compliance — which matters more?' Below: two paragraphs of body text. CTA button at bottom-right.",
        interaction="Static hook slide. CTA button 'Let's explore →' advances to next slide. No branching."))

sb.add_L07("1.2-3", "Tender evaluation overview", [
    ("Develop\ncriteria", "Set the method, weighting, and evidence expectations before bids open"),
    ("Pre-\nqualification", "Confirm mandatory eligibility and shortlist integrity"),
    ("Score &\nrank", "Apply technical, financial, commercial, and compliance criteria"),
    ("Moderate &\nconsensus", "Resolve scoring differences and agree defensible rationale"),
    ("Presentations &\nclarifications", "Clarify proposals without uncontrolled re-bidding"),
    ("Due\ndiligence", "Verify delivery capability, compliance, and financial integrity"),
    ("Document\n& award", "Record outcome, approve, standstill/debrief, and award"),
], notes=sb._format_notes(
    vo="Here is the evaluation process at a glance. The defensible pathway has seven steps: develop criteria, pre-qualification, score and rank, moderation and consensus, presentations or clarifications, due diligence, and finally documenting the outcome through approval, standstill or debrief requirements, and award.",
    visual="Seven-step horizontal stepper with compact labels. Use two-line labels and short captions so all steps fit.",
    interaction="Static stepper. No interaction. Serves as an overview before the anchor deep-dive."))

eval_tiles = [
    ("📐", "Develop evaluation criteria"),
    ("🧾", "Pre-qualification"),
    ("📊", "Score and rank bidders"),
    ("🤝", "Moderate and reach consensus"),
    ("🎤", "Presentations and clarifications"),
    ("🔎", "Due diligence"),
    ("✅", "Document outcome and award"),
]
sb.add_anchor("1.2-4", "The evaluation process", eval_tiles,
    subtitle="Explore the seven evaluation steps and the controls that make the outcome defensible.",
    notes=sb._format_notes(
        vo="Now let's go deeper. Click each step to see what happens, how it is controlled, and where EY supports a fair and documented process.",
        visual="Seven horizontal bars stacked vertically, numbered 01-07. All in unvisited state.",
        interaction="Rise-friendly build: use accordion, tabs, or buttons rather than bespoke overlays if building in Rise. All seven items must be visited before Continue activates."))

sb.add_popup_text("1.2-4-01", "The evaluation process", 1, "Develop evaluation criteria",
    body="Evaluation criteria define what matters, how it is weighted, and what evidence evaluators will use before any bids are opened.",
    bullets=[
        "Define technical, financial, commercial, compliance, and value-for-money criteria",
        "Set weighting, scoring scale, minimum thresholds, evaluator roles, and conflict controls",
        "Document the method in the evaluation manual and train evaluators before scoring begins",
        "EY role: help finalize the evaluation manual, evidence requirements, and evaluator briefing",
    ],
    key_message="Criteria must be locked before bids are opened — changing them mid-process undermines fairness.",
    notes=sb._format_notes(
        vo="The first step is developing the criteria. The evaluation method, weighting, evidence expectations, and evaluator roles need to be documented before scoring starts. This is one of the foundations of defensibility.",
        visual="Dark pop-up panel. Body text, four dash bullets, and a yellow key-message bar at the bottom.",
        interaction="Pop-up/content layer on anchor 1.2-4. Close returns to anchor. Tile 01 gets checkmark."))

sb.add_popup_text_media("1.2-4-02", "The evaluation process", 2, "Pre-qualification",
    body="Pre-qualification confirms whether bidders meet mandatory eligibility and capability requirements before full comparative evaluation proceeds.",
    bullets=[
        "Check pass/fail requirements such as eligibility, certifications, financial capacity, insurance, conflicts, and minimum experience",
        "Separate non-compliant or ineligible bids before detailed scoring where procurement rules require it",
        "Record the decision trail for each bidder, including any clarification requests",
        "EY role: support the pre-qualification framework and review evidence for consistency",
    ],
    media_label="{{MEDIA: Pre-qualification matrix — mandatory criteria and pass/fail status}}",
    notes=sb._format_notes(
        vo="Pre-qualification is more than admin screening. It protects the evaluation from comparing bids that should not proceed, and it creates an early decision trail for eligibility and mandatory compliance.",
        visual="Dark pop-up panel. Left: body text and four dash bullets. Right: pre-qualification matrix placeholder.",
        interaction="Pop-up/content layer on anchor 1.2-4. Close returns to anchor. Tile 02 gets checkmark."))

sb.add_popup_text_media("1.2-4-03", "The evaluation process", 3, "Score and rank bidders",
    body="Evaluators apply the approved criteria to score compliant proposals and build an initial ranking.",
    bullets=[
        "Evaluators score independently against the published criteria and evidence in the submission",
        "Technical, financial, commercial, and compliance streams may be scored separately before combining",
        "Financial evaluation includes price scoring, affordability, cost-structure analysis, and value-for-money implications",
        "EY role: support scoring tools, quality checks, and financial evaluation integrity",
    ],
    media_label="{{MEDIA: Evaluation matrix with technical, financial, commercial, and compliance columns}}",
    notes=sb._format_notes(
        vo="Once pre-qualification is complete, evaluators score and rank the proposals against the approved method. The initial ranking is not the end of the process; it still needs moderation, clarifications where appropriate, due diligence, and documentation.",
        visual="Dark pop-up panel. Left: body text and four dash bullets. Right: evaluation matrix placeholder.",
        interaction="Pop-up/content layer on anchor 1.2-4. Close returns to anchor. Tile 03 gets checkmark."))

sb.add_popup_text_media("1.2-4-04", "The evaluation process", 4, "Moderate and reach consensus",
    body="Moderation turns independent scoring into a documented panel position by resolving material differences and agreeing the rationale for final scores.",
    bullets=[
        "Compare evaluator scores and identify outliers, evidence gaps, or inconsistent interpretations",
        "Facilitate consensus discussions without allowing unsupported score changes",
        "Record agreed scores, rationale, dissenting views where relevant, and decision owners",
        "EY role: facilitate moderation and protect consistency across technical and financial streams",
    ],
    media_label="{{MEDIA: Consensus flow — independent scores → moderation → agreed rationale → final score}}",
    notes=sb._format_notes(
        vo="Moderation is the step that was missing from the simpler AI flow. It matters because it turns individual judgement into a panel decision with an auditable rationale.",
        visual="Dark pop-up panel. Left: body text and four dash bullets. Right: consensus flow diagram placeholder.",
        interaction="Pop-up/content layer on anchor 1.2-4. Close returns to anchor. Tile 04 gets checkmark."))

sb.add_popup_text("1.2-4-05", "The evaluation process", 5, "Presentations and clarifications",
    body="Presentations and clarifications can resolve ambiguities, but they must not become a backdoor route to re-bid or change the evaluation rules.",
    bullets=[
        "Use presentations to test understanding of the submitted proposal, delivery approach, key personnel, or assumptions",
        "Use written clarifications to resolve ambiguities, omissions, or inconsistencies in the bid record",
        "Keep questions consistent, documented, and tied to the submitted offer and evaluation method",
        "EY role: prepare questions, facilitate sessions, and maintain the clarification audit trail",
    ],
    key_message="Clarify the proposal — do not replace the proposal.",
    notes=sb._format_notes(
        vo="Presentations and clarifications help evaluators understand the proposal, but they are not a chance to rewrite the bid or change the scoring rules. The audit trail matters here.",
        visual="Dark pop-up panel. Body text, four dash bullets, and a yellow key-message bar.",
        interaction="Pop-up/content layer on anchor 1.2-4. Close returns to anchor. Tile 05 gets checkmark."))

sb.add_popup_text_media("1.2-4-06", "The evaluation process", 6, "Due diligence",
    body="Before finalising the preferred bidder, due diligence verifies that the bidder can actually deliver. Three structured sub-checks ensure nothing is missed.",
    bullets=[
        "Sub-check 1 — Financial integrity: assess credit rating, balance-sheet strength, parent-company guarantees, and cash-flow adequacy to sustain the contract",
        "Sub-check 2 — Compliance documents: verify that mandatory certifications, insurances, licences, and regulatory approvals are current and valid",
        "Sub-check 3 — Clarifications: request written answers to proposal ambiguities — scope gaps, resourcing assumptions, or delivery-timeline questions",
        "Reference checks run in parallel: contact previous clients to verify track record and performance",
        "EY role: lead financial integrity checks and coordinate the clarification process",
    ],
    media_label="{{MEDIA: Three-panel due diligence checklist — Financial integrity | Compliance documents | Clarifications}}",
    notes=sb._format_notes(
        vo="Due diligence verifies that the preferred bidder can actually deliver. Financial integrity, compliance documents, clarifications, and reference checks all reduce the risk of recommending a bidder on untested assumptions.",
        visual="Dark pop-up panel. Left: body text and five dash bullets structured around three sub-checks. Right: three-panel due diligence checklist.",
        interaction="Pop-up/content layer on anchor 1.2-4. Close returns to anchor. Tile 06 gets checkmark. Dev note: in Rise, the three sub-checks can become nested accordion rows."))

sb.add_popup_stepper("1.2-4-07", "The evaluation process", 7, "Document outcome and award",
    bullets=[
        "Prepare the evaluation report with scores, moderated justifications, clarifications, due-diligence findings, and recommendation",
        "Obtain governance approvals before naming or contracting with the preferred proponent",
        "Observe standstill requirements where applicable and prepare debriefs for unsuccessful bidders",
        "EY role: help build the value-for-money rationale and defensible award record",
    ],
    steps=[
        ("Report", "Evaluation record"),
        ("Approve", "Governance"),
        ("Debrief", "Standstill / letters"),
        ("Award", "Award notice"),
    ],
    notes=sb._format_notes(
        vo="The final step is not just selecting a bidder. The outcome has to be documented, approved, and communicated. The evaluation report, governance trail, standstill or debrief material, and award notice make the decision defensible.",
        visual="Dark pop-up panel. Left: four dash bullets. Right: four-step process flow — Report → Approve → Debrief → Award.",
        interaction="Pop-up/content layer on anchor 1.2-4. Close returns to anchor. Tile 07 gets checkmark."))

sb.add_anchor_visited("1.2-4-visited", "The evaluation process", eval_tiles,
    subtitle="All components explored. Click Continue to test your knowledge.",
    notes=sb._format_notes(
        vo="Great — you have now explored all seven steps of the evaluation process. Let's see how well you have understood the material.",
        visual="Seven horizontal bars with green checkmarks. Continue button active.",
        interaction="All tiles visited. Continue button advances to MCQ."))

mcq_stem_12 = "Which of the following best describes EY's role during moderation and consensus scoring?"
mcq_options_12 = [
    "Drafting bidder proposals",
    "Facilitating documented consensus sessions for technical and financial streams",
    "Conducting legal negotiations with bidders",
    "Preparing the initial RFQ document",
]
sb.add_L09_default("1.2-5a", "Knowledge check", mcq_stem_12, mcq_options_12,
    notes=sb._format_notes(
        vo="Time for a knowledge check. Read the question carefully and select the best answer.",
        visual="Question stem at top. Four radio-button options (A–D). Submit button at bottom-right.",
        interaction="L09 MCQ default state. Learner selects one option and clicks Submit. No feedback visible yet."))

sb.add_L09_feedback("1.2-5b", "Knowledge check", mcq_stem_12, mcq_options_12,
    correct_idx=1,
    feedback_correct="That's right. EY's role during moderation is to facilitate documented consensus sessions, ensuring fairness, consistency, and an auditable rationale across evaluation streams.",
    feedback_incorrect="Not quite. EY does not draft proposals, conduct legal negotiations, or prepare the RFQ. EY's role at this stage is to facilitate and document the consensus scoring process.",
    notes=sb._format_feedback_notes(
        vo="Let's see how you did.",
        correct="That's right. EY's role during moderation is to facilitate documented consensus sessions, ensuring fairness, consistency, and an auditable rationale.",
        incorrect="Not quite. EY does not draft proposals, conduct legal negotiations, or prepare the RFQ. EY's role at this stage is to facilitate and document the consensus scoring process.",
        dev="L09 feedback state. Left 2/3 shows question with selected answer marked. Right 1/3 is feedback panel — green header for correct, red for incorrect. Continue button in feedback panel."))

sb.add_L10_default("1.2-6a", "Scenario: Evaluator disagreement",
    context="Two evaluators have given significantly different technical scores for the same bidder. The gap is large enough to affect the final ranking. What should EY do?",
    choices=[
        "Average the two scores\nand move on",
        "Facilitate a consensus\ndiscussion to align\non scoring",
        "Ask the client to decide\nwithout discussion",
        "Disqualify the bidder\nimmediately",
    ],
    notes=sb._format_notes(
        vo="Here is a scenario. Two evaluators have scored the same bidder very differently — and the gap could change the final ranking. What should EY do? Choose the best response.",
        visual="Scenario box at top with context text. Four choice buttons below in a row.",
        interaction="L10 scenario default state. Learner selects one choice. Submit triggers feedback."))

sb.add_L10_feedback("1.2-6b", "Scenario: Evaluator disagreement",
    context="Two evaluators have given significantly different technical scores for the same bidder. The gap is large enough to affect the final ranking. What should EY do?",
    chosen="Facilitate a consensus discussion to align on scoring",
    consequence="Correct. EY should facilitate a consensus discussion to ensure fairness and transparency.\n\n• Averaging scores without discussion can lead to unfair evaluation.\n• Asking the client to decide bypasses EY's facilitation role.\n• Disqualification without clarification is against best practices.\n\nConsensus scoring is how you turn disagreement into a fair, defensible result.",
    notes=sb._format_feedback_notes(
        vo="The best response is to facilitate a consensus discussion. Averaging scores hides the disagreement. Passing it to the client bypasses EY's role. And disqualification without investigation is never appropriate.",
        correct="Correct! EY should facilitate a consensus discussion to ensure fairness and transparency in the scoring process.",
        incorrect="Not the best choice. The correct approach is to facilitate a consensus discussion — this is core to EY's facilitation role during evaluation.",
        dev="L10 feedback state. Left 2/3: scenario + selected choice highlighted. Right 1/3: consequence/feedback panel. Continue button in panel."))

sb.add_L14("1.2-7", "eLearning 1 summary", [
    "Tender documents ensure transparency, compliance, and fair evaluation",
    "Evaluation criteria must be finalised before bids are opened",
    "Pre-qualification screens eligibility before detailed comparative scoring",
    "Moderation and consensus convert individual scores into a documented panel rationale",
    "Presentations, clarifications, and due diligence test ambiguity without changing the rules",
    "The award record needs scores, justifications, approvals, standstill/debrief evidence, and final recommendation",
], cta="Continue to eLearning 2",
    notes=sb._format_notes(
        vo="Let's wrap up eLearning 1. Tender documents set the rules. Pre-qualification screens eligibility. Scoring, moderation, clarifications, due diligence, and award documentation create the audit trail. The result is a fairer and more defensible decision.",
        visual="Six summary bars with yellow left-accent. 'Continue to eLearning 2' button at bottom-right.",
        interaction="Summary slide. Button advances to eLearning 2 title slide."))


# ═══════════════════════════════════════════════════════════════
# eLEARNING 2 — EXCLUSIVE CONTRACT NEGOTIATION
# ═══════════════════════════════════════════════════════════════

sb.add_title_slide(
    "eLearning 2",
    "Exclusive contract negotiation",
    "Navigating negotiations, transaction support, and contract preparation inputs")

# ── 2.1-1: Learning objectives ──
sb.add_L13("2.1-1", "Learning objectives", [
    "Identify where negotiations sit within the procurement lifecycle",
    "Explain what commercial close and financial close involve",
    "Apply key principles and best practices in exclusive contract negotiation",
], notes=sb._format_notes(
    vo="Welcome to eLearning 2. In this first lesson you will learn where negotiations fit in the procurement process, what happens during commercial and financial close, and the key principles that guide effective contract negotiation.",
    visual="Three objective bars with blue left-accent, numbered 01–03.",
    interaction="Static slide. Continue button."))

sb.add_L07("2.1-2", "The procurement process — where negotiations sit", [
    ("Market\nengagement", "Understand the market and identify potential suppliers"),
    ("RFQ", "Shortlist qualified bidders through a Request for Qualifications"),
    ("RFP", "Evaluate detailed proposals from shortlisted bidders"),
    ("Negotiations &\nagreements", "Finalise terms with the preferred proponent"),
], notes=sb._format_notes(
    vo="Let's start by placing negotiations in context. A typical public-sector procurement moves through four stages: market engagement, a Request for Qualifications, a Request for Proposals, and finally — negotiations and project agreements. This lesson focuses on that final stage.",
    visual="Four-step horizontal stepper. The fourth step 'Negotiations & agreements' is highlighted with a blue outline to show current focus.",
    interaction="Static stepper. Step 4 visually emphasised. Dev note: consider pulsing or glow animation on step 4 to draw the eye."))

sb.add_L03("2.1-3", "Entry into exclusive negotiation",
    media_label="{{MEDIA: Process strip — RFP evaluation → Preferred proponent selected → Exclusive negotiation begins}}",
    heading="From evaluation to negotiation",
    body="Once the RFP evaluation is complete and a preferred proponent is selected, that proponent enters exclusive negotiations. This is a structured phase — not a free-form discussion.",
    bullets=[
        "RFP evaluation leads to selection of a preferred proponent",
        "The preferred proponent enters exclusive negotiations",
        "Negotiations are structured around pre-defined commercial and legal terms",
        "Other shortlisted bidders may remain on standby as reserve",
    ],
    notes=sb._format_notes(
        vo="Once the RFP evaluation is complete, the highest-scoring bidder becomes the preferred proponent and enters exclusive negotiations. This is not a free-form conversation — it is a structured process focused on finalising the commercial and legal terms that will form the project agreement.",
        visual="Left: process strip showing the flow from RFP evaluation through preferred proponent selection to exclusive negotiation. Right: heading, body text, and four dash bullets.",
        interaction="Static content slide. No interaction. Continue button."))

sb.add_L06("2.1-4", "What negotiation finalises",
    col_a_header="COMMERCIAL CLOSE",
    col_a_items=[
        "Project agreement — the master contract",
        "Construction contract and services contract",
        "Letters of credit and performance security",
        "Representations and warranties",
    ],
    col_b_header="FINANCIAL CLOSE",
    col_b_items=[
        "Adapt the project agreement to Project Co.'s structure",
        "Align all project documents with financing requirements",
        "Adjust proposal price to reflect market movements",
        "Finalise funding and payment structures",
    ],
    notes=sb._format_notes(
        vo="Negotiations lead to two key milestones: commercial close and financial close. Commercial close finalises the project agreement, construction and services contracts, and all the supporting legal documents. Financial close then adapts those agreements to the preferred proponent's corporate structure, aligns them with financing requirements, and locks in the final pricing.",
        visual="Two-column comparison. Left header: 'Commercial close' with four dash-bullet items. Right header: 'Financial close' with four dash-bullet items.",
        interaction="Static comparison slide. Dev note: consider progressive reveal — commercial close first, then financial close."))

sb.add_L01("2.1-5", "Key principles and best practices",
    body="Effective negotiation requires discipline, structure, and attention to risk. These principles guide how EY supports clients through exclusive negotiations.",
    bullets=[
        "Start from the contract position, not the bidder's proposal — negotiate towards agreement, not away from it",
        "Convert uncertainty into enforceable contract protections — do not accept assurances without evidence",
        "Test every bidder claim against market norms and available data before accepting it",
        "Maintain momentum without sacrificing rigour — pace matters, but so does thoroughness",
        "Document every negotiation outcome in real time — verbal agreements are not agreements",
    ],
    notes=sb._format_notes(
        vo="These are the principles that guide effective negotiation. Start from the contract position. Convert uncertainty into protections. Test every claim. Keep momentum without losing rigour. And document everything as you go. These are not abstract ideas — they are practical disciplines that prevent problems at close and beyond.",
        visual="Body text at top, then five dash-bullet items below. Full-width single-column layout.",
        interaction="Static content slide. Continue button.\n\nSME / SOURCE-GAP NOTE: The source document (pptx p. 3, p. 24) names 'negotiations support' as a service offering but does not explicitly enumerate teachable principles or detailed transaction-support guidance. The five principles on this slide are synthesised from the broader procurement-advisory context and scenario patterns. Flag for SME validation before final sign-off."))

# ── 2.1-6: MCQ ──
mcq_stem_21 = "Which sequence best reflects the transition into negotiation and project agreement finalisation in a public-sector procurement process?"
mcq_options_21 = [
    "Market engagement → RFQ → RFP → negotiations and project agreements",
    "RFQ → contract management → market engagement → financial close",
    "Bid evaluation → contract closeout → RFP → RFQ",
    "Packaging analysis → supplier onboarding → dispute resolution → financial modelling",
]
sb.add_L09_default("2.1-6a", "Knowledge check", mcq_stem_21, mcq_options_21,
    notes=sb._format_notes(
        vo="Let's check your understanding. Which sequence correctly describes the transition into negotiations?",
        visual="Question stem at top. Four radio-button options A–D. Submit button.",
        interaction="L09 MCQ default state. Learner selects one option and clicks Submit."))

sb.add_L09_feedback("2.1-6b", "Knowledge check", mcq_stem_21, mcq_options_21,
    correct_idx=0,
    feedback_correct="Correct. The standard sequence is market engagement → RFQ → RFP → negotiations and project agreements. Each stage builds on the previous one.",
    feedback_incorrect="Not quite. The correct sequence is: market engagement → RFQ → RFP → negotiations and project agreements. The other sequences mix up stages or include post-award activities.",
    notes=sb._format_feedback_notes(
        vo="Let's review the answer.",
        correct="Correct. The standard public-sector procurement sequence is market engagement, then RFQ, then RFP, then negotiations and project agreements.",
        incorrect="Not quite. The correct sequence is market engagement → RFQ → RFP → negotiations and project agreements. The other options mix procurement stages with post-award activities.",
        dev="L09 feedback state. Left 2/3: question with selected answer. Right 1/3: feedback panel. Continue button."))

# ── 2.1-7: Scenario 1 — Evidence gap ──
sb.add_L10_default("2.1-7a", "Scenario: Evidence gap",
    context="A bidder lacks experience in cold-climate operations. There is no winter performance data in their submission. The bidder assures you their team can handle it. What would you do next?",
    choices=[
        "Proceed and manage\nwinter risk through\noperations later",
        "Pause to require evidence\nand convert uncertainty\ninto enforceable contract\nprotections",
        "Adjust evaluation scoring\nto reflect the gap",
    ],
    notes=sb._format_notes(
        vo="Here is your first scenario. A bidder has no cold-climate experience and no winter performance data, but they assure you their team can handle it. What is the right move?",
        visual="Scenario box at top. Three choice buttons below.",
        interaction="L10 scenario default. Learner selects one choice."))

sb.add_L10_feedback("2.1-7b", "Scenario: Evidence gap",
    context="A bidder lacks experience in cold-climate operations. There is no winter performance data in their submission. The bidder assures you their team can handle it. What would you do next?",
    chosen="Pause to require evidence and convert uncertainty into enforceable contract protections",
    consequence="Correct. Verbal assurances are not evidence. The right approach is to pause, require the bidder to provide verifiable winter-performance data, and — if the gap remains — convert the uncertainty into specific contract protections: milestones, reporting requirements, remedies for underperformance.\n\n• Proceeding without evidence creates unmanaged risk.\n• Adjusting evaluation scoring is a backward step — criteria should already be locked.",
    notes=sb._format_feedback_notes(
        vo="The right answer is to pause and require evidence. Assurances without data are worthless in a contract. Convert the uncertainty into enforceable protections — milestones, reporting, and remedies.",
        correct="Correct. Pause, require evidence, and convert uncertainty into enforceable contract protections. Never accept assurances without supporting data.",
        incorrect="Not the best choice. The correct approach is to pause, require evidence, and build contract protections. Proceeding without evidence or adjusting locked criteria are both problematic.",
        dev="L10 feedback state. Consequence panel on right 1/3. Continue button."))

# ── 2.1-8: Scenario 2 — Timeline realism ──
sb.add_L10_default("2.1-8a", "Scenario: Timeline realism",
    context="A bidder proposes a 6-month fleet-refurbishment turnaround. The market norm is 12–18 months. The bidder is confident they can deliver. What would you do next?",
    choices=[
        "Accept the timeline\nto maintain momentum",
        "Test and de-risk the plan\nthrough contractual\nmilestones, evidence,\nand remedies",
        "Flag the issue for the\nclient to decide\npost-award",
    ],
    notes=sb._format_notes(
        vo="Second scenario. A bidder claims they can refurbish a fleet in six months. The market norm is twelve to eighteen. They are confident. What should you do?",
        visual="Scenario box at top. Three choice buttons below.",
        interaction="L10 scenario default. Learner selects one choice."))

sb.add_L10_feedback("2.1-8b", "Scenario: Timeline realism",
    context="A bidder proposes a 6-month fleet-refurbishment turnaround. The market norm is 12–18 months. The bidder is confident they can deliver. What would you do next?",
    chosen="Test and de-risk the plan through contractual milestones, evidence, and remedies",
    consequence="Correct. A timeline that is half the market norm is a red flag, not a selling point. The right approach is to test the plan: require evidence of how they will achieve it, set contractual milestones to track progress, and build in remedies if they fall behind.\n\n• Accepting the timeline to maintain momentum creates schedule risk.\n• Flagging for post-award decision defers the problem — it does not solve it.",
    notes=sb._format_feedback_notes(
        vo="The right answer is to test and de-risk. A six-month claim against a twelve-to-eighteen-month norm needs evidence, milestones, and contractual remedies. Do not accept it at face value, and do not defer the problem.",
        correct="Correct. Test the plan, require evidence, set milestones, and build in remedies. An aggressive timeline needs contractual safeguards.",
        incorrect="Not the best choice. The correct approach is to test and de-risk the timeline through evidence requirements, milestones, and contractual remedies.",
        dev="L10 feedback state. Consequence panel on right 1/3. Continue button."))

sb.add_L14("2.1-9", "Lesson 2.1 summary", [
    "Negotiations follow RFP evaluation — the preferred proponent enters exclusive discussions",
    "Commercial close and financial close are the two key milestones",
    "Convert uncertainty into enforceable contract protections — never accept assurances alone",
    "Test every bidder claim against market norms before accepting it",
], notes=sb._format_notes(
    vo="To recap: negotiations come after RFP evaluation. They lead to two milestones — commercial close and financial close. Always convert uncertainty into protections. And always test bidder claims against what the market actually supports.",
    visual="Four summary bars with yellow left-accent. Continue button.",
    interaction="Static summary. Continue button advances to Lesson 2.2."))


# ═══════════════════════════════════════════════════════════════
# LESSON 2.2 — Commercial and financial inputs for contract prep
# ═══════════════════════════════════════════════════════════════

sb.add_L13("2.2-1", "Learning objectives", [
    "Identify the commercial inputs required for contract preparation",
    "Identify the financial inputs required for contract preparation",
    "Explain how those inputs appear in commercial close and financial close documents",
], notes=sb._format_notes(
    vo="In this second lesson, you will learn to identify the commercial and financial inputs that feed into contract preparation — and how they show up in the documents produced at close.",
    visual="Three objective bars with blue left-accent, numbered 01–03.",
    interaction="Static slide. Continue button."))

input_tiles = [
    ("📄", "Commercial inputs"),
    ("💰", "Financial inputs"),
    ("📋", "How inputs show up at close"),
    ("🤝", "EY service line touch points"),
]
sb.add_anchor("2.2-2", "Contract preparation inputs", input_tiles,
    subtitle="Click each component to explore what goes into contract preparation.",
    notes=sb._format_notes(
        vo="Contract preparation draws on two streams of inputs — commercial and financial — that come together at close. Click each component to explore what they are, where they come from, and how they appear in the final documents.",
        visual="Four horizontal bars stacked vertically, numbered 01–04. All unvisited.",
        interaction="Anchor/menu slide (L12). All four tiles must be visited before Continue activates."))

sb.add_popup_text("2.2-2-01", "Contract preparation inputs", 1, "Commercial inputs",
    body="Commercial inputs define the contractual structure and terms. They come from procurement, transaction development, and contract-development workstreams.",
    bullets=[
        "What they are: contract types, key contractual terms and conditions",
        "Where they come from: procurement and transaction development work",
        "Who contributes: technical advisors, financial advisors, legal advisors, procurement authority, transaction process advisors",
        "Why they matter: they shape the contractual structure to be finalised at close",
        "How they appear at close: project agreement, construction contract, services contract, letters of credit, performance security",
    ],
    key_message="Commercial inputs define the 'what' and 'how' of the contract — without them, there is nothing to negotiate.",
    notes=sb._format_notes(
        vo="Commercial inputs are the building blocks of the contract. They define the contract types, key terms, and conditions. These come from procurement and transaction development work, with contributions from technical, financial, and legal advisors as well as the procurement authority. At close, they materialise as the project agreement, construction and services contracts, letters of credit, and performance security.",
        visual="Dark pop-up panel. Body text, five dash bullets using what/where/who/why/how-at-close structure, and a yellow key-message bar at bottom.",
        interaction="Pop-up overlay on anchor 2.2-2. X close returns to anchor. Tile 01 gets checkmark."))

sb.add_popup_text("2.2-2-02", "Contract preparation inputs", 2, "Financial inputs",
    body="Financial inputs support pricing, funding, and value-for-money analysis. They come from financial submission requirements and financial advisory work.",
    bullets=[
        "What they are: financial plan, financing/funding plan, financial modelling, price form(s)",
        "Where they come from: financial submission requirements and financial analysis",
        "Who contributes: financial advisors and related project/advisory roles",
        "Why they matter: they support financial suitability, VfM analysis, pricing, and funding structure",
        "How they appear at close: adapted project agreement, aligned project documents, proposal-price adjustment for market movements, finalised payment structures",
    ],
    key_message="Financial inputs answer the 'how much' and 'how funded' — they are the numbers behind the contract.",
    notes=sb._format_notes(
        vo="Financial inputs are the numbers behind the contract. They include the financial plan, funding plan, financial modelling, and price forms. Financial advisors are the primary contributors, and these inputs drive the value-for-money analysis, pricing decisions, and funding structure. At close, they appear as the adapted project agreement, aligned documents, market-adjusted pricing, and finalised payment structures.",
        visual="Dark pop-up panel. Body text, five dash bullets (what/where/who/why/how-at-close), and a yellow key-message bar.",
        interaction="Pop-up overlay on anchor 2.2-2. X close returns to anchor. Tile 02 gets checkmark."))

sb.add_popup_compare("2.2-2-03", "Contract preparation inputs", 3,
    "How inputs show up at close",
    col_a_header="COMMERCIAL CLOSE DOCUMENTS",
    col_a_items=[
        "Project agreement (master contract)",
        "Construction contract",
        "Services contract",
        "Letters of credit",
        "Performance security",
    ],
    col_b_header="FINANCIAL CLOSE DOCUMENTS",
    col_b_items=[
        "Project agreement adapted to Project Co. structure",
        "Alignment across all project documents",
        "Proposal-price adjustment for market movements",
        "Finalised payment structures and timing",
    ],
    key_message="Notice: timing, payment structures, and document alignment are the critical watch-points at close.",
    notes=sb._format_notes(
        vo="Here is where it all comes together. At commercial close, the outputs are the project agreement, construction and services contracts, letters of credit, and performance security. At financial close, the project agreement is adapted to the preferred proponent's structure, documents are aligned with financing requirements, and pricing is adjusted for any market movements since proposal submission.",
        visual="Dark pop-up panel with two-column comparison. Left: commercial close documents. Right: financial close documents. Key-message bar at bottom.",
        interaction="Pop-up overlay on anchor 2.2-2. X close returns to anchor. Tile 03 gets checkmark."))

sb.add_popup_text("2.2-2-04", "Contract preparation inputs", 4, "EY service line touch points",
    body="Contract preparation does not happen in isolation. Multiple EY service lines contribute expertise at different stages of the process.",
    bullets=[
        "What they are: cross-functional advisory inputs — governance, deal structuring, legal drafting, and negotiation facilitation",
        "Where they come from: EY Internal Audit, Transaction Advisory, Legal Advisory, and Negotiations Support teams",
        "Who contributes: IA advisors (governance), transaction advisors (financial modelling), legal advisors (contract drafting), negotiation leads (close facilitation)",
        "Why they matter: no single service line holds the full picture — coordination prevents gaps and misalignment",
        "How they appear at close: integrated governance sign-offs, validated financial models, legally reviewed contract suite, facilitated close sessions",
    ],
    key_message="Effective contract preparation requires cross-service-line coordination — no single team has the full picture.",
    notes=sb._format_notes(
        vo="Contract preparation is a team effort. EY's Internal Audit practice advises on governance and compliance. Transaction advisory supports deal structuring and modelling. Legal advisory handles contract drafting and risk allocation. And the negotiations support team facilitates the close process itself. At close, you see their work in governance sign-offs, validated models, legally reviewed contracts, and facilitated close sessions.",
        visual="Dark pop-up panel. Body text, five dash bullets (what/where/who/why/how-at-close), and a yellow key-message bar.",
        interaction="Pop-up overlay on anchor 2.2-2. X close returns to anchor. Tile 04 gets checkmark."))

sb.add_anchor_visited("2.2-2-visited", "Contract preparation inputs", input_tiles,
    subtitle="All components explored. Click Continue to test your knowledge.",
    notes=sb._format_notes(
        vo="You have now explored all four components of contract preparation inputs. Let's put your knowledge to the test.",
        visual="Four horizontal bars with green checkmarks. Continue button active.",
        interaction="All tiles visited. Continue button advances to MCQ."))

# ── 2.2-3: MCQ ──
mcq2_stem = "Which set of inputs is most directly associated with contract preparation?"
mcq2_options = [
    "Funding structure, financial model inputs, price forms, payment terms, and contract-related assumptions",
    "Community feedback, maintenance logs, variation history, and closeout reports",
    "Bidder interview notes, shortlist rankings, and debrief letters",
    "KPI scorecards, claims registers, and handover certificates",
]
sb.add_L09_default("2.2-3a", "Knowledge check", mcq2_stem, mcq2_options,
    notes=sb._format_notes(
        vo="Time for a knowledge check. Which set of inputs is most directly associated with contract preparation?",
        visual="Question stem. Four radio-button options A–D. Submit button.",
        interaction="L09 MCQ default state."))

sb.add_L09_feedback("2.2-3b", "Knowledge check", mcq2_stem, mcq2_options,
    correct_idx=0,
    feedback_correct="Correct. Funding structure, financial model inputs, price forms, payment terms, and contract-related assumptions are the core financial and commercial inputs that feed directly into contract preparation.",
    feedback_incorrect="Not quite. The correct answer includes funding structure, financial model inputs, price forms, payment terms, and contract-related assumptions. The other options describe post-award, evaluation, or operational activities — not contract preparation inputs.",
    notes=sb._format_feedback_notes(
        vo="Let's review.",
        correct="Correct. These are the core financial and commercial inputs that feed directly into contract preparation.",
        incorrect="Not quite. The correct answer is A — these are the inputs that directly drive contract preparation. The other options relate to post-award, evaluation, or operational activities.",
        dev="L09 feedback state. Continue button."))

# ── 2.2-4: Scenario — Incomplete inputs ──
sb.add_L10_default("2.2-4a", "Scenario: Incomplete inputs",
    context="The team is preparing contract documentation after selecting the preferred proponent. Technical inputs are available, but key commercial and financial inputs are incomplete. What should the team obtain next?",
    choices=[
        "Closeout reports and\nlessons learned",
        "Contract terms/structures\nplus funding-plan, model,\nand price-form inputs",
        "Performance dashboards\nand compliance reports",
        "Dispute-board procedures\nand live claims records",
    ],
    notes=sb._format_notes(
        vo="Here is a scenario. The team is preparing contract documentation, but commercial and financial inputs are incomplete. What should they prioritise?",
        visual="Scenario box at top. Four choice buttons below.",
        interaction="L10 scenario default."))

sb.add_L10_feedback("2.2-4b", "Scenario: Incomplete inputs",
    context="The team is preparing contract documentation after selecting the preferred proponent. Technical inputs are available, but key commercial and financial inputs are incomplete. What should the team obtain next?",
    chosen="Contract terms/structures plus funding-plan, model, and price-form inputs",
    consequence="Correct. The missing inputs are the commercial terms and structures plus the financial inputs — funding plan, financial model, and price forms. These are essential for contract preparation and cannot be deferred.\n\n• Closeout reports and lessons learned are post-contract activities.\n• Performance dashboards relate to contract management, not preparation.\n• Dispute-board procedures are post-award operational tools.",
    notes=sb._format_feedback_notes(
        vo="The right answer is to obtain the missing commercial terms and financial inputs. These are the building blocks of the contract — without them, you cannot prepare the documentation.",
        correct="Correct. The team needs contract terms/structures and the financial inputs — funding plan, model, and price forms.",
        incorrect="Not the best choice. The correct answer is B — contract terms/structures plus funding-plan, model, and price-form inputs are what drive contract preparation.",
        dev="L10 feedback state. Continue button."))

# ── 2.2-5: Scenario — Financial strength changes ──
sb.add_L10_default("2.2-5a", "Scenario: Financial strength changes",
    context="A bidder's parent-company credit rating has deteriorated since submission. The bidder's technical proposal remains strong, and the team is deep in negotiations. What would you do next?",
    choices=[
        "Discontinue negotiations\nimmediately",
        "Tighten financial\nprotections and document\ngovernance approvals\nbefore close",
        "Rely on the bidder's\nassurances given their\ntechnical strength",
    ],
    notes=sb._format_notes(
        vo="Final scenario. The preferred bidder's parent company has had a credit downgrade since submitting their proposal. Their technical score is still strong and you are deep in negotiations. What do you do?",
        visual="Scenario box at top. Three choice buttons below.",
        interaction="L10 scenario default."))

sb.add_L10_feedback("2.2-5b", "Scenario: Financial strength changes",
    context="A bidder's parent-company credit rating has deteriorated since submission. The bidder's technical proposal remains strong, and the team is deep in negotiations. What would you do next?",
    chosen="Tighten financial protections and document governance approvals before close",
    consequence="Correct. A credit downgrade is a material change that needs to be addressed — but it does not necessarily mean walking away. The right approach is to tighten financial protections: additional security, stronger parent-company guarantees, tighter reporting requirements. And document the governance approvals for proceeding.\n\n• Discontinuing immediately may be disproportionate if protections can be secured.\n• Relying on assurances without action ignores a material financial risk.",
    notes=sb._format_feedback_notes(
        vo="The right answer is to tighten protections and get governance approvals. A credit downgrade is serious but manageable — if you build the right safeguards into the contract.",
        correct="Correct. Tighten financial protections and secure governance approvals before proceeding to close.",
        incorrect="Not the best choice. The correct approach is to tighten financial protections — additional security, stronger guarantees, tighter reporting — and document governance approvals before close.",
        dev="L10 feedback state. Continue button."))

sb.add_L14("2.2-6", "Programme summary", [
    "The throughline: every step exists to build a defensible procurement outcome",
    "Tender documents ensure transparency, compliance, and fair evaluation across the lifecycle",
    "Evaluation criteria must be locked before bids open — defensibility starts here",
    "Negotiations convert uncertainty into enforceable protections — tested against market norms",
    "Commercial and financial inputs produce the documented evidence trail that underpins defensibility at close",
    "If it is not documented, structured, and evidence-based — it is not defensible",
], cta="Complete programme",
    notes=sb._format_notes(
        vo="Thank you for completing both modules. If you take one thing from this programme, let it be this: every step in the procurement lifecycle — from writing tender documents to signing at close — exists to build a defensible outcome. Defensibility means that every decision can be explained, evidenced, and withstand scrutiny. Tender documents set the rules. Locked criteria prevent mid-stream challenge. Consensus scoring produces auditable records. Contract protections convert risk into documented safeguards. If it is not documented, structured, and evidence-based, it is not defensible. That is the standard. Well done.",
        visual="Six summary bars with yellow left-accent. 'Complete programme' button at bottom-right. First bar is visually distinct (bold or slightly larger) to signal the throughline.",
        interaction="Final slide. 'Complete programme' triggers SCORM completion. Dev note: the word 'defensible/defensibility' should appear in the programme's closing VO and on-screen as the unifying theme."))

# ── Save ──
out = "/Users/qianhuisun/Desktop/elearning-skills/modules/storyboard-combined.pptx"
sb.save(out)
