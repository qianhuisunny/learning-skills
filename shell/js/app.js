(function () {
  "use strict";

  const scorm = pipwerks.SCORM;
  scorm.version = "1.2";

  // ---------- Module state ----------
  const state = {
    content: null,
    currentIdx: 0,
    mcqState: {},   // slide_id → { selectedIdx, submitted, isCorrect }
    scenarioState: {}, // slide_id → { selectedIdx, submitted, isCorrect }
    matchState: {}, // slide_id → { selections: string[], submitted, isCorrect }
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
        `<div class="slide"><h1>Error loading module</h1><p>${esc(e.message)}</p></div>`;
      return;
    }
    document.title = state.content.module.title;

    state.maxScore = state.content.slides
      .filter(s => ["L09", "L10", "L11"].includes(s.layout))
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
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Render markdown-ish body lines: lines starting with "- " become bullets, others paragraphs.
  function renderBodyLines(lines) {
    const parts = [];
    let currentBullets = null;
    (lines || []).forEach(line => {
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

  function moduleLabelHtml() {
    return `<span class="module-label">${esc(state.content.module.module_label || "")}</span>`;
  }

  // ---------- Render ----------
  function renderSlide() {
    const slide = currentSlide();
    const app = document.getElementById("app");
    app.innerHTML = "";
    app.appendChild(renderByLayout(slide));

    const visible = visibleSlides();
    const progress = document.getElementById("progress");
    progress.innerHTML = `Page <span class="current">${state.currentIdx + 1}</span>/${visible.length}`;
    document.getElementById("btn-prev").disabled = state.currentIdx === 0;

    const nextBtn = document.getElementById("btn-next");
    nextBtn.disabled = !canAdvance();
    const isLast = state.currentIdx === visible.length - 1;
    nextBtn.innerHTML = isLast ? "Finish" : "&#8594;";
    nextBtn.classList.toggle("finish", isLast);

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
    if (slide.layout === "L10") {
      const scenario = state.scenarioState[slide.id];
      return !!(scenario && scenario.submitted);
    }
    if (slide.layout === "L11") {
      const match = state.matchState[slide.id];
      return !!(match && match.submitted);
    }
    if (slide.layout === "L12") {
      const menu = state.menuState[slide.id] || { visited: new Set() };
      return menu.visited.size >= slide.bars.length;
    }
    return true;
  }

  function refreshNextBtn() {
    const nextBtn = document.getElementById("btn-next");
    if (nextBtn) nextBtn.disabled = !canAdvance();
  }

  function renderByLayout(slide) {
    switch (slide.layout) {
      case "L01": return renderL01(slide);
      case "L02": return renderL02(slide);
      case "L03": return renderL03(slide);
      case "L04": return renderL04(slide);
      case "L05": return renderL05(slide);
      case "L06": return renderL06(slide);
      case "L07": return renderL07(slide);
      case "L08": return renderL08(slide);
      case "L09": return renderL09(slide);
      case "L10": return renderL10(slide);
      case "L11": return renderL11(slide);
      case "L12": return renderL12(slide);
      case "L13": return renderL13(slide);
      case "L14": return renderL14(slide);
      default: {
        const el = document.createElement("div");
        el.className = "slide";
        el.innerHTML = `<h1>Unknown layout</h1><p>${esc(slide.layout)}</p>`;
        return el;
      }
    }
  }

  // ---------- Layout renderers ----------
  function renderL01(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l01";
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <div class="body">${renderBodyLines(slide.body)}</div>
    `;
    return el;
  }

  function renderL03(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l03";
    const media = slide.media || { placeholder: "media placeholder" };
    const heading = slide.heading ? `<h2>${esc(slide.heading)}</h2>` : "";
    const bullets = (slide.bullets || []).map(b => `<li>${esc(b)}</li>`).join("");
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <div class="grid">
        <div class="media">{{MEDIA_1}}<br>${esc(media.placeholder)}</div>
        <div class="text">${heading}<ul class="bullets">${bullets}</ul></div>
      </div>
    `;
    return el;
  }

  function renderL02(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l02";
    const cta = slide.cta ? `<button class="cta" type="button">${esc(slide.cta)}</button>` : "";
    el.innerHTML = `
      ${moduleLabelHtml()}
      <div class="hero">${esc(slide.hero_label || slide.title)}</div>
      <h1>${esc(slide.title)}</h1>
      <div class="body">${renderBodyLines(slide.body)}</div>
      ${cta}
    `;
    return el;
  }

  function renderL04(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l04";
    const media = slide.media || { placeholder: "media placeholder" };
    const heading = slide.heading ? `<h2>${esc(slide.heading)}</h2>` : "";
    const bullets = (slide.bullets || []).map(b => `<li>${esc(b)}</li>`).join("");
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <div class="grid">
        <div class="text">${heading}<div class="body">${renderBodyLines(slide.body || [])}</div><ul class="bullets">${bullets}</ul></div>
        <div class="media">{{MEDIA_1}}<br>${esc(media.placeholder)}</div>
      </div>
    `;
    return el;
  }

  function renderL05(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l05";
    const cards = (slide.cards || []).map(card => `
      <li class="card">
        <span class="icon">${esc(card.icon || "•")}</span>
        <h2>${esc(card.title)}</h2>
        <p>${esc(card.body)}</p>
      </li>
    `).join("");
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <ul class="cards">${cards}</ul>
    `;
    return el;
  }

  function renderL06(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l06";
    const columns = (slide.columns || []).slice(0, 2).map(col => `
      <section class="compare-col">
        <h2>${esc(col.heading)}</h2>
        <ul class="bullets">${(col.items || []).map(i => `<li>${esc(i)}</li>`).join("")}</ul>
      </section>
    `).join("");
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <div class="compare">${columns}</div>
    `;
    return el;
  }

  function renderL07(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l07";
    const steps = (slide.steps || []).map((step, i) => `
      <li class="step">
        <span class="num">${String(i + 1).padStart(2, "0")}</span>
        <h2>${esc(step.label)}</h2>
        <p>${esc(step.caption)}</p>
      </li>
    `).join("");
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <ol class="steps">${steps}</ol>
    `;
    return el;
  }

  function renderL08(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l08";
    const nodes = (slide.nodes || []).map(node => `
      <li class="node">
        <h2>${esc(node.label)}</h2>
        <p>${esc(node.body)}</p>
      </li>
    `).join("");
    el.innerHTML = `
      ${moduleLabelHtml()}
      <h1>${esc(slide.title)}</h1>
      <ol class="timeline">${nodes}</ol>
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
          refreshNextBtn();
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

  function renderL10(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l10";
    const scenario = state.scenarioState[slide.id] || { selectedIdx: null, submitted: false, isCorrect: null };

    function draw() {
      const choices = (slide.choices || []).map((choice, i) => {
        const cls = [];
        if (scenario.selectedIdx === i) cls.push("selected");
        if (scenario.submitted) cls.push(choice.is_correct ? "correct-answer" : "disabled");
        return `<li class="${cls.join(" ")}" data-idx="${i}">${esc(choice.label)}</li>`;
      }).join("");
      const selected = scenario.selectedIdx != null ? (slide.choices || [])[scenario.selectedIdx] : null;
      const feedback = scenario.submitted && selected
        ? `<aside class="feedback-panel ${scenario.isCorrect ? "correct" : "incorrect"}">
             <h3>${scenario.isCorrect ? "Good decision" : "Consider the trade-off"}</h3>
             <p>${esc(selected.feedback || "")}</p>
           </aside>`
        : "";
      el.innerHTML = `
        ${moduleLabelHtml()}
        <h1>${esc(slide.title)}</h1>
        <section class="context">${esc(slide.context)}</section>
        <ul class="choices">${choices}</ul>
        ${feedback}
      `;
      if (!scenario.submitted) {
        el.querySelectorAll(".choices li").forEach(li => {
          li.addEventListener("click", () => {
            scenario.selectedIdx = parseInt(li.dataset.idx, 10);
            const choice = (slide.choices || [])[scenario.selectedIdx];
            scenario.isCorrect = !!(choice && choice.is_correct);
            scenario.submitted = true;
            state.scenarioState[slide.id] = scenario;
            if (scenario.isCorrect) {
              state.totalScore += (slide.points != null ? slide.points : 25);
            }
            draw();
            refreshNextBtn();
          });
        });
      }
    }
    draw();
    return el;
  }

  function renderL11(slide) {
    const el = document.createElement("div");
    el.className = "slide layout-l11";
    const pairs = slide.pairs || [];
    const targets = pairs.map(p => p.target);
    const match = state.matchState[slide.id] || {
      selections: new Array(pairs.length).fill(""),
      submitted: false,
      isCorrect: null
    };
    state.matchState[slide.id] = match;

    function draw() {
      const rows = pairs.map((pair, i) => {
        const opts = [`<option value="">Choose match</option>`].concat(targets.map(target => {
          const selected = match.selections[i] === target ? "selected" : "";
          return `<option value="${esc(target)}" ${selected}>${esc(target)}</option>`;
        })).join("");
        const result = match.submitted
          ? `<span class="result ${match.selections[i] === pair.target ? "correct" : "incorrect"}">${match.selections[i] === pair.target ? "Correct" : "Review"}</span>`
          : "";
        return `
          <li class="match-row">
            <span class="item">${esc(pair.item)}</span>
            <select data-idx="${i}" ${match.submitted ? "disabled" : ""}>${opts}</select>
            ${result}
          </li>
        `;
      }).join("");
      const allSelected = match.selections.every(Boolean);
      const feedback = match.submitted
        ? `<aside class="feedback-panel ${match.isCorrect ? "correct" : "incorrect"}">
             <h3>${match.isCorrect ? "All matched" : "Some matches need review"}</h3>
             <p>${esc(match.isCorrect ? slide.feedback_correct : slide.feedback_incorrect)}</p>
           </aside>`
        : "";
      el.innerHTML = `
        ${moduleLabelHtml()}
        <h1>${esc(slide.title)}</h1>
        <p class="instruction">${esc(slide.instruction)}</p>
        <ul class="matches">${rows}</ul>
        <button class="submit-btn" ${allSelected || match.submitted ? "" : "disabled"}>Submit</button>
        ${feedback}
      `;
      if (!match.submitted) {
        el.querySelectorAll("select").forEach(select => {
          select.addEventListener("change", () => {
            match.selections[parseInt(select.dataset.idx, 10)] = select.value;
            draw();
          });
        });
        el.querySelector(".submit-btn").addEventListener("click", () => {
          if (!match.selections.every(Boolean)) return;
          match.submitted = true;
          match.isCorrect = pairs.every((pair, i) => match.selections[i] === pair.target);
          if (match.isCorrect) {
            state.totalScore += (slide.points != null ? slide.points : 25);
          }
          draw();
          refreshNextBtn();
        });
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
                  <button class="popup-close" aria-label="Close">×</button>
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
          refreshNextBtn();
        });
      });
      const closeBtn = el.querySelector(".popup-close");
      if (closeBtn) {
        closeBtn.addEventListener("click", () => {
          menu.openBar = null;
          draw();
        });
      }
      // Also allow clicking the backdrop (outside the panel) to close
      const backdrop = el.querySelector(".popup-backdrop");
      if (backdrop) {
        backdrop.addEventListener("click", (ev) => {
          if (ev.target === backdrop) {
            menu.openBar = null;
            draw();
          }
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
    // Exit button removed — top-bar back arrow + Next/Finish handle all navigation
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
