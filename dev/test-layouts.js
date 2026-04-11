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
