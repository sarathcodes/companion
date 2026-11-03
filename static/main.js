$.getScript("/static/common.js");
$.getScript("/static/audio.js");

let curriculumClasses = [];
let b1Roadmap = null;
let studyProgress = { completed_exercises: [], completed_speaking: [], mastered_classes: [] };

let structuredCourseLevels = [];
let allCourseModules = [];
let courseProgress = {
  mastered_modules: [],
  module_scores: {},
  attempts_count: {},
  needs_review_modules: [],
  completed_a2_writing: []
};

let selectedLevelFilter = "ALL";
let activeQuestModuleId = null;
let activeQuestStep = 1; // 1 = Secret Rule, 2 = Word Cards, 3 = Boss Mic Challenge

let activeClassId = null;
let activeClassStep = 1; // 1 = Rule, 2 = Words, 3 = Quiz & Homework Mic

let activeOralRecordingId = null;
let activeOralBlobPromise = null;

// Common Daily Verbs & Right-Click Dictionary / Starred Words State
let commonDailyVerbs = [];
let starredWords = [];
let selectedVerbCategory = "ALL";
let activeVerbObj = null;
let lastDictLookupEntry = null;

const QUEST_EMOJIS = {
  "a1-m1": "👨‍👩‍👦",
  "a1-m2": "⏰",
  "a1-m3": "🥐",
  "a1-m4": "🚋",
  "a1-m5": "🩺",
  "a2-m1": "✈️",
  "a2-m2": "🧸",
  "a2-m3": "🏠",
  "a2-m4": "🎁",
  "a2-m5": "📅",
  "a2-m6": "✉️",
  "b1-m1": "🔮",
  "b1-m2": "♻️",
  "b1-m3": "⚖️",
  "b1-m4": "💡",
  "b1-m5": "🛎️",
  "b1-m6": "🏆"
};

const CLASS_EMOJIS = ["🏔️", "🚌", "🧗", "⏳", "💼", "🚆", "🪥", "🏢", "🎬", "☀️", "📸", "🎓", "🌟", "🚀"];

function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function speakFrenchText(text, btnEl) {
  if (!text) return;
  initAudio();
  const $btn = btnEl ? $(btnEl) : null;
  const origHtml = $btn ? $btn.html() : "";
  if ($btn) {
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin"></i>');
  }
  $.post("/api/speak_french", { text: text }, function (res) {
    if ($btn) {
      $btn.prop("disabled", false).html(origHtml || '<i class="fa-solid fa-volume-high"></i>');
    }
    if (res.file_url) {
      playSingleAudioFile(res.file_url);
    } else if (res.error) {
      showNotification(res.error);
    }
  }).fail(function () {
    if ($btn) {
      $btn.prop("disabled", false).html(origHtml || '<i class="fa-solid fa-volume-high"></i>');
    }
  });
}

function switchTab(tabId) {
  $(".fun-tab-btn").removeClass("active");
  $(`.fun-tab-btn[data-tab="${tabId}"]`).addClass("active");
  $(".tab-section").hide().removeClass("active");
  $(`#${tabId}`).show().addClass("active");

  if (tabId === "tab-course") {
    $("#quest-lesson-view").hide();
    $("#quest-map-view").show();
  } else if (tabId === "tab-classes") {
    $("#single-class-view").hide();
    $("#classes-grid-view").show();
  }
}

function updateTotalXP() {
  const masteredCount = (courseProgress.mastered_modules || []).length;
  const exCount = (studyProgress.completed_exercises || []).length;
  const spCount = (studyProgress.completed_speaking || []).length;
  const totalXP = (masteredCount * 100) + (spCount * 50) + (exCount * 20);
  $("#header-stars-count").text(totalXP);
}

function getStarsHtml(score, isMastered) {
  if (!score && !isMastered) return '<span class="text-muted">☆☆☆</span>';
  const s = score || (isMastered ? 8 : 0);
  if (s >= 9) return "⭐⭐⭐";
  if (s >= 8) return "⭐⭐☆";
  if (s >= 5) return "⭐☆☆";
  return "☆☆☆";
}

// =========================================================
// 1. AVENTURE A1 -> B1 (QUEST MAP & 3-STEP LESSON PLAYER)
// =========================================================

function loadStructuredCourseData() {
  $.get("/api/structured_course", function (data) {
    structuredCourseLevels = data.levels || [];
    courseProgress = data.progress || {
      mastered_modules: [],
      module_scores: {},
      attempts_count: {},
      needs_review_modules: [],
      completed_a2_writing: []
    };
    allCourseModules = [];
    structuredCourseLevels.forEach(function (lvl) {
      (lvl.modules || []).forEach(function (m) {
        allCourseModules.push(m);
      });
    });

    updateTotalXP();
    renderQuestHeroBanner();
    renderQuestCardsGrid();
    renderCheatSheetModal();
    populateChatFocusSelector();
  });
}

function renderQuestHeroBanner() {
  const totalMastered = (courseProgress.mastered_modules || []).length;
  const totalMods = allCourseModules.length || 17;
  const pct = Math.round((totalMastered / totalMods) * 100);

  const countByLevel = lvl => {
    const mods = allCourseModules.filter(m => m.level === lvl);
    const done = mods.filter(m => (courseProgress.mastered_modules || []).includes(m.id)).length;
    return `${done}/${mods.length}`;
  };

  const html = `
    <div class="row align-items-center g-3">
      <div class="col-md-8">
        <div class="d-flex align-items-center gap-2 mb-1">
          <span class="badge bg-warning text-dark fs-6">🏆 Objectif : Oral B1 + Écrit A2 (Février)</span>
        </div>
        <h2 class="h3 fw-bold mb-1">Ta Carte d'Aventure avec Gemini !</h2>
        <p class="mb-2 opacity-90">
          Complète les 17 missions en parlant au micro. Obtiens au moins <strong>8/10</strong> au Défi du Boss pour gagner tes étoiles ⭐ !
        </p>
        <div class="bg-white bg-opacity-25 rounded-pill p-1 mb-2" style="max-width: 480px;">
          <div class="bg-warning rounded-pill text-dark fw-bold small px-3 py-1" style="width: ${Math.max(pct, 12)}%;">
            ${totalMastered}/${totalMods} Missions (${pct}%)
          </div>
        </div>
        <div class="d-flex flex-wrap gap-3 small fw-bold">
          <span>🌱 Niveau A1 : ${countByLevel("A1")}</span>
          <span>🚀 Niveau A2 : ${countByLevel("A2")}</span>
          <span>👑 Niveau B1 : ${countByLevel("B1")}</span>
        </div>
      </div>
      <div class="col-md-4 text-md-end">
        <button type="button" id="surprise-quest-btn" class="fun-btn fun-btn-yellow btn-lg">
          🎲 Mission Surprise !
        </button>
      </div>
    </div>
  `;
  $("#quest-hero-banner").html(html);
}

function renderQuestCardsGrid() {
  const $grid = $("#quest-cards-grid");
  $grid.empty();

  const list = selectedLevelFilter === "ALL"
    ? allCourseModules
    : allCourseModules.filter(m => m.level === selectedLevelFilter);

  list.forEach(function (m) {
    const isMastered = (courseProgress.mastered_modules || []).includes(m.id);
    const score = (courseProgress.module_scores || {})[m.id] || 0;
    const emoji = QUEST_EMOJIS[m.id] || "🎯";
    const stars = getStarsHtml(score, isMastered);

    const levelBadgeColor = m.level === "A1" ? "bg-info text-dark" : m.level === "A2" ? "bg-primary" : "bg-warning text-dark";

    const $card = $(`
      <div class="quest-card ${isMastered ? 'quest-mastered' : ''}" data-mod-id="${escapeHtml(m.id)}">
        <div>
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div class="quest-emoji-circle">${emoji}</div>
            <div class="text-end">
              <span class="badge ${levelBadgeColor} mb-1">${escapeHtml(m.code)}</span>
              <div class="stars-row">${stars}</div>
            </div>
          </div>
          <div class="small fw-bold text-primary text-uppercase mb-1">${escapeHtml(m.theme)}</div>
          <h3 class="h5 fw-bold mb-2">${escapeHtml(m.title)}</h3>
        </div>
        <div class="mt-3 pt-2 border-top d-flex justify-content-between align-items-center">
          <span class="small fw-bold ${isMastered ? 'text-success' : 'text-muted'}">
            ${isMastered ? `✅ Réussi (${score}/10)` : score ? `Essayé (${score}/10)` : 'Prêt à jouer !'}
          </span>
          <span class="fun-btn ${isMastered ? 'fun-btn-green' : 'fun-btn-blue'} py-1 px-3 small">
            ${isMastered ? 'Rejouer' : 'Jouer ➡️'}
          </span>
        </div>
      </div>
    `);

    $card.on("click", function () {
      openQuestMission(m.id, 1);
    });

    $grid.append($card);
  });
}

function openQuestMission(moduleId, stepNum) {
  activeQuestModuleId = moduleId;
  activeQuestStep = stepNum || 1;
  $("#quest-map-view").hide();
  $("#quest-lesson-view").show();
  renderActiveQuestStep();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderActiveQuestStep() {
  const mod = allCourseModules.find(m => m.id === activeQuestModuleId);
  if (!mod) return;

  const emoji = QUEST_EMOJIS[mod.id] || "🎯";
  const isMastered = (courseProgress.mastered_modules || []).includes(mod.id);
  const bestScore = (courseProgress.module_scores || {})[mod.id] || 0;
  const ref = mod.quick_refresher || {};

  let stepContentHtml = "";

  // STEP 1: LA RÈGLE MAGIQUE (SIMPLE & AUDIO)
  if (activeQuestStep === 1) {
    let examplesHtml = "";
    (mod.concepts || []).forEach(function (c) {
      let rulesBullets = (c.rules || []).map(r => `<li class="mb-2">${escapeHtml(r)}</li>`).join("");
      let exBubbles = (c.examples || []).map(ex => `
        <div class="example-bubble">
          <div>
            <div class="fw-bold fs-5 text-primary">${escapeHtml(ex.fr)}</div>
            <div class="text-muted">${escapeHtml(ex.en)}</div>
          </div>
          <button type="button" class="sound-circle-btn play-fr-btn" data-fr="${escapeHtml(ex.fr)}" title="Écouter">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      `).join("");

      examplesHtml += `
        <div class="mt-4">
          <h4 class="h5 fw-bold mb-2">📌 ${escapeHtml(c.title)}</h4>
          <p class="text-muted mb-2">${escapeHtml(c.explanation)}</p>
          <ul class="fw-bold">${rulesBullets}</ul>
          ${exBubbles}
        </div>
      `;
    });

    stepContentHtml = `
      <div class="magic-rule-box mb-4">
        <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-2">
          <h3 class="h5 fw-bold mb-0">🤖 Gemini t'explique le secret :</h3>
          <button type="button" class="fun-btn fun-btn-purple py-1 px-3 play-fr-btn" data-fr="${escapeHtml(mod.gemini_presentation)}">
            🔊 Écouter Gemini
          </button>
        </div>
        <p class="fs-5 mb-3">${escapeHtml(mod.gemini_presentation)}</p>
        <div class="bg-white text-dark p-3 rounded-4 border">
          <div class="small fw-bold text-uppercase text-primary mb-1">⚡ La Formule Magique à retenir :</div>
          <div class="fw-bold fs-5 mb-1">${escapeHtml(ref.formula || "")}</div>
          <div class="small text-muted">💡 <strong>Astuce :</strong> ${escapeHtml(ref.key_takeaway || "")}</div>
        </div>
      </div>

      ${examplesHtml}

      <div class="text-end mt-4 pt-3 border-top">
        <button type="button" class="fun-btn fun-btn-green btn-lg change-quest-step-btn" data-step="2">
          Étape 2 : Découvrir les Mots Audio 🃏 ➡️
        </button>
      </div>
    `;
  }

  // STEP 2: LES CARTES MOTS (TAP-TO-HEAR FLASHCARDS)
  else if (activeQuestStep === 2) {
    let cardsHtml = "";
    (mod.vocabulary || []).forEach(function (v) {
      const cleanFr = v.fr.split(" (")[0].split(" / ")[0].split(" (+")[0].trim();
      cardsHtml += `
        <div class="word-flashcard play-fr-btn" data-fr="${escapeHtml(cleanFr)}">
          <div class="mb-2">
            <span class="sound-circle-btn"><i class="fa-solid fa-volume-high"></i></span>
          </div>
          <div class="h5 fw-bold text-primary mb-1">${escapeHtml(v.fr)}</div>
          <div class="fw-bold text-muted mb-2">${escapeHtml(v.en)}</div>
          ${v.note ? `<span class="badge bg-light text-dark border">${escapeHtml(v.note)}</span>` : ""}
        </div>
      `;
    });

    stepContentHtml = `
      <div class="text-center mb-4">
        <h3 class="h4 fw-bold">🃏 Clique sur chaque carte pour écouter et répéter à voix haute !</h3>
        <p class="text-muted">Tu auras besoin de ces mots pour battre le Boss à l'étape 3.</p>
      </div>
      <div class="flashcard-grid mb-4">
        ${cardsHtml}
      </div>
      <div class="d-flex justify-content-between mt-4 pt-3 border-top">
        <button type="button" class="fun-btn fun-btn-gray change-quest-step-btn" data-step="1">
          ⬅️ Revoir la Règle
        </button>
        <button type="button" class="fun-btn fun-btn-red btn-lg change-quest-step-btn" data-step="3">
          Étape 3 : Défi Micro (Boss Final) 🎤 ➡️
        </button>
      </div>
    `;
  }

  // STEP 3: LE DÉFI DU BOSS (GIANT MICROPHONE + STRICT GRADING)
  else if (activeQuestStep === 3) {
    const oc = (mod.oral_challenges || [])[0] || {};
    const chipsHtml = (oc.mandatory_structures || [])
      .map(s => `<span class="word-badge-chip">✨ ${escapeHtml(s)}</span>`)
      .join("");

    let a2WritingHtml = "";
    if (mod.writing_task_a2) {
      const wt = mod.writing_task_a2;
      a2WritingHtml = `
        <div class="fun-card mt-4 border-primary">
          <h4 class="h5 fw-bold mb-2">✉️ Bonus Mission Écrit A2 (60–80 mots)</h4>
          <p class="mb-2">${escapeHtml(wt.prompt_fr)}</p>
          <textarea class="form-control mb-3" id="course-wt-input-${escapeHtml(mod.id)}" rows="3" placeholder="Écris ton petit message A2 ici..."></textarea>
          <button type="button" class="fun-btn fun-btn-blue evaluate-course-wt-btn" data-mod-id="${escapeHtml(mod.id)}" data-prompt="${escapeHtml(wt.prompt_fr)}">
            ✅ Vérifier mon message A2
          </button>
          <div id="course-wt-feedback-${escapeHtml(mod.id)}"></div>
        </div>
      `;
    }

    stepContentHtml = `
      <div class="boss-arena">
        <span class="badge bg-danger fs-6 mb-2">🔥 DÉFI DU BOSS — Obtiens au moins 8/10 pour gagner les étoiles !</span>
        <div class="d-flex justify-content-center align-items-center gap-2 my-2">
          <h3 class="h4 fw-bold mb-0">${escapeHtml(oc.title || "Parle en français !")}</h3>
          <button type="button" class="sound-circle-btn play-fr-btn" data-fr="${escapeHtml(oc.prompt_fr || "")}" title="Écouter la question">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>

        <p class="fs-5 my-3 mx-auto" style="max-width: 720px;">${escapeHtml(oc.prompt_fr || "")}</p>

        <div class="mb-4">
          <div class="small fw-bold text-uppercase text-muted mb-1">🎯 Mots magiques obligatoires à utiliser dans ta réponse :</div>
          ${chipsHtml}
        </div>

        <!-- Giant Microphone Button -->
        <div class="my-3">
          <button type="button" class="giant-mic-btn course-oral-record-btn" data-oc-id="${escapeHtml(oc.id)}">
            <i class="fa-solid fa-microphone"></i>
          </button>
          <div class="fw-bold mt-2" id="mic-status-label-${escapeHtml(oc.id)}">
            Clique sur le micro 🎤 pour parler en français !
          </div>
        </div>

        <div class="mx-auto my-3" style="max-width: 680px;">
          <textarea class="form-control rounded-4 p-3 fs-5 text-center" id="course-oral-input-${escapeHtml(oc.id)}" rows="3" placeholder="Ta réponse parlée s'affichera ici (tu peux aussi la corriger)..."></textarea>
        </div>

        <button type="button" class="fun-btn fun-btn-green btn-lg evaluate-course-oral-btn"
          data-oc-id="${escapeHtml(oc.id)}"
          data-mod-id="${escapeHtml(mod.id)}"
          data-prompt="${escapeHtml(oc.prompt_fr)}"
          data-mandatory='${escapeHtml(JSON.stringify(oc.mandatory_structures || []))}'>
          🚀 Vérifier ma Réponse (Objectif 8/10) !
        </button>

        <div id="course-oral-feedback-${escapeHtml(oc.id)}" class="text-start mt-4"></div>
      </div>

      ${a2WritingHtml}

      <div class="d-flex justify-content-between mt-4 pt-3 border-top">
        <button type="button" class="fun-btn fun-btn-gray change-quest-step-btn" data-step="2">
          ⬅️ Revoir les Mots
        </button>
        <button type="button" class="fun-btn fun-btn-purple go-chat-class-btn" data-class-id="${escapeHtml(mod.id)}">
          💬 S'entraîner en direct avec Renée sur cette mission
        </button>
      </div>
    `;
  }

  const html = `
    <div class="fun-card">
      <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3 pb-3 border-bottom">
        <button type="button" id="back-to-map-btn" class="fun-btn fun-btn-gray py-1 px-3">
          ⬅️ Retour à la Carte
        </button>
        <div class="text-center">
          <span class="badge bg-primary me-1">${escapeHtml(mod.code)}</span>
          <span class="fw-bold fs-5">${emoji} ${escapeHtml(mod.title)}</span>
        </div>
        <div class="stars-row">${getStarsHtml(bestScore, isMastered)}</div>
      </div>

      <!-- 3-Step Pill Bar -->
      <div class="stepper-bar">
        <button type="button" class="step-pill ${activeQuestStep === 1 ? 'active' : ''} change-quest-step-btn" data-step="1">
          1️⃣ Le Secret (La Règle)
        </button>
        <button type="button" class="step-pill ${activeQuestStep === 2 ? 'active' : ''} change-quest-step-btn" data-step="2">
          2️⃣ Les Cartes Mots 🔊
        </button>
        <button type="button" class="step-pill ${activeQuestStep === 3 ? 'active' : ''} change-quest-step-btn" data-step="3">
          3️⃣ Défi Micro (Boss) 🎤
        </button>
      </div>

      ${stepContentHtml}
    </div>
  `;

  $("#quest-lesson-view").html(html);
}

function renderFunEvaluationResult(ev, containerSelector) {
  if (!ev) return;
  const score = ev.score || 0;
  const passed = ev.passed !== undefined ? ev.passed : score >= 7;
  const stars = score >= 9 ? "⭐⭐⭐" : score >= 8 ? "⭐⭐☆" : score >= 6 ? "⭐☆☆" : "☆☆☆";

  const bannerBg = passed
    ? "background: #dcfce7; border: 3px solid #22c55e; color: #14532d;"
    : "background: #fef3c7; border: 3px solid #f59e0b; color: #78350f;";

  const html = `
    <div class="p-4 rounded-4 mt-3" style="${bannerBg}">
      <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
        <div>
          <div class="fs-3 fw-bold">${stars} ${passed ? "BRAVO ! MISSION RÉUSSIE !" : "PRESQUE ! CONTINUE COMME ÇA !"}</div>
          <div class="fw-bold">Ton Score : ${score} / 10 — ${escapeHtml(ev.verdict || "")}</div>
        </div>
        ${(ev.spoken_examiner_feedback_fr || ev.spoken_feedback_fr) ? `
          <button type="button" class="fun-btn fun-btn-blue play-fr-btn" data-fr="${escapeHtml(ev.spoken_examiner_feedback_fr || ev.spoken_feedback_fr)}">
            🔊 Réécouter la voix
          </button>
        ` : ""}
      </div>

      <div class="bg-white text-dark p-3 rounded-4 mb-3 border">
        <div class="small fw-bold text-success text-uppercase mb-1">✅ Comment le dire parfaitement en français :</div>
        <div class="d-flex justify-content-between align-items-center gap-2">
          <div class="fs-5 fw-bold text-primary">${escapeHtml(ev.corrected_french || "")}</div>
          <button type="button" class="sound-circle-btn play-fr-btn" data-fr="${escapeHtml(ev.corrected_french || "")}">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      </div>

      <div class="bg-white text-dark p-3 rounded-4 mb-3 border">
        <div class="small fw-bold text-primary text-uppercase mb-1">💡 Pourquoi ? (L'explication simple) :</div>
        <div>${escapeHtml(ev.strict_explanation_en || ev.explanation_en || "")}</div>
        ${ev.structures_used_check ? `<div class="small text-muted mt-1">🎯 <strong>Mots magiques :</strong> ${escapeHtml(ev.structures_used_check)}</div>` : ""}
      </div>

      ${(ev.model_answer_fr || ev.b1_upgrade_fr) ? `
        <div class="bg-white text-dark p-3 rounded-4 mb-3 border">
          <div class="small fw-bold text-uppercase mb-1" style="color: #7c3aed;">👑 Exemple de Champion B1 :</div>
          <div class="d-flex justify-content-between align-items-center gap-2">
            <div class="fw-bold">${escapeHtml(ev.model_answer_fr || ev.b1_upgrade_fr)}</div>
            <button type="button" class="sound-circle-btn play-fr-btn" data-fr="${escapeHtml(ev.model_answer_fr || ev.b1_upgrade_fr)}">
              <i class="fa-solid fa-volume-high"></i>
            </button>
          </div>
        </div>
      ` : ""}

      ${ev.follow_up_verification_question_fr ? `
        <div class="bg-white text-dark p-3 rounded-4 border d-flex justify-content-between align-items-center gap-2">
          <div>
            <div class="small fw-bold text-danger text-uppercase">🎤 Question Bonus pour vérifier que tu as tout compris :</div>
            <div class="fw-bold">${escapeHtml(ev.follow_up_verification_question_fr)}</div>
          </div>
          <button type="button" class="sound-circle-btn play-fr-btn" data-fr="${escapeHtml(ev.follow_up_verification_question_fr)}">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      ` : ""}
    </div>
  `;

  $(containerSelector).html(html);
}

// =========================================================
// 2. MES COURS 1-11 (NOTEBOOK CLASSES IN FUN GAME MODE)
// =========================================================

function loadCurriculumData() {
  $.get("/api/curriculum", function (data) {
    curriculumClasses = data.classes || [];
    b1Roadmap = data.roadmap || null;
    studyProgress = data.progress || { completed_exercises: [], completed_speaking: [], mastered_classes: [] };

    updateTotalXP();
    renderClassesGrid();
    populateChatFocusSelector();
  });
}

function renderClassesGrid() {
  const $grid = $("#classes-cards-grid");
  $grid.empty();

  curriculumClasses.forEach(function (cls, idx) {
    const emoji = CLASS_EMOJIS[idx % CLASS_EMOJIS.length];
    const $card = $(`
      <div class="quest-card" data-class-id="${escapeHtml(cls.id)}">
        <div>
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div class="quest-emoji-circle">${emoji}</div>
            <span class="badge bg-primary fs-6">Cours ${escapeHtml(cls.number)} • ${escapeHtml(cls.date)}</span>
          </div>
          <h3 class="h5 fw-bold mb-2">${escapeHtml(cls.title)}</h3>
          <p class="small text-muted mb-0">${escapeHtml(cls.summary)}</p>
        </div>
        <div class="mt-3 pt-2 border-top d-flex justify-content-between align-items-center">
          <span class="small fw-bold text-primary">
            ${(cls.written_exercises || []).length} quiz • ${(cls.speaking_prompts || []).length} défis micro
          </span>
          <span class="fun-btn fun-btn-blue py-1 px-3 small">Ouvrir ➡️</span>
        </div>
      </div>
    `);

    $card.on("click", function () {
      activeClassId = cls.id;
      activeClassStep = 1;
      $("#classes-grid-view").hide();
      $("#single-class-view").show();
      renderSingleClassStep();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    $grid.append($card);
  });
}

function renderSingleClassStep() {
  const cls = curriculumClasses.find(c => c.id === activeClassId);
  if (!cls) return;

  let bodyHtml = "";

  // STEP 1: LA RÈGLE DU COURS
  if (activeClassStep === 1) {
    let conceptsHtml = "";
    (cls.concepts || []).forEach(function (c) {
      const rules = (c.rules || []).map(r => `<li class="mb-2">${escapeHtml(r)}</li>`).join("");
      const exs = (c.examples || []).map(ex => `
        <div class="example-bubble">
          <div>
            <div class="fw-bold fs-5 text-primary">${escapeHtml(ex.fr)}</div>
            <div class="text-muted">${escapeHtml(ex.en)}</div>
          </div>
          <button type="button" class="sound-circle-btn play-fr-btn" data-fr="${escapeHtml(ex.fr)}">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      `).join("");

      conceptsHtml += `
        <div class="magic-rule-box mb-4">
          <h4 class="h5 fw-bold mb-2">💡 ${escapeHtml(c.title)}</h4>
          <p class="mb-2">${escapeHtml(c.explanation)}</p>
          <ul class="fw-bold">${rules}</ul>
          ${exs}
        </div>
      `;
    });

    bodyHtml = `
      ${conceptsHtml}
      <div class="text-end mt-3">
        <button type="button" class="fun-btn fun-btn-green btn-lg change-class-step-btn" data-step="2">
          Étape 2 : Écouter les Mots du Cours 🃏 ➡️
        </button>
      </div>
    `;
  }

  // STEP 2: LES MOTS DU COURS
  else if (activeClassStep === 2) {
    let cardsHtml = "";
    (cls.vocabulary || []).forEach(function (v) {
      const cleanFr = v.fr.split(" vs.")[0].split(" (")[0].trim();
      cardsHtml += `
        <div class="word-flashcard play-fr-btn" data-fr="${escapeHtml(cleanFr)}">
          <div class="mb-2"><span class="sound-circle-btn"><i class="fa-solid fa-volume-high"></i></span></div>
          <div class="h5 fw-bold text-primary mb-1">${escapeHtml(v.fr)}</div>
          <div class="fw-bold text-muted mb-2">${escapeHtml(v.en)}</div>
          ${v.note ? `<span class="badge bg-light text-dark border">${escapeHtml(v.note)}</span>` : ""}
        </div>
      `;
    });

    bodyHtml = `
      <div class="text-center mb-4">
        <h3 class="h4 fw-bold">🃏 Clique sur une carte pour entendre la prononciation !</h3>
      </div>
      <div class="flashcard-grid mb-4">${cardsHtml}</div>
      <div class="d-flex justify-content-between mt-4 pt-3 border-top">
        <button type="button" class="fun-btn fun-btn-gray change-class-step-btn" data-step="1">⬅️ Revoir la Règle</button>
        <button type="button" class="fun-btn fun-btn-red btn-lg change-class-step-btn" data-step="3">Étape 3 : Quiz &amp; Défi Micro 🎮 ➡️</button>
      </div>
    `;
  }

  // STEP 3: QUIZ & DÉFI MICRO
  else if (activeClassStep === 3) {
    let speakingHtml = "";
    (cls.speaking_prompts || []).forEach(function (sp) {
      const chips = (sp.target_structures || []).map(s => `<span class="word-badge-chip">✨ ${escapeHtml(s)}</span>`).join("");
      speakingHtml += `
        <div class="boss-arena mb-4">
          <span class="badge bg-danger fs-6 mb-2">🎤 DÉFI PARLER — Devoir &amp; Pratique Orale</span>
          <div class="d-flex justify-content-center align-items-center gap-2 my-2">
            <h4 class="h4 fw-bold mb-0">${escapeHtml(sp.title)}</h4>
            <button type="button" class="sound-circle-btn play-fr-btn" data-fr="${escapeHtml(sp.prompt_fr)}">
              <i class="fa-solid fa-volume-high"></i>
            </button>
          </div>
          <p class="fs-5 my-3 mx-auto" style="max-width: 700px;">${escapeHtml(sp.prompt_fr)}</p>
          <div class="mb-3">${chips}</div>

          <div class="my-3">
            <button type="button" class="giant-mic-btn oral-record-btn" data-sp-id="${escapeHtml(sp.id)}">
              <i class="fa-solid fa-microphone"></i>
            </button>
            <div class="fw-bold mt-2">Clique sur le micro 🎤 pour répondre à voix haute !</div>
          </div>

          <div class="mx-auto my-3" style="max-width: 660px;">
            <textarea class="form-control rounded-4 p-3 fs-5 text-center" id="oral-input-${escapeHtml(sp.id)}" rows="3" placeholder="Ta réponse en français..."></textarea>
          </div>

          <button type="button" class="fun-btn fun-btn-green btn-lg evaluate-oral-btn"
            data-sp-id="${escapeHtml(sp.id)}"
            data-class-id="${escapeHtml(cls.id)}"
            data-prompt="${escapeHtml(sp.prompt_fr)}">
            🚀 Vérifier ma Réponse avec Renée !
          </button>
          <div id="oral-feedback-${escapeHtml(sp.id)}" class="text-start mt-3"></div>
        </div>
      `;
    });

    let quizHtml = "";
    (cls.written_exercises || []).forEach(function (ex, idx) {
      quizHtml += `
        <div class="fun-card mb-3">
          <div class="badge bg-primary mb-2">Question ${idx + 1}</div>
          <p class="fs-5 fw-bold mb-1">${escapeHtml(ex.question)}</p>
          <p class="small text-muted mb-3">💡 Indice : ${escapeHtml(ex.hint || "")}</p>
          <div class="d-flex flex-wrap gap-2">
            <input type="text" class="form-control rounded-3" style="max-width: 380px;" id="written-input-${escapeHtml(ex.id)}" placeholder="Écris ta réponse ici...">
            <button type="button" class="fun-btn fun-btn-blue check-written-btn"
              data-ex-id="${escapeHtml(ex.id)}"
              data-answer="${escapeHtml(ex.answer)}"
              data-accepted='${escapeHtml(JSON.stringify(ex.accepted_answers || [ex.answer]))}'
              data-explanation="${escapeHtml(ex.explanation)}">
              ✅ Vérifier
            </button>
          </div>
          <div id="written-feedback-${escapeHtml(ex.id)}" class="mt-2"></div>
        </div>
      `;
    });

    bodyHtml = `
      ${speakingHtml}
      <div class="d-flex justify-content-between align-items-center mb-3 mt-4">
        <h3 class="h4 fw-bold mb-0">✍️ Mini-Quiz Rapide du Cours ${escapeHtml(cls.number)}</h3>
        <button type="button" id="generate-ai-exercises-btn" class="fun-btn fun-btn-purple py-1 px-3" data-class-id="${escapeHtml(cls.id)}">
          ✨ +3 Nouvelles Questions !
        </button>
      </div>
      ${quizHtml}
    `;
  }

  const html = `
    <div class="fun-card">
      <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3 pb-3 border-bottom">
        <button type="button" id="back-to-classes-btn" class="fun-btn fun-btn-gray py-1 px-3">
          ⬅️ Tous les Cours (1–11)
        </button>
        <h2 class="h4 fw-bold mb-0">🎒 Cours ${escapeHtml(cls.number)} : ${escapeHtml(cls.title)}</h2>
        <button type="button" class="fun-btn fun-btn-purple py-1 px-3 go-chat-class-btn" data-class-id="${escapeHtml(cls.id)}">
          💬 Parler de ce cours avec Renée
        </button>
      </div>

      <div class="stepper-bar">
        <button type="button" class="step-pill ${activeClassStep === 1 ? 'active' : ''} change-class-step-btn" data-step="1">
          1️⃣ La Règle Simple 💡
        </button>
        <button type="button" class="step-pill ${activeClassStep === 2 ? 'active' : ''} change-class-step-btn" data-step="2">
          2️⃣ Les Cartes Mots 🔊
        </button>
        <button type="button" class="step-pill ${activeClassStep === 3 ? 'active' : ''} change-class-step-btn" data-step="3">
          3️⃣ Défi Micro &amp; Quiz 🎮
        </button>
      </div>

      ${bodyHtml}
    </div>
  `;

  $("#single-class-view").html(html);
}

function renderCheatSheetModal() {
  let html = `<div class="quest-grid">`;
  allCourseModules.forEach(function (m) {
    const ref = m.quick_refresher || {};
    const emoji = QUEST_EMOJIS[m.id] || "⚡";
    html += `
      <div class="fun-card">
        <div class="badge bg-primary mb-2">${emoji} ${escapeHtml(m.code)} — ${escapeHtml(m.theme)}</div>
        <h4 class="h6 fw-bold mb-2">${escapeHtml(ref.rule_title || m.title)}</h4>
        <div class="p-2 rounded-3 bg-light text-primary fw-bold small mb-2 border">${escapeHtml(ref.formula || "")}</div>
        <p class="small text-muted mb-0">💡 ${escapeHtml(ref.key_takeaway || "")}</p>
      </div>
    `;
  });
  html += `</div>`;
  $("#cheatsheet-modal-body").html(html);
}

function populateChatFocusSelector() {
  const $chatSelect = $("#chat-focus-select");
  $chatSelect.html('<option value="">💬 Discussion libre avec Renée</option>');

  allCourseModules.forEach(function (m) {
    $chatSelect.append(`<option value="${escapeHtml(m.id)}">🗺️ Mission ${escapeHtml(m.code)} : ${escapeHtml(m.title)}</option>`);
  });

  curriculumClasses.forEach(function (cls) {
    $chatSelect.append(`<option value="${escapeHtml(cls.id)}">🎒 Cours ${escapeHtml(cls.number)} : ${escapeHtml(cls.title)}</option>`);
  });
}

// =========================================================
// 3. COMMON DAILY VERBS CONJUGATION & STARRED WORDS
// =========================================================

function loadVerbsAndStarredWords() {
  $.get("/api/verbs_and_starred", function (data) {
    commonDailyVerbs = data.verbs || [];
    starredWords = data.starred_words || [];
    $("#starred-words-count").text(starredWords.length);

    if (!activeVerbObj && commonDailyVerbs.length > 0) {
      activeVerbObj = commonDailyVerbs[0];
    }
    renderActiveVerbDetail(activeVerbObj);
    renderCommonVerbsGrid();
    renderStarredWordsPanel();
  });
}

function renderCommonVerbsGrid() {
  const $grid = $("#common-verbs-grid");
  $grid.empty();

  const filtered = selectedVerbCategory === "ALL"
    ? commonDailyVerbs
    : commonDailyVerbs.filter(v => v.category === selectedVerbCategory);

  filtered.forEach(function (v) {
    const isActive = activeVerbObj && activeVerbObj.verb === v.verb ? "verb-card-active" : "";
    const auxBadge = v.auxiliary === "être" ? "bg-danger" : "bg-primary";
    const $card = $(`
      <div class="word-flashcard ${isActive}" data-verb="${escapeHtml(v.verb)}">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <span class="fs-3">${v.emoji || "⚡"}</span>
          <span class="badge ${auxBadge}">Aux: ${escapeHtml(v.auxiliary)} (${escapeHtml(v.past_participle)})</span>
        </div>
        <div class="h4 fw-bold text-primary mb-1">${escapeHtml(v.verb)}</div>
        <div class="small fw-bold text-muted">${escapeHtml(v.en)}</div>
      </div>
    `);
    $card.on("click", function () {
      activeVerbObj = v;
      renderActiveVerbDetail(v);
      renderCommonVerbsGrid();
      document.getElementById("active-verb-detail").scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
    $grid.append($card);
  });
}

function renderActiveVerbDetail(v) {
  const $detail = $("#active-verb-detail");
  if (!v) {
    $detail.empty();
    return;
  }

  let tensesHtml = "";
  const tensesObj = v.tenses || {};
  Object.keys(tensesObj).forEach(function (tenseName) {
    const formsList = (tensesObj[tenseName] || [])
      .map(line => `<div class="py-1 border-bottom small fw-bold">${escapeHtml(line)}</div>`)
      .join("");
    tensesHtml += `
      <div class="tense-box">
        <div class="tense-title">${escapeHtml(tenseName)}</div>
        ${formsList}
      </div>
    `;
  });

  let examplesHtml = "";
  (v.examples || []).forEach(function (ex) {
    examplesHtml += `
      <div class="example-bubble">
        <div>
          <div class="fw-bold text-primary">${escapeHtml(ex.fr)}</div>
          <div class="small text-muted">${escapeHtml(ex.en)}</div>
        </div>
        <button type="button" class="sound-circle-btn play-fr-btn" data-fr="${escapeHtml(ex.fr)}" title="Écouter">
          <i class="fa-solid fa-volume-high"></i>
        </button>
      </div>
    `;
  });

  const auxBadge = v.auxiliary === "être" ? "bg-danger" : "bg-primary";
  const html = `
    <div class="fun-card border-primary">
      <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3 pb-3 border-bottom">
        <div class="d-flex align-items-center gap-3">
          <div class="quest-emoji-circle">${v.emoji || "⚡"}</div>
          <div>
            <div class="d-flex align-items-center gap-2">
              <h3 class="h3 fw-bold text-primary mb-0">${escapeHtml(v.verb)}</h3>
              <button type="button" class="sound-circle-btn play-fr-btn" data-fr="${escapeHtml(v.verb)}" title="Écouter le verbe">
                <i class="fa-solid fa-volume-high"></i>
              </button>
              <span class="badge ${auxBadge} fs-6">Auxiliaire : ${escapeHtml(v.auxiliary)} • Participe passé : ${escapeHtml(v.past_participle)}</span>
            </div>
            <div class="fw-bold text-muted fs-5">${escapeHtml(v.en)}</div>
          </div>
        </div>
      </div>

      ${v.tip ? `
        <div class="magic-rule-box mb-3 py-2 px-3">
          <strong>💡 Astuce :</strong> ${escapeHtml(v.tip)}
        </div>
      ` : ""}

      <div class="tense-grid mb-3">
        ${tensesHtml}
      </div>

      <h4 class="h6 fw-bold mt-3 mb-2">🗣️ Phrases du quotidien :</h4>
      ${examplesHtml}
    </div>
  `;

  $detail.html(html);
}

function renderStarredWordsPanel() {
  const $container = $("#starred-words-container");
  $("#starred-words-count").text(starredWords.length);

  if (starredWords.length === 0) {
    $container.html(`
      <div class="fun-card text-center py-5" style="grid-column: 1 / -1;">
        <div class="display-4 mb-2">⭐</div>
        <h3 class="h4 fw-bold">Aucun mot favori pour l'instant !</h3>
        <p class="text-muted mb-0">
          Fais un <strong>clic droit</strong> sur n'importe quel mot français dans l'application, puis clique sur <strong>⭐ Favori</strong> pour le sauvegarder ici.
        </p>
      </div>
    `);
    return;
  }

  $container.empty();
  starredWords.forEach(function (entry) {
    const forms = entry.forms || {};
    let formsPreviewHtml = "";
    if (entry.is_verb && forms.tenses && forms.tenses["Présent"]) {
      formsPreviewHtml = `
        <div class="small bg-light text-dark p-2 rounded-3 border mb-2">
          <div><strong>Infinitif :</strong> ${escapeHtml(forms.infinitive || entry.lemma)} (Aux: ${escapeHtml(forms.auxiliary || "avoir")}, PP: ${escapeHtml(forms.past_participle || "")})</div>
          <div class="mt-1"><strong>Présent :</strong> ${(forms.tenses["Présent"] || []).map(escapeHtml).join(" • ")}</div>
          ${forms.tenses["Passé Composé"] ? `<div class="mt-1"><strong>Passé Composé :</strong> ${(forms.tenses["Passé Composé"] || []).slice(0, 3).map(escapeHtml).join(" • ")}...</div>` : ""}
          ${forms.tenses["Imparfait"] ? `<div class="mt-1"><strong>Imparfait :</strong> ${(forms.tenses["Imparfait"] || []).slice(0, 3).map(escapeHtml).join(" • ")}...</div>` : ""}
        </div>
      `;
    } else {
      formsPreviewHtml = `
        <div class="small bg-light text-dark p-2 rounded-3 border mb-2">
          ${forms.masculine_singular ? `<div><strong>Masc. :</strong> ${escapeHtml(forms.masculine_singular)}</div>` : ""}
          ${forms.feminine_singular ? `<div><strong>Fém. :</strong> ${escapeHtml(forms.feminine_singular)}</div>` : ""}
          ${forms.plural ? `<div><strong>Pluriel :</strong> ${escapeHtml(forms.plural)}</div>` : ""}
          ${(forms.related_family && forms.related_family.length) ? `<div><strong>Famille :</strong> ${forms.related_family.map(escapeHtml).join(", ")}</div>` : ""}
        </div>
      `;
    }

    let exHtml = "";
    (entry.examples || []).forEach(function (ex) {
      exHtml += `
        <div class="example-bubble py-2 px-3">
          <div class="small">
            <div class="fw-bold text-primary">${escapeHtml(ex.fr)}</div>
            <div class="text-muted">${escapeHtml(ex.en)}</div>
          </div>
          <button type="button" class="sound-circle-btn play-fr-btn" style="width: 34px; height: 34px;" data-fr="${escapeHtml(ex.fr)}">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      `;
    });

    const $card = $(`
      <div class="fun-card d-flex flex-column justify-content-between">
        <div>
          <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
            <div>
              <span class="badge bg-primary mb-1">${escapeHtml(entry.part_of_speech || "Mot")}</span>
              <h3 class="h4 fw-bold text-primary mb-0">
                ${escapeHtml(entry.lemma || entry.word)}
                ${entry.word && entry.lemma && entry.word.toLowerCase() !== entry.lemma.toLowerCase()
                  ? `<span class="small text-muted fw-normal">(${escapeHtml(entry.word)})</span>`
                  : ""}
              </h3>
            </div>
            <div class="d-flex gap-1">
              <button type="button" class="sound-circle-btn play-fr-btn" data-fr="${escapeHtml(entry.lemma || entry.word)}" title="Écouter">
                <i class="fa-solid fa-volume-high"></i>
              </button>
              <button type="button" class="star-word-btn starred remove-star-btn" data-entry='${escapeHtml(JSON.stringify(entry))}' title="Retirer des favoris">
                ⭐
              </button>
            </div>
          </div>

          <div class="fw-bold fs-5 mb-2">🇬🇧 ${escapeHtml(entry.english_meaning || "")}</div>
          ${entry.grammar_tip ? `<p class="small text-muted mb-2">💡 ${escapeHtml(entry.grammar_tip)}</p>` : ""}
          ${formsPreviewHtml}
          ${exHtml}
        </div>
      </div>
    `);
    $container.append($card);
  });
}

// =========================================================
// 4. RIGHT-CLICK SMART DICTIONARY POPUP (ANYWHERE ON PAGE)
// =========================================================

function extractWordAtPoint(clientX, clientY) {
  // 1. If user highlighted text, use selection
  const sel = window.getSelection();
  if (sel && sel.toString().trim().length > 0 && sel.toString().trim().length < 45) {
    const selectedText = sel.toString().trim();
    const anchorText = sel.anchorNode && sel.anchorNode.textContent ? sel.anchorNode.textContent.trim() : "";
    return { word: selectedText, context: anchorText.slice(0, 220) };
  }

  // 2. Otherwise detect exact word under the mouse cursor
  let range = null;
  let textNode = null;
  let offset = 0;

  if (document.caretRangeFromPoint) {
    range = document.caretRangeFromPoint(clientX, clientY);
    if (range) {
      textNode = range.startContainer;
      offset = range.startOffset;
    }
  } else if (document.caretPositionFromPoint) {
    const pos = document.caretPositionFromPoint(clientX, clientY);
    if (pos) {
      textNode = pos.offsetNode;
      offset = pos.offset;
    }
  }

  if (!textNode || textNode.nodeType !== Node.TEXT_NODE) {
    return null;
  }

  const text = textNode.textContent || "";
  if (!text.trim()) return null;

  const isWordChar = ch => /[a-zA-ZÀ-ÿœŒæÆ'-]/.test(ch);
  let start = offset;
  let end = offset;

  while (start > 0 && isWordChar(text[start - 1])) start--;
  while (end < text.length && isWordChar(text[end])) end++;

  let word = text.slice(start, end).replace(/^['-]+|['-]+$/g, "");
  // Strip leading contraction like l', d', j', qu', n', s', m', t', c'
  word = word.replace(/^(l'|d'|j'|qu'|n'|s'|m'|t'|c')/i, "");

  if (!word || word.length < 2) return null;
  return { word: word, context: text.trim().slice(0, 220) };
}

function positionPopoverNearCursor(clientX, clientY) {
  const $pop = $("#smart-dict-popover");
  $pop.show();
  const popWidth = $pop.outerWidth() || 420;
  const popHeight = Math.min($pop.outerHeight() || 380, window.innerHeight * 0.8);

  let left = clientX + 12;
  let top = clientY + 12;

  if (left + popWidth > window.innerWidth - 16) {
    left = Math.max(12, window.innerWidth - popWidth - 16);
  }
  if (top + popHeight > window.innerHeight - 16) {
    top = Math.max(12, window.innerHeight - popHeight - 16);
  }

  $pop.css({ left: left + "px", top: top + "px" });
}

function renderSmartDictionaryPopoverContent(entry, isStarred) {
  lastDictLookupEntry = entry;
  const forms = entry.forms || {};
  let formsHtml = "";

  if (entry.is_verb && forms.tenses) {
    let tensesBlocks = "";
    ["Présent", "Passé Composé", "Imparfait", "Futur Simple", "Conditionnel"].forEach(function (tName) {
      if (forms.tenses[tName]) {
        tensesBlocks += `
          <div class="p-2 rounded-3 bg-light text-dark border small">
            <div class="fw-bold text-primary border-bottom pb-1 mb-1">${escapeHtml(tName)}</div>
            ${forms.tenses[tName].map(l => `<div>${escapeHtml(l)}</div>`).join("")}
          </div>
        `;
      }
    });
    formsHtml = `
      <div class="mb-3">
        <div class="small fw-bold text-uppercase text-muted mb-1">
          🔄 Conjugaison (${escapeHtml(forms.infinitive || entry.lemma)} • Aux: ${escapeHtml(forms.auxiliary || "avoir")} • PP: ${escapeHtml(forms.past_participle || "")}) :
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(165px, 1fr)); gap: 0.5rem;">
          ${tensesBlocks}
        </div>
      </div>
    `;
  } else {
    formsHtml = `
      <div class="p-2 rounded-3 bg-light text-dark border small mb-3">
        <div class="fw-bold text-primary mb-1">🔄 Toutes les formes du mot :</div>
        ${forms.masculine_singular ? `<div><strong>Masculin :</strong> ${escapeHtml(forms.masculine_singular)}</div>` : ""}
        ${forms.feminine_singular ? `<div><strong>Féminin :</strong> ${escapeHtml(forms.feminine_singular)}</div>` : ""}
        ${forms.plural ? `<div><strong>Pluriel :</strong> ${escapeHtml(forms.plural)}</div>` : ""}
        ${(forms.related_family && forms.related_family.length) ? `<div><strong>Mots de la même famille :</strong> ${forms.related_family.map(escapeHtml).join(", ")}</div>` : ""}
      </div>
    `;
  }

  let examplesHtml = "";
  (entry.examples || []).forEach(function (ex) {
    examplesHtml += `
      <div class="example-bubble py-2 px-3">
        <div class="small">
          <div class="fw-bold text-primary">${escapeHtml(ex.fr)}</div>
          <div class="text-muted">${escapeHtml(ex.en)}</div>
        </div>
        <button type="button" class="sound-circle-btn play-fr-btn" style="width: 34px; height: 34px;" data-fr="${escapeHtml(ex.fr)}">
          <i class="fa-solid fa-volume-high"></i>
        </button>
      </div>
    `;
  });

  const html = `
    <div class="d-flex justify-content-between align-items-start gap-2 mb-2 pb-2 border-bottom">
      <div>
        <span class="badge bg-primary mb-1">${escapeHtml(entry.part_of_speech || "Dictionnaire")}</span>
        <div class="d-flex align-items-center gap-2">
          <h4 class="h4 fw-bold text-primary mb-0">${escapeHtml(entry.word)}</h4>
          ${entry.lemma && entry.lemma.toLowerCase() !== entry.word.toLowerCase()
            ? `<span class="badge bg-light text-dark border">Base : ${escapeHtml(entry.lemma)}</span>`
            : ""}
          <button type="button" class="sound-circle-btn play-fr-btn" style="width: 34px; height: 34px;" data-fr="${escapeHtml(entry.word)}" title="Écouter">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      </div>

      <div class="d-flex align-items-center gap-1">
        <button type="button" id="popover-star-btn" class="star-word-btn ${isStarred ? 'starred' : ''}" title="Sauvegarder dans Mes Mots Favoris">
          ${isStarred ? "⭐ Favori !" : "☆ Favori"}
        </button>
        <button type="button" id="close-dict-popover-btn" class="btn-close ms-1" aria-label="Fermer"></button>
      </div>
    </div>

    <div class="fw-bold fs-5 mb-2">🇬🇧 ${escapeHtml(entry.english_meaning || "")}</div>
    ${entry.grammar_tip ? `<div class="small text-muted mb-2">💡 <strong>Astuce :</strong> ${escapeHtml(entry.grammar_tip)}</div>` : ""}

    ${formsHtml}

    <div class="small fw-bold text-uppercase text-muted mb-1">💬 Exemples en phrase :</div>
    ${examplesHtml}
  `;

  $("#smart-dict-content").html(html);
}

// =========================================================
// DOCUMENT READY & EVENT HANDLERS
// =========================================================

$(document).ready(function () {
  var currentLanguageIndex = 0;
  var prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
  var darkMode = prefersDarkScheme.matches;

  setDarkMode(darkMode);
  loadStructuredCourseData();
  loadCurriculumData();
  loadVerbsAndStarredWords();

  // =========================================================
  // RIGHT-CLICK SMART DICTIONARY EVENT HANDLERS
  // =========================================================
  $(document).on("contextmenu", function (e) {
    // Allow normal right-click inside text inputs/textareas unless text is selected
    if ($(e.target).is("input, textarea") && !window.getSelection().toString().trim()) {
      return;
    }
    const found = extractWordAtPoint(e.clientX, e.clientY);
    if (!found || !found.word) return;

    e.preventDefault();
    $("#smart-dict-content").html(`
      <div class="text-center py-3">
        <div class="fs-3 mb-1"><i class="fa-solid fa-spinner fa-spin text-primary"></i></div>
        <div class="fw-bold">📖 Recherche de « ${escapeHtml(found.word)} »...</div>
        <div class="small text-muted">Traduction, formes, conjugaison &amp; exemples</div>
      </div>
    `);
    positionPopoverNearCursor(e.clientX, e.clientY);

    $.post("/api/dictionary_lookup", { word: found.word, context: found.context }, function (res) {
      if (res.error || !res.entry) {
        $("#smart-dict-content").html(`
          <div class="d-flex justify-content-between align-items-center">
            <span class="text-danger fw-bold">${escapeHtml(res.error || "Mot introuvable")}</span>
            <button type="button" id="close-dict-popover-btn" class="btn-close"></button>
          </div>
        `);
        return;
      }
      renderSmartDictionaryPopoverContent(res.entry, res.is_starred);
      positionPopoverNearCursor(e.clientX, e.clientY);
    });
  });

  $(document).on("click", "#close-dict-popover-btn", function () {
    $("#smart-dict-popover").hide();
  });

  // Close popover when clicking outside
  $(document).on("mousedown", function (e) {
    const $pop = $("#smart-dict-popover");
    if ($pop.is(":visible") && !$(e.target).closest("#smart-dict-popover").length && e.button === 0) {
      $pop.hide();
    }
  });

  // Star / Unstar word inside Right-Click Popover
  $(document).on("click", "#popover-star-btn", function () {
    if (!lastDictLookupEntry) return;
    const $btn = $(this);
    $.post("/api/toggle_star_word", { entry_json: JSON.stringify(lastDictLookupEntry) }, function (res) {
      starredWords = res.starred_words || [];
      renderStarredWordsPanel();
      if (res.starred) {
        $btn.addClass("starred").text("⭐ Favori !");
      } else {
        $btn.removeClass("starred").text("☆ Favori");
      }
    });
  });

  // Remove Starred word from Starred Words Panel
  $(document).on("click", ".remove-star-btn", function () {
    const rawEntry = $(this).attr("data-entry");
    $.post("/api/toggle_star_word", { entry_json: rawEntry }, function (res) {
      starredWords = res.starred_words || [];
      renderStarredWordsPanel();
    });
  });

  // Verbs & Starred Words Sub-Tabs
  $(document).on("click", ".verbs-subtab-btn", function () {
    const subtab = $(this).attr("data-subtab");
    $(".verbs-subtab-btn").removeClass("active");
    $(this).addClass("active");
    if (subtab === "verbs-panel") {
      $("#starred-panel").hide();
      $("#verbs-panel").show();
    } else {
      $("#verbs-panel").hide();
      $("#starred-panel").show();
      renderStarredWordsPanel();
    }
  });

  // Filter Common Daily Verbs by Category
  $(document).on("click", ".verb-cat-pill", function () {
    $(".verb-cat-pill").removeClass("active");
    $(this).addClass("active");
    selectedVerbCategory = $(this).attr("data-cat");
    renderCommonVerbsGrid();
  });

  // Conjugate any custom verb via AI Search Box
  $("#conjugate-custom-verb-btn").on("click", function () {
    const query = ($("#custom-verb-input").val() || "").trim();
    if (!query) {
      showNotification("Écris un verbe à conjuguer (ex: courir, finir, dormir) !");
      return;
    }
    const $btn = $(this);
    const orig = $btn.html();
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin"></i>');

    $.post("/api/conjugate_verb", { verb: query }, function (res) {
      $btn.prop("disabled", false).html(orig);
      if (res.error || !res.verb_data) {
        showNotification(res.error || "Impossible de conjuguer ce verbe.");
        return;
      }
      $("#starred-panel").hide();
      $("#verbs-panel").show();
      activeVerbObj = res.verb_data;
      renderActiveVerbDetail(activeVerbObj);
    }).fail(function () {
      $btn.prop("disabled", false).html(orig);
    });
  });

  $("#custom-verb-input").on("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      $("#conjugate-custom-verb-btn").click();
    }
  });

  // Top 3 Main Navigation Buttons
  $(document).on("click", ".fun-tab-btn", function () {
    switchTab($(this).data("tab"));
  });

  // Level Filter Pills (All / A1 / A2 / B1)
  $(document).on("click", ".level-pill", function () {
    $(".level-pill").removeClass("active");
    $(this).addClass("active");
    selectedLevelFilter = $(this).data("level");
    renderQuestCardsGrid();
  });

  // Back to Map / Back to Classes
  $(document).on("click", "#back-to-map-btn", function () {
    $("#quest-lesson-view").hide();
    $("#quest-map-view").show();
    renderQuestHeroBanner();
    renderQuestCardsGrid();
  });

  $(document).on("click", "#back-to-classes-btn", function () {
    $("#single-class-view").hide();
    $("#classes-grid-view").show();
  });

  // Change Step inside Quest Player or Class Player
  $(document).on("click", ".change-quest-step-btn", function () {
    activeQuestStep = parseInt($(this).attr("data-step"), 10);
    renderActiveQuestStep();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  $(document).on("click", ".change-class-step-btn", function () {
    activeClassStep = parseInt($(this).attr("data-step"), 10);
    renderSingleClassStep();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Surprise Quest Button
  $(document).on("click", "#surprise-quest-btn", function () {
    if (allCourseModules.length === 0) return;
    const randomMod = allCourseModules[Math.floor(Math.random() * allCourseModules.length)];
    openQuestMission(randomMod.id, 3);
  });

  // Play French Audio on any Card or Button
  $(document).on("click", ".play-fr-btn", function (e) {
    e.stopPropagation();
    const frText = $(this).attr("data-fr");
    speakFrenchText(frText, $(this).hasClass("word-flashcard") ? null : this);
  });

  // Cheat-Sheet Modal ("⚡ Astuces")
  const cheatsheetDialog = document.getElementById("cheatsheet-dialog");
  $("#open-cheatsheet-btn").on("click", function () {
    if (cheatsheetDialog && cheatsheetDialog.showModal) {
      cheatsheetDialog.showModal();
    }
  });
  $("#close-cheatsheet-btn").on("click", function () {
    if (cheatsheetDialog && cheatsheetDialog.close) {
      cheatsheetDialog.close();
    }
  });

  // Jump to Live Chat with Renée on any topic
  $(document).on("click", ".go-chat-class-btn", function () {
    const focusId = $(this).attr("data-class-id");
    $("#chat-focus-select").val(focusId);
    switchTab("tab-practice");
    startFocusedChat(focusId);
  });

  $("#apply-chat-focus-btn").on("click", function () {
    startFocusedChat($("#chat-focus-select").val());
  });

  $("#begin-chat-btn").on("click", function () {
    initChat();
  });

  // Record Microphone in Quest Boss Arena
  $(document).on("click", ".course-oral-record-btn", function () {
    const $btn = $(this);
    const ocId = $btn.attr("data-oc-id");
    const $label = $(`#mic-status-label-${ocId}`);
    initAudio();

    if (activeOralRecordingId === ocId) {
      activeOralRecordingId = null;
      $btn.removeClass("recording").prop("disabled", true);
      $label.text("⏳ Gemini écoute et écrit ce que tu as dit...");
      stopRecording();
      activeOralBlobPromise.then(blob => {
        uploadAudio(blob).then(filename => {
          $.post("/transcribe_recording", { filename: filename }, function (res) {
            $btn.prop("disabled", false);
            $label.text("🎤 Clique sur le micro si tu veux ajouter une phrase !");
            if (res.error) showNotification(res.error);
            if (res.recorded_text) {
              const $input = $(`#course-oral-input-${ocId}`);
              const existing = $input.val().trim();
              $input.val(existing ? existing + " " + res.recorded_text : res.recorded_text);
            }
          });
        });
      });
    } else {
      activeOralRecordingId = ocId;
      $btn.addClass("recording");
      $label.text("🔴 Enregistrement en cours... Parle maintenant, puis reclique pour arrêter !");
      activeOralBlobPromise = startRecording();
    }
  });

  // Evaluate Quest Boss Challenge
  $(document).on("click", ".evaluate-course-oral-btn", function () {
    const $btn = $(this);
    const ocId = $btn.attr("data-oc-id");
    const modId = $btn.attr("data-mod-id");
    const promptText = $btn.attr("data-prompt");
    const mandatoryRaw = $btn.attr("data-mandatory") || "[]";
    const userVal = ($(`#course-oral-input-${ocId}`).val() || "").trim();

    if (!userVal) {
      showNotification("Clique sur le micro rouge 🎤 pour parler en français d'abord !");
      return;
    }

    initAudio();
    const origHtml = $btn.html();
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin me-2"></i> Gemini vérifie ta réponse...');

    $.post("/api/evaluate_course_challenge", {
      module_id: modId,
      prompt_text: promptText,
      user_answer: userVal,
      mandatory_structures: mandatoryRaw,
      is_writing_a2: 0
    }, function (res) {
      $btn.prop("disabled", false).html(origHtml);
      if (res.error) {
        showNotification(res.error);
        return;
      }
      if (res.progress) {
        courseProgress = res.progress;
        updateTotalXP();
      }
      renderFunEvaluationResult(res.evaluation, `#course-oral-feedback-${ocId}`);
      if (res.audio_url) {
        playSingleAudioFile(res.audio_url);
      }
    }).fail(function () {
      $btn.prop("disabled", false).html(origHtml);
    });
  });

  // Evaluate A2 Writing Bonus Mission
  $(document).on("click", ".evaluate-course-wt-btn", function () {
    const $btn = $(this);
    const modId = $btn.attr("data-mod-id");
    const promptText = $btn.attr("data-prompt");
    const userVal = ($(`#course-wt-input-${modId}`).val() || "").trim();

    if (!userVal) {
      showNotification("Écris ton petit message A2 d'abord !");
      return;
    }

    const origHtml = $btn.html();
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin me-2"></i> Vérification...');

    $.post("/api/evaluate_course_challenge", {
      module_id: modId,
      prompt_text: promptText,
      user_answer: userVal,
      mandatory_structures: "[]",
      is_writing_a2: 1
    }, function (res) {
      $btn.prop("disabled", false).html(origHtml);
      if (res.error) {
        showNotification(res.error);
        return;
      }
      if (res.progress) {
        courseProgress = res.progress;
        updateTotalXP();
      }
      renderFunEvaluationResult(res.evaluation, `#course-wt-feedback-${modId}`);
    }).fail(function () {
      $btn.prop("disabled", false).html(origHtml);
    });
  });

  // Record Microphone in Class 1-11 Speaking Challenge
  $(document).on("click", ".oral-record-btn", function () {
    const $btn = $(this);
    const spId = $btn.attr("data-sp-id");
    initAudio();

    if (activeOralRecordingId === spId) {
      activeOralRecordingId = null;
      $btn.removeClass("recording").prop("disabled", true);
      stopRecording();
      activeOralBlobPromise.then(blob => {
        uploadAudio(blob).then(filename => {
          $.post("/transcribe_recording", { filename: filename }, function (res) {
            $btn.prop("disabled", false);
            if (res.error) showNotification(res.error);
            if (res.recorded_text) {
              const $input = $(`#oral-input-${spId}`);
              const existing = $input.val().trim();
              $input.val(existing ? existing + " " + res.recorded_text : res.recorded_text);
            }
          });
        });
      });
    } else {
      activeOralRecordingId = spId;
      $btn.addClass("recording");
      activeOralBlobPromise = startRecording();
    }
  });

  // Evaluate Class 1-11 Speaking Challenge
  $(document).on("click", ".evaluate-oral-btn", function () {
    const $btn = $(this);
    const spId = $btn.attr("data-sp-id");
    const classId = $btn.attr("data-class-id");
    const promptText = $btn.attr("data-prompt");
    const userVal = ($(`#oral-input-${spId}`).val() || "").trim();

    if (!userVal) {
      showNotification("Clique sur le micro 🎤 pour parler d'abord !");
      return;
    }

    initAudio();
    const origHtml = $btn.html();
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin me-2"></i> Renée écoute ta réponse...');

    $.post("/api/evaluate_exercise", {
      class_id: classId,
      item_id: spId,
      prompt_text: promptText,
      user_answer: userVal,
      mode: "speaking"
    }, function (res) {
      $btn.prop("disabled", false).html(origHtml);
      if (res.error) {
        showNotification(res.error);
        return;
      }
      if (res.progress) {
        studyProgress = res.progress;
        updateTotalXP();
      }
      renderFunEvaluationResult(res.evaluation, `#oral-feedback-${spId}`);
      if (res.audio_url) {
        playSingleAudioFile(res.audio_url);
      }
    }).fail(function () {
      $btn.prop("disabled", false).html(origHtml);
    });
  });

  // Check Mini-Quiz Question in Classes 1-11
  $(document).on("click", ".check-written-btn", function () {
    const exId = $(this).attr("data-ex-id");
    const expected = $(this).attr("data-answer");
    const explanation = $(this).attr("data-explanation");
    let accepted = [];
    try {
      accepted = JSON.parse($(this).attr("data-accepted") || "[]");
    } catch (e) {
      accepted = [expected];
    }

    const userVal = ($(`#written-input-${exId}`).val() || "").trim();
    if (!userVal) {
      showNotification("Écris ta réponse d'abord !");
      return;
    }

    const normalize = s => s.toLowerCase().replace(/[.!?]/g, "").replace(/\s+/g, " ").trim();
    const isMatch = accepted.some(a => normalize(a) === normalize(userVal)) || normalize(expected) === normalize(userVal);

    if (isMatch) {
      $.post("/api/mark_progress", { category: "completed_exercises", item_id: exId }, function (res) {
        if (res.progress) {
          studyProgress = res.progress;
          updateTotalXP();
        }
      });
      $(`#written-feedback-${exId}`).html(`
        <div class="p-3 rounded-4 mt-2" style="background: #dcfce7; border: 2px solid #22c55e; color: #14532d;">
          <div class="fw-bold">🎉 Super ! C'est exactement ça : ${escapeHtml(expected)} (+20 XP)</div>
          <div class="small mt-1">${escapeHtml(explanation)}</div>
        </div>
      `);
    } else {
      $(`#written-feedback-${exId}`).html(`
        <div class="p-3 rounded-4 mt-2" style="background: #fef3c7; border: 2px solid #f59e0b; color: #78350f;">
          <div class="fw-bold">💡 Presque ! La bonne réponse est : <u>${escapeHtml(expected)}</u></div>
          <div class="small mt-1">${escapeHtml(explanation)}</div>
        </div>
      `);
    }
  });

  // Generate 3 New Quiz Questions with AI
  $(document).on("click", "#generate-ai-exercises-btn", function () {
    const $btn = $(this);
    const classId = $btn.attr("data-class-id");
    const cls = curriculumClasses.find(c => c.id === classId);
    if (!cls) return;

    const orig = $btn.html();
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin me-1"></i> Création...');

    $.post("/api/generate_exercises", { class_id: classId }, function (res) {
      $btn.prop("disabled", false).html(orig);
      if (res.generated && res.generated.written_exercises) {
        cls.written_exercises = (cls.written_exercises || []).concat(res.generated.written_exercises);
        renderSingleClassStep();
      }
    }).fail(function () {
      $btn.prop("disabled", false).html(orig);
    });
  });

  // Import New Class PDF Dialog
  const importDialog = document.getElementById("import-class-dialog");
  $("#open-import-modal-btn").on("click", function () {
    $("#import-class-number").val(curriculumClasses.length + 1);
    if (importDialog && importDialog.showModal) importDialog.showModal();
  });
  $("#close-import-dialog-btn, #cancel-import-btn").on("click", function () {
    if (importDialog && importDialog.close) importDialog.close();
  });

  $("#import-class-form").on("submit", function (e) {
    e.preventDefault();
    const $submitBtn = $("#submit-import-btn");
    const origHtml = $submitBtn.html();
    $submitBtn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin me-1"></i> Magie en cours...');

    const formData = new FormData(this);
    $.ajax({
      url: "/api/import_class",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (res) {
        $submitBtn.prop("disabled", false).html(origHtml);
        if (res.error) {
          showNotification(res.error);
          return;
        }
        if (res.classes) curriculumClasses = res.classes;
        if (importDialog && importDialog.close) importDialog.close();
        renderClassesGrid();
        populateChatFocusSelector();
      },
      error: function () {
        $submitBtn.prop("disabled", false).html(origHtml);
      }
    });
  });

  // =========================================================
  // FREE PRACTICE CHAT LOGIC
  // =========================================================
  var textarea = document.getElementById("message-input");
  if (textarea) {
    textarea.addEventListener("input", function () {
      autoResize(this);
    });
    autoResize(textarea);
  }

  $("#message-form").on("submit", function (e) {
    e.preventDefault();
    var message = $("#message-input").val();
    if (message.trim() !== "") {
      $("#message-input").val("");
      $.post("/user_message_info", { message: message }, function (response) {
        var has_user_recording = response["user_recording"] !== null;
        var is_language_learning = response["is_language_learning"];
        var error_message = response["error"];
        if (error_message !== null) showNotification(error_message);
        addMessage("user", message, has_user_recording, is_language_learning);
        getResponse(0);
      });
    }
  });

  let recordedBlobPromise;
  $("#record-button").on("click", function () {
    var recordButton = $(this);
    var langToggleButton = $("#lang-toggle-button");

    if (recordButton.attr("name") === "stop") {
      stopAudio();
    } else if (recordButton.hasClass("off")) {
      recordButton.removeClass("off").addClass("on");
      langToggleButton.removeClass("off").addClass("on");
      recordedBlobPromise = startRecording();
    } else {
      recordButton.removeClass("on").addClass("off");
      langToggleButton.removeClass("on").addClass("off");
      toggleLoadingIcon("show");
      stopRecording();
      recordedBlobPromise.then(blob => {
        uploadAudio(blob).then(filename => {
          $.post("/transcribe_recording", { filename: filename }, function (response) {
            var recorded_text = response["recorded_text"];
            var error_message = response["error"];
            if (error_message !== null) showNotification(error_message);
            $("#message-input").val(recorded_text);
            if (auto_send_recording) {
              $("#submit-button").click();
            } else {
              $("#message-input").focus();
            }
            autoResize(textarea);
            toggleLoadingIcon("hide");
          });
        }).catch(error => {
          showNotification(error);
          toggleLoadingIcon("hide");
        });
      }).catch(error => {
        showNotification(error);
        toggleLoadingIcon("hide");
      });
    }
  });

  $("#message-input").keydown(function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      $("#message-form").submit();
      autoResize(this);
    }
  });

  $("#header-dark-toggle").on("click", function () {
    darkMode = !darkMode;
    setDarkMode(darkMode);
  });

  $.post("/set_language", { language: languages[currentLanguageIndex] }, function () {});
  $("#lang-toggle-button").on("click", function () {
    var lang_button = $("#lang-toggle-button");
    if (lang_button.hasClass("on")) return;
    currentLanguageIndex = (currentLanguageIndex + 1) % languages.length;
    $("#lang-text").text(languages[currentLanguageIndex]);
    $.post("/set_language", { language: languages[currentLanguageIndex] }, function () {});
  });

  $("#save-session").on("click", function () {
    $.get("/save_session", function (response) {
      if (response["success"]) {
        var saveIcon = $("#save-icon");
        saveIcon.removeClass("fa-floppy-disk").addClass("fa-check");
        setTimeout(function () {
          saveIcon.removeClass("fa-check").addClass("fa-floppy-disk");
        }, 2000);
      }
    });
  });

  $("#load-saved-session").on("click", function () {
    $.get("/load_session", function (response) {
      var messages = response["messages"];
      if (messages.length > 0) {
        initAudio();
        $("#audio-init").hide();
        $("#main-chat").show();
        loadPastMessages(messages);
      } else {
        showNotification("Aucune discussion sauvegardée.");
      }
    });
  });
});

function startFocusedChat(focusId) {
  initAudio();
  $("#audio-init").hide();
  $("#main-chat").show();
  $("#message-box").empty();
  $.post("/api/set_chat_focus", { focus_id: focusId || "" }, function () {
    getResponse(1);
  });
}

var message_counter = 1;
function addMessage(sender, message, has_user_recording, is_language_learning, do_not_store) {
  var message_box = $("#message-box");
  var message_row = $('<div class="row mb-3"></div>');
  var message_col = $('<div class="col d-flex align-items-start"></div>');
  var message_card = $('<div class="card flex-grow-1 rounded-4"></div>');
  var message_body = $('<div class="card-body"></div>');
  message_body.text(message);
  message_body.id = "message_" + message_counter;
  message_counter += 1;

  if (sender === "user") {
    message_card.addClass("bg-primary text-white");
    var img = $('<img src="' + user_profile_img + '" alt="User" class="profile-pic rounded-circle mr-3" width="44" height="44">');
  } else {
    message_card.addClass("bg-light text-dark");
    var img = $('<img src="' + bot_profile_img + '" alt="Tutor" class="profile-pic rounded-circle mr-3" width="44" height="44">');
  }

  message_card.append(message_body);

  var button_container = $('<div class="button-container"></div>');
  if (sender === "user") {
    var sound_on_button = is_language_learning
      ? $('<div class="d-block"><button type="button" class="btn btn-link user-button sound-on-button"><i class="fas fa-volume-up"></i></button></div>')
      : null;
    var translate_button = !is_language_learning
      ? $('<div class="d-block"><button type="button" class="btn btn-link user-button translate-button"><i class="fa fa-language"></i></button></div>')
      : null;
    if (sound_on_button) button_container.append(sound_on_button);
    if (translate_button) button_container.append(translate_button);
  } else {
    var translate_button = $('<div class="d-block"><button type="button" class="btn btn-link bot-button translate-button"><i class="fa fa-language"></i></button></div>');
    var sound_on_button = $('<div class="d-block"><button type="button" class="btn btn-link bot-button sound-on-button"><i class="fas fa-volume-up"></i></button></div>');
    button_container.append(translate_button).append(sound_on_button);
  }
  message_card.append(button_container);

  message_col.append(img).append(message_card);
  message_row.append(message_col);
  message_box.append(message_row);
  message_box.scrollTop(message_box.prop("scrollHeight"));

  var translated_message = false;
  if (translate_button) {
    translate_button.on("click", function () {
      if (!translated_message) {
        $.post("/translate_text", { text: message_body.html(), sender: sender }, function (response) {
          var translated_text = (response["message"] || "").replace(/\n/g, "<br>");
          message_body.html(message_body.html() + "<hr><em>" + translated_text + "</em>");
          translated_message = true;
        });
      }
    });
  }
  if (sound_on_button) {
    sound_on_button.on("click", function () {
      stopPlaying = false;
      $.post("/play_bot_recording", { message_id: message_body.id, text: message_body.text(), play_existing: 1 }, function () {});
    });
  }

  if (sender === "user" && !do_not_store) {
    $.post("/store_message", { sender: sender, message: message }, function () {});
  }
}

function toggleLoadingIcon(action) {
  if (action === "show") {
    $("#logo-image").attr("src", "/static/logo-loading.gif");
  } else if (action === "hide") {
    $("#logo-image").attr("src", "/static/logo.png");
  }
}

function getResponse(is_initial_message) {
  toggleLoadingIcon("show");
  stopPlaying = false;
  $.post("/get_response", { is_initial_message: is_initial_message }, function (response) {
    var bot_message = response["message"];
    var message_index = response["message_index"];
    if (response["error"] !== null) showNotification(response["error"]);
    addMessage("assistant", bot_message, false);
    getNextMessage(message_index);
  });
}

function getNextMessage(message_index) {
  $.post("/get_next_message", { message_index: message_index }, function (response) {
    var bot_message = response["message"];
    if (bot_message === null) {
      toggleLoadingIcon("hide");
      return;
    }
    updateLastMessage(bot_message.replace(/\n/g, "<br>"));
    getNextMessage(message_index);
  });
}

function updateLastMessage(newContent) {
  $("#message-box").find(".row:last .card-body").html(newContent);
}

function setDarkMode(isDarkMode) {
  if (isDarkMode) {
    $("body").addClass("dark-mode");
    $("#mode-icon").removeClass("fa-sun").addClass("fa-moon");
  } else {
    $("body").removeClass("dark-mode");
    $("#mode-icon").removeClass("fa-moon").addClass("fa-sun");
  }
}

function loadPastMessages(messages) {
  var message_box = $("#message-box");
  message_box.html("");
  for (var i = 0; i < messages.length; i++) {
    var msg = messages[i];
    addMessage(msg.role, msg.content, false, msg.is_language_learning, true);
  }
}

function autoResize(textarea) {
  if (!textarea) return;
  textarea.style.height = "2.2em";
  textarea.style.height = textarea.scrollHeight + "px";
}

function initChat() {
  initAudio();
  $("#audio-init").hide();
  $("#main-chat").show();
  getResponse(1);
}
