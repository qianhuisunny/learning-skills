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
        `<div class="slide"><h1>Error loading module</h1><p>${esc(e.message)}</p></div>`;
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
      case "L03": return renderL03(slide);
      case "L09": return renderL09(slide);
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
