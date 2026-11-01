$.getScript("/static/common.js");
$.getScript("/static/audio.js");

let curriculumClasses = [];
let b1Roadmap = null;
let studyProgress = { completed_exercises: [], completed_speaking: [], mastered_classes: [] };
let selectedClassId = "class-11"; // Default to latest class (Class 11) so user sees their current lesson immediately
let activeOralRecordingId = null;
let activeOralBlobPromise = null;

// Structured Course (A1 -> A2 -> B1) State
let structuredCourseLevels = [];
let allCourseModules = [];
let courseProgress = {
  mastered_modules: [],
  module_scores: {},
  attempts_count: {},
  needs_review_modules: [],
  completed_a2_writing: []
};
let selectedCourseModuleId = "b1-m1";
let selectedCourseLevelFilter = "ALL";
let refresherFilter = "ALL";
let isRefresherOpen = false;

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
  if ($btn) {
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin"></i>');
  }
  $.post("/api/speak_french", { text: text }, function (res) {
    if ($btn) {
      $btn.prop("disabled", false).html('<i class="fa-solid fa-volume-high"></i>');
    }
    if (res.file_url) {
      playSingleAudioFile(res.file_url);
    } else if (res.error) {
      showNotification(res.error);
    }
  }).fail(function () {
    if ($btn) {
      $btn.prop("disabled", false).html('<i class="fa-solid fa-volume-high"></i>');
    }
  });
}

function switchTab(tabId) {
  $(".tab-btn").removeClass("active");
  $(`.tab-btn[data-tab="${tabId}"]`).addClass("active");
  $(".tab-section").hide().removeClass("active");
  $(`#${tabId}`).show().addClass("active");
}

function loadCurriculumData() {
  $.get("/api/curriculum", function (data) {
    curriculumClasses = data.classes || [];
    b1Roadmap = data.roadmap || null;
    studyProgress = data.progress || { completed_exercises: [], completed_speaking: [], mastered_classes: [] };

    if (curriculumClasses.length > 0 && !curriculumClasses.some(c => c.id === selectedClassId)) {
      selectedClassId = curriculumClasses[curriculumClasses.length - 1].id;
    }

    renderClassSidebar();
    renderClassDetail(selectedClassId);
    populateClassSelectors();
    renderExercisesForClass(selectedClassId);
    renderB1Roadmap();
  });
}

function renderClassSidebar() {
  const $nav = $("#class-list-nav");
  $nav.empty();

  curriculumClasses.forEach(function (cls) {
    const isActive = cls.id === selectedClassId ? "active" : "";
    const $item = $(`
      <button type="button" class="class-nav-item ${isActive}" data-class-id="${escapeHtml(cls.id)}">
        <div>
          <div class="class-num-badge">Cours ${escapeHtml(cls.number)} • ${escapeHtml(cls.date)}</div>
          <div class="fw-bold small mt-1">${escapeHtml(cls.title)}</div>
        </div>
        <span class="badge bg-secondary ms-2">${escapeHtml(cls.cefr_level || "A2/B1")}</span>
      </button>
    `);
    $item.on("click", function () {
      selectedClassId = cls.id;
      renderClassSidebar();
      renderClassDetail(selectedClassId);
      $("#exercise-class-select").val(selectedClassId);
      renderExercisesForClass(selectedClassId);
    });
    $nav.append($item);
  });
}

function renderClassDetail(classId) {
  const cls = curriculumClasses.find(c => c.id === classId);
  const $view = $("#class-detail-view");
  if (!cls) {
    $view.html('<p class="text-muted">Sélectionnez un cours à gauche.</p>');
    return;
  }

  let conceptsHtml = "";
  (cls.concepts || []).forEach(function (concept) {
    let rulesHtml = "";
    (concept.rules || []).forEach(function (r) {
      rulesHtml += `<li>${escapeHtml(r)}</li>`;
    });

    let examplesHtml = "";
    (concept.examples || []).forEach(function (ex) {
      examplesHtml += `
        <div class="example-box">
          <div>
            <div class="fw-bold text-primary">${escapeHtml(ex.fr)}</div>
            <div class="small text-muted">${escapeHtml(ex.en)}</div>
          </div>
          <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(ex.fr)}" title="Écouter la prononciation">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      `;
    });

    conceptsHtml += `
      <div class="concept-card">
        <h3 class="h6 fw-bold mb-2">${escapeHtml(concept.title)}</h3>
        <p class="small text-muted mb-2">${escapeHtml(concept.explanation)}</p>
        <ul class="rule-list small">${rulesHtml}</ul>
        ${examplesHtml}
      </div>
    `;
  });

  let vocabHtml = "";
  (cls.vocabulary || []).forEach(function (v) {
    const cleanFr = v.fr.split(" vs.")[0].split(" (")[0].trim();
    vocabHtml += `
      <div class="vocab-item">
        <div>
          <div class="fw-bold small">${escapeHtml(v.fr)}</div>
          <div class="small text-muted">${escapeHtml(v.en)}</div>
          ${v.note ? `<div class=" badge bg-light text-dark border mt-1">${escapeHtml(v.note)}</div>` : ""}
        </div>
        <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(cleanFr)}" title="Écouter">
          <i class="fa-solid fa-volume-high"></i>
        </button>
      </div>
    `;
  });

  const html = `
    <div class="d-flex flex-wrap justify-content-between align-items-start gap-2 mb-3 pb-3 border-bottom">
      <div>
        <span class="badge bg-primary mb-1">Cours ${escapeHtml(cls.number)} (${escapeHtml(cls.date)}) • Niveau ${escapeHtml(cls.cefr_level)}</span>
        <h2 class="h4 fw-bold mb-1">${escapeHtml(cls.title)}</h2>
        <p class="text-muted small mb-0">${escapeHtml(cls.summary)}</p>
      </div>
      <div class="d-flex gap-2">
        <button type="button" class="btn btn-sm btn-danger go-practice-exercises-btn" data-class-id="${escapeHtml(cls.id)}">
          <i class="fa-solid fa-microphone-lines me-1"></i> Faire les Exercices &amp; Oral (${(cls.written_exercises || []).length + (cls.speaking_prompts || []).length})
        </button>
        <button type="button" class="btn btn-sm btn-outline-primary go-chat-class-btn" data-class-id="${escapeHtml(cls.id)}">
          <i class="fa-solid fa-comments me-1"></i> Parler avec Renée
        </button>
      </div>
    </div>

    ${cls.homework ? `
      <div class="alert alert-primary d-flex flex-wrap justify-content-between align-items-center gap-2 mb-4">
        <div>
          <div class="fw-bold small text-uppercase"><i class="fa-solid fa-house-laptop me-1"></i> Devoir du Cours ${escapeHtml(cls.number)}</div>
          <div class="small mt-1">${escapeHtml(cls.homework)}</div>
        </div>
        <button type="button" class="btn btn-sm btn-primary go-practice-exercises-btn" data-class-id="${escapeHtml(cls.id)}">
          <i class="fa-solid fa-microphone me-1"></i> Pratiquer ce devoir à l'oral
        </button>
      </div>
    ` : ""}

    <h3 class="h5 fw-bold mb-3"><i class="fa-solid fa-lightbulb text-warning me-2"></i>Règles &amp; Concepts Clés</h3>
    ${conceptsHtml}

    <h3 class="h5 fw-bold mt-4 mb-3"><i class="fa-solid fa-spell-check text-success me-2"></i>Vocabulaire &amp; Expressions du Cours (Cliquez sur 🔊)</h3>
    <div class="vocab-grid mb-2">
      ${vocabHtml}
    </div>
  `;

  $view.html(html);
}

function populateClassSelectors() {
  const $exSelect = $("#exercise-class-select");
  const $chatSelect = $("#chat-focus-select");

  $exSelect.empty();
  $chatSelect.html('<option value="">Conversation libre (Tous niveaux / Quotidien)</option>');

  curriculumClasses.forEach(function (cls) {
    $exSelect.append(`<option value="${escapeHtml(cls.id)}">Cours ${escapeHtml(cls.number)} (${escapeHtml(cls.date)}) — ${escapeHtml(cls.title)}</option>`);
    $chatSelect.append(`<option value="${escapeHtml(cls.id)}">Cours ${escapeHtml(cls.number)} : ${escapeHtml(cls.title)}</option>`);
  });

  if (b1Roadmap && b1Roadmap.b1_speaking_simulators) {
    b1Roadmap.b1_speaking_simulators.forEach(function (sim) {
      $chatSelect.append(`<option value="${escapeHtml(sim.id)}">DELF B1 Oral — ${escapeHtml(sim.part)} : ${escapeHtml(sim.title)}</option>`);
    });
  }

  if (allCourseModules && allCourseModules.length > 0) {
    allCourseModules.forEach(function (m) {
      $chatSelect.append(`<option value="${escapeHtml(m.id)}">Cours Gemini ${escapeHtml(m.code)} (${escapeHtml(m.theme)}) : ${escapeHtml(m.title)}</option>`);
    });
  }

  $exSelect.val(selectedClassId);
}

function renderExercisesForClass(classId) {
  const cls = curriculumClasses.find(c => c.id === classId);
  if (!cls) return;

  const completedWritten = (studyProgress.completed_exercises || []).length;
  const completedSpoken = (studyProgress.completed_speaking || []).length;
  $("#written-progress-badge").text(`${completedWritten + completedSpoken} réussis au total`);

  // 1. Render Speaking Prompts
  const $speakingContainer = $("#speaking-prompts-container");
  $speakingContainer.empty();

  (cls.speaking_prompts || []).forEach(function (sp) {
    const isDone = (studyProgress.completed_speaking || []).includes(sp.id);
    const structuresBadges = (sp.target_structures || [])
      .map(s => `<span class="badge bg-light text-dark border me-1 mb-1">${escapeHtml(s)}</span>`)
      .join("");

    const $card = $(`
      <div class="speaking-card" id="sp-card-${escapeHtml(sp.id)}">
        <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
          <h3 class="h6 fw-bold mb-0">
            ${isDone ? '<i class="fa-solid fa-circle-check text-success me-1"></i>' : '<i class="fa-solid fa-comments text-danger me-1"></i>'}
            ${escapeHtml(sp.title)}
          </h3>
          <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(sp.prompt_fr)}" title="Écouter la consigne">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
        <p class="small mb-2">${escapeHtml(sp.prompt_fr)}</p>
        <div class="mb-3">
          <span class="small text-muted d-block mb-1">Expressions cibles à utiliser :</span>
          ${structuresBadges}
        </div>
        <div class="mb-2">
          <textarea class="form-control form-control-sm oral-answer-input" id="oral-input-${escapeHtml(sp.id)}" rows="3" placeholder="Cliquez sur 'Parler au micro' pour dicter votre réponse en français, ou écrivez-la ici..."></textarea>
        </div>
        <div class="d-flex flex-wrap gap-2">
          <button type="button" class="btn btn-sm btn-danger oral-record-btn" data-sp-id="${escapeHtml(sp.id)}">
            <i class="fa-solid fa-microphone me-1"></i> Parler au micro
          </button>
          <button type="button" class="btn btn-sm btn-primary evaluate-oral-btn" data-sp-id="${escapeHtml(sp.id)}" data-class-id="${escapeHtml(cls.id)}" data-prompt="${escapeHtml(sp.prompt_fr)}">
            <i class="fa-solid fa-wand-magic-sparkles me-1"></i> Évaluer ma réponse (Correction B1)
          </button>
        </div>
        <div id="oral-feedback-${escapeHtml(sp.id)}"></div>
      </div>
    `);
    $speakingContainer.append($card);
  });

  // 2. Render Written Exercises
  const $writtenContainer = $("#written-exercises-container");
  $writtenContainer.empty();

  (cls.written_exercises || []).forEach(function (ex, idx) {
    const isDone = (studyProgress.completed_exercises || []).includes(ex.id);
    const $exCard = $(`
      <div class="exercise-card" id="ex-card-${escapeHtml(ex.id)}">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <span class="badge bg-secondary">Exercice ${idx + 1}</span>
          ${isDone ? '<span class="badge bg-success"><i class="fa-solid fa-check me-1"></i>Réussi</span>' : ""}
        </div>
        <p class="fw-bold small mt-2 mb-1">${escapeHtml(ex.question)}</p>
        <p class="small text-muted mb-2"><i class="fa-regular fa-lightbulb me-1"></i>Indice : ${escapeHtml(ex.hint || "")}</p>
        <div class="input-group input-group-sm mb-2">
          <input type="text" class="form-control written-answer-input" id="written-input-${escapeHtml(ex.id)}" placeholder="Votre réponse en français...">
          <button type="button" class="btn btn-primary check-written-btn"
            data-ex-id="${escapeHtml(ex.id)}"
            data-class-id="${escapeHtml(cls.id)}"
            data-question="${escapeHtml(ex.question)}"
            data-answer="${escapeHtml(ex.answer)}"
            data-accepted='${escapeHtml(JSON.stringify(ex.accepted_answers || [ex.answer]))}'
            data-explanation="${escapeHtml(ex.explanation)}">
            Vérifier
          </button>
          <button type="button" class="btn btn-outline-secondary ai-check-written-btn"
            data-ex-id="${escapeHtml(ex.id)}"
            data-class-id="${escapeHtml(cls.id)}"
            data-question="${escapeHtml(ex.question)}"
            data-answer="${escapeHtml(ex.answer)}"
            title="Demander une explication détaillée à Renée">
            <i class="fa-solid fa-robot"></i> Aide IA
          </button>
        </div>
        <div id="written-feedback-${escapeHtml(ex.id)}"></div>
      </div>
    `);
    $writtenContainer.append($exCard);
  });
}

function renderEvaluationCard(evaluation, containerSelector) {
  if (!evaluation) return;
  const score = evaluation.score || 0;
  const badgeClass = score >= 8 ? "bg-success" : score >= 6 ? "bg-primary" : "bg-warning text-dark";
  const boxClass = score >= 6 ? "feedback-box" : "feedback-box needs-work";

  const html = `
    <div class="${boxClass}">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <span class="badge ${badgeClass}">${escapeHtml(evaluation.verdict || "Évaluation")} — ${score}/10</span>
        ${evaluation.spoken_feedback_fr ? `
          <button type="button" class="btn btn-sm btn-outline-primary play-fr-btn" data-fr="${escapeHtml(evaluation.spoken_feedback_fr)}">
            <i class="fa-solid fa-volume-high me-1"></i> Réécouter Renée
          </button>
        ` : ""}
      </div>
      <div class="small mb-2">
        <strong>✅ Correction en français :</strong>
        <div class="d-flex justify-content-between align-items-center bg-light dark-surface p-2 rounded mt-1 border">
          <span class="text-primary fw-bold">${escapeHtml(evaluation.corrected_french || "")}</span>
          <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(evaluation.corrected_french || "")}">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      </div>
      <div class="small mb-2">
        <strong>💡 Explication grammaticale :</strong>
        <div class="text-muted mt-1">${escapeHtml(evaluation.explanation_en || "")}</div>
      </div>
      ${evaluation.b1_upgrade_fr ? `
        <div class="small">
          <strong>🚀 Version Modèle DELF B1 (avec connecteurs) :</strong>
          <div class="d-flex justify-content-between align-items-center bg-light dark-surface p-2 rounded mt-1 border">
            <span>${escapeHtml(evaluation.b1_upgrade_fr)}</span>
            <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(evaluation.b1_upgrade_fr)}">
              <i class="fa-solid fa-volume-high"></i>
            </button>
          </div>
        </div>
      ` : ""}
    </div>
  `;
  $(containerSelector).html(html);
}

function renderB1Roadmap() {
  if (!b1Roadmap) return;
  const $container = $("#b1-roadmap-container");

  let sectionsHtml = "";
  (b1Roadmap.exam_requirements.sections || []).forEach(function (s) {
    sectionsHtml += `
      <div class="col-md-6 col-lg-3">
        <div class="concept-card h-100 mb-0">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="badge bg-primary">${escapeHtml(s.points)}</span>
            <span class="small text-muted"><i class="fa-regular fa-clock me-1"></i>${escapeHtml(s.duration)}</span>
          </div>
          <h4 class="h6 fw-bold">${escapeHtml(s.name)}</h4>
          <p class="small text-muted mb-0">${escapeHtml(s.details)}</p>
        </div>
      </div>
    `;
  });

  let milestonesHtml = "";
  (b1Roadmap.milestones || []).forEach(function (m) {
    const topicsList = (m.topics || []).map(t => `<li>${escapeHtml(t)}</li>`).join("");
    milestonesHtml += `
      <div class="concept-card">
        <div class="d-flex flex-wrap justify-content-between align-items-center mb-2">
          <h4 class="h6 fw-bold mb-0">${escapeHtml(m.month)}</h4>
          <span class="badge bg-info text-dark">${escapeHtml(m.status)}</span>
        </div>
        <ul class="rule-list small mb-0">${topicsList}</ul>
      </div>
    `;
  });

  let simulatorsHtml = "";
  (b1Roadmap.b1_speaking_simulators || []).forEach(function (sim) {
    simulatorsHtml += `
      <div class="col-lg-4">
        <div class="speaking-card h-100 d-flex flex-column justify-content-between mb-0">
          <div>
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-danger">${escapeHtml(sim.part)}</span>
              <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(sim.prompt_fr)}" title="Écouter le sujet">
                <i class="fa-solid fa-volume-high"></i>
              </button>
            </div>
            <h4 class="h6 fw-bold">${escapeHtml(sim.title)}</h4>
            <p class="small mb-2">${escapeHtml(sim.prompt_fr)}</p>
            <p class="small text-muted"><i class="fa-solid fa-lightbulb text-warning me-1"></i><strong>Astuce B1 :</strong> ${escapeHtml(sim.tips)}</p>
          </div>
          <div class="mt-2">
            <button type="button" class="btn btn-sm btn-primary w-100 go-chat-class-btn" data-class-id="${escapeHtml(sim.id)}">
              <i class="fa-solid fa-comments me-1"></i> Simuler cette épreuve avec Renée
            </button>
          </div>
        </div>
      </div>
    `;
  });

  const html = `
    <div class="panel-card mb-4 border-primary">
      <div class="row align-items-center g-3">
        <div class="col-lg-8">
          <span class="badge bg-success mb-2"><i class="fa-solid fa-check-circle me-1"></i>Évaluation de faisabilité : ${escapeHtml(b1Roadmap.feasibility_verdict)}</span>
          <h2 class="h4 fw-bold">Objectif : Certificat DELF B1 d'ici fin Février</h2>
          <p class="small text-muted mb-2">${escapeHtml(b1Roadmap.feasibility_summary)}</p>
          <div class="small fw-bold text-primary">
            <i class="fa-solid fa-award me-1"></i> Seuil de réussite officiel : ${escapeHtml(b1Roadmap.exam_requirements.passing_score)}
          </div>
        </div>
        <div class="col-lg-4 text-lg-end">
          <div class="p-3 rounded bg-light dark-surface border text-center">
            <div class="small text-muted">Votre progression actuelle</div>
            <div class="h3 fw-bold text-primary my-1">${curriculumClasses.length} Cours étudiés</div>
            <div class="small text-success fw-bold">
              ${(studyProgress.completed_exercises || []).length} exercices écrits • ${(studyProgress.completed_speaking || []).length} défis oraux validés
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="panel-card mb-4">
      <h3 class="h5 fw-bold mb-3"><i class="fa-solid fa-clipboard-check text-primary me-2"></i>Les 4 Épreuves du DELF B1</h3>
      <div class="row g-3">
        ${sectionsHtml}
      </div>
    </div>

    <div class="panel-card mb-4">
      <h3 class="h5 fw-bold mb-3"><i class="fa-solid fa-microphone-lines text-danger me-2"></i>Simulateur d'Examen Oral DELF B1 (Production Orale — 25 points)</h3>
      <div class="row g-3">
        ${simulatorsHtml}
      </div>
    </div>

    <div class="panel-card">
      <h3 class="h5 fw-bold mb-3"><i class="fa-solid fa-calendar-check text-success me-2"></i>Plan de Route sur 4 Mois (Novembre → Fin Février)</h3>
      ${milestonesHtml}
    </div>
  `;

  $container.html(html);
}

// =========================================================
// STRUCTURED COURSE (A1 -> A2 -> B1) PRESENTED BY GEMINI
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

    if (allCourseModules.length > 0 && !allCourseModules.some(m => m.id === selectedCourseModuleId)) {
      selectedCourseModuleId = allCourseModules[0].id;
    }

    renderCourseTrackerBanner();
    renderCourseRefresherPanel();
    renderCourseSidebar();
    renderCourseModuleDetail(selectedCourseModuleId);
    populateClassSelectors();
  });
}

function getLevelStats(levelCode) {
  const mods = allCourseModules.filter(m => m.level === levelCode);
  const mastered = mods.filter(m => (courseProgress.mastered_modules || []).includes(m.id)).length;
  const total = mods.length || 1;
  return {
    mastered: mastered,
    total: mods.length,
    pct: Math.round((mastered / total) * 100)
  };
}

function renderCourseTrackerBanner() {
  const a1 = getLevelStats("A1");
  const a2 = getLevelStats("A2");
  const b1 = getLevelStats("B1");
  const totalMastered = (courseProgress.mastered_modules || []).length;
  const totalMods = allCourseModules.length || 17;
  const overallPct = Math.round((totalMastered / totalMods) * 100);
  const reviewCount = (courseProgress.needs_review_modules || []).length;
  const a2WrittenDone = (courseProgress.completed_a2_writing || []).length;

  const html = `
    <div class="row align-items-center g-3">
      <div class="col-lg-5">
        <div class="d-flex align-items-center gap-2 mb-1">
          <span class="badge bg-primary"><i class="fa-solid fa-wand-magic-sparkles me-1"></i>Présenté par Gemini</span>
          <span class="badge bg-danger"><i class="fa-solid fa-gavel me-1"></i>Mode Strict : 8/10 requis</span>
          <span class="badge bg-success">Oral B1 + Écrit A2</span>
        </div>
        <h2 class="h4 fw-bold mb-1">Parcours Structuré A1 → A2 → B1</h2>
        <p class="small text-muted mb-2">
          Chaque module possède son <strong>thème</strong>, son <strong>vocabulaire audio</strong>, son <strong>aide-mémoire</strong> et un <strong>examen oral strict</strong> qui vérifie que vous maîtrisez vraiment le concept.
        </p>
        <div class="d-flex flex-wrap gap-2">
          <button type="button" id="toggle-refresher-btn" class="btn btn-sm ${isRefresherOpen ? 'btn-primary' : 'btn-outline-primary'}">
            <i class="fa-solid fa-bolt me-1"></i> ${isRefresherOpen ? 'Fermer l\'Aide-Mémoire' : 'Aide-Mémoire & Révision Rapide (17 fiches)'}
          </button>
          <button type="button" id="flash-oral-quiz-btn" class="btn btn-sm btn-outline-danger" title="Tester un concept au hasard à l'oral">
            <i class="fa-solid fa-shuffle me-1"></i> Quiz Oral Flash (Aléatoire)
          </button>
        </div>
      </div>

      <div class="col-lg-7">
        <div class="row g-2">
          <div class="col-sm-4">
            <div class="p-2 rounded bg-light dark-surface border">
              <div class="d-flex justify-content-between small fw-bold mb-1">
                <span>Niveau A1 (Survie Orale)</span>
                <span class="text-primary">${a1.mastered}/${a1.total}</span>
              </div>
              <div class="progress" style="height: 8px;">
                <div class="progress-bar bg-info" role="progressbar" style="width: ${a1.pct}%"></div>
              </div>
            </div>
          </div>
          <div class="col-sm-4">
            <div class="p-2 rounded bg-light dark-surface border">
              <div class="d-flex justify-content-between small fw-bold mb-1">
                <span>Niveau A2 (Oral + Écrit A2)</span>
                <span class="text-primary">${a2.mastered}/${a2.total}</span>
              </div>
              <div class="progress" style="height: 8px;">
                <div class="progress-bar bg-primary" role="progressbar" style="width: ${a2.pct}%"></div>
              </div>
            </div>
          </div>
          <div class="col-sm-4">
            <div class="p-2 rounded bg-light dark-surface border">
              <div class="d-flex justify-content-between small fw-bold mb-1">
                <span>Niveau B1 (Maîtrise Orale)</span>
                <span class="text-success">${b1.mastered}/${b1.total}</span>
              </div>
              <div class="progress" style="height: 8px;">
                <div class="progress-bar bg-success" role="progressbar" style="width: ${b1.pct}%"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="d-flex flex-wrap justify-content-between align-items-center mt-2 pt-2 border-top small">
          <span><strong>Progression globale :</strong> ${totalMastered} / ${totalMods} modules validés (${overallPct}%)</span>
          <span><strong>Écrit Cible A2 :</strong> ${a2WrittenDone} / 2 validés</span>
          <span class="text-warning fw-bold"><i class="fa-solid fa-bookmark me-1"></i>À réviser : ${reviewCount} module(s)</span>
        </div>
      </div>
    </div>
  `;

  $("#course-tracker-banner").html(html);
}

function renderCourseRefresherPanel() {
  const $panel = $("#course-refresher-panel");
  if (!isRefresherOpen) {
    $panel.hide();
    return;
  }
  $panel.show();

  let filtered = allCourseModules;
  if (refresherFilter === "MASTERED") {
    filtered = allCourseModules.filter(m => (courseProgress.mastered_modules || []).includes(m.id));
  } else if (refresherFilter === "REVIEW") {
    filtered = allCourseModules.filter(m => (courseProgress.needs_review_modules || []).includes(m.id));
  }

  let cardsHtml = "";
  if (filtered.length === 0) {
    cardsHtml = `<p class="text-muted small mb-0">Aucun module dans cette catégorie pour le moment.</p>`;
  } else {
    filtered.forEach(function (m) {
      const isMastered = (courseProgress.mastered_modules || []).includes(m.id);
      const isReview = (courseProgress.needs_review_modules || []).includes(m.id);
      const bestScore = (courseProgress.module_scores || {})[m.id];
      const ref = m.quick_refresher || {};

      cardsHtml += `
        <div class="refresher-card">
          <div>
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-primary">${escapeHtml(m.code)} • ${escapeHtml(m.theme)}</span>
              ${isMastered
                ? `<span class="badge bg-success"><i class="fa-solid fa-check me-1"></i>Validé (${bestScore || 8}/10)</span>`
                : isReview
                ? `<span class="badge bg-warning text-dark">À réviser</span>`
                : `<span class="badge bg-secondary">Non validé</span>`
              }
            </div>
            <h4 class="h6 fw-bold mb-1">${escapeHtml(ref.rule_title || m.title)}</h4>
            <div class="small bg-white dark-surface p-2 rounded border mb-2 font-monospace text-primary">
              ${escapeHtml(ref.formula || "")}
            </div>
            <p class="small text-muted mb-2">
              <strong>💡 Règle d'or :</strong> ${escapeHtml(ref.key_takeaway || "")}
            </p>
          </div>
          <div class="d-flex justify-content-between align-items-center pt-2 border-top mt-2">
            <button type="button" class="btn btn-sm btn-outline-primary jump-to-course-module-btn" data-mod-id="${escapeHtml(m.id)}">
              Ouvrir &amp; Pratiquer l'Oral
            </button>
            <button type="button" class="btn btn-sm ${isReview ? 'btn-warning' : 'btn-outline-secondary'} toggle-review-flag-btn" data-mod-id="${escapeHtml(m.id)}" title="Marquer à réviser">
              <i class="fa-solid fa-bookmark"></i>
            </button>
          </div>
        </div>
      `;
    });
  }

  const html = `
    <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3 pb-2 border-bottom">
      <div>
        <h3 class="h5 fw-bold mb-0"><i class="fa-solid fa-bolt text-warning me-2"></i>Aide-Mémoire &amp; Révision Rapide des Concepts (A1 → B1)</h3>
        <p class="small text-muted mb-0">Toutes les formules clés et pièges à éviter en un coup d'œil.</p>
      </div>
      <div class="btn-group btn-group-sm">
        <button type="button" class="btn ${refresherFilter === 'ALL' ? 'btn-primary' : 'btn-outline-primary'} refresher-filter-btn" data-filter="ALL">Tous (${allCourseModules.length})</button>
        <button type="button" class="btn ${refresherFilter === 'MASTERED' ? 'btn-success' : 'btn-outline-success'} refresher-filter-btn" data-filter="MASTERED">Validés ✅ (${(courseProgress.mastered_modules || []).length})</button>
        <button type="button" class="btn ${refresherFilter === 'REVIEW' ? 'btn-warning' : 'btn-outline-warning'} refresher-filter-btn" data-filter="REVIEW">À réviser ⚠️ (${(courseProgress.needs_review_modules || []).length})</button>
      </div>
    </div>
    <div class="refresher-grid">
      ${cardsHtml}
    </div>
  `;

  $panel.html(html);
}

function renderCourseSidebar() {
  const $list = $("#course-module-list");
  $list.empty();

  const modulesToShow = selectedCourseLevelFilter === "ALL"
    ? allCourseModules
    : allCourseModules.filter(m => m.level === selectedCourseLevelFilter);

  modulesToShow.forEach(function (m) {
    const isActive = m.id === selectedCourseModuleId ? "active" : "";
    const isMastered = (courseProgress.mastered_modules || []).includes(m.id);
    const isReview = (courseProgress.needs_review_modules || []).includes(m.id);
    const bestScore = (courseProgress.module_scores || {})[m.id];

    let statusBadge = `<span class="badge bg-secondary">${escapeHtml(m.level)}</span>`;
    if (isMastered) {
      statusBadge = `<span class="badge bg-success"><i class="fa-solid fa-check me-1"></i>${bestScore || 8}/10</span>`;
    } else if (isReview || bestScore) {
      statusBadge = `<span class="badge bg-warning text-dark">${bestScore ? bestScore + '/10' : 'À réviser'}</span>`;
    }

    const $btn = $(`
      <button type="button" class="class-nav-item ${isActive}" data-mod-id="${escapeHtml(m.id)}">
        <div>
          <div class="class-num-badge">${escapeHtml(m.code)} • Thème : ${escapeHtml(m.theme)}</div>
          <div class="fw-bold small mt-1">${escapeHtml(m.title)}</div>
        </div>
        <div class="ms-2 flex-shrink-0">${statusBadge}</div>
      </button>
    `);

    $btn.on("click", function () {
      selectedCourseModuleId = m.id;
      renderCourseSidebar();
      renderCourseModuleDetail(selectedCourseModuleId);
    });

    $list.append($btn);
  });
}

function renderCourseModuleDetail(moduleId) {
  const mod = allCourseModules.find(m => m.id === moduleId);
  const $detail = $("#course-module-detail");
  if (!mod) {
    $detail.html('<p class="text-muted">Sélectionnez un module à gauche.</p>');
    return;
  }

  const isMastered = (courseProgress.mastered_modules || []).includes(mod.id);
  const isReview = (courseProgress.needs_review_modules || []).includes(mod.id);
  const bestScore = (courseProgress.module_scores || {})[mod.id];
  const attempts = (courseProgress.attempts_count || {})[mod.id] || 0;
  const ref = mod.quick_refresher || {};

  let conceptsHtml = "";
  (mod.concepts || []).forEach(function (c) {
    const rulesList = (c.rules || []).map(r => `<li>${escapeHtml(r)}</li>`).join("");
    let examplesHtml = "";
    (c.examples || []).forEach(function (ex) {
      examplesHtml += `
        <div class="example-box">
          <div>
            <div class="fw-bold text-primary">${escapeHtml(ex.fr)}</div>
            <div class="small text-muted">${escapeHtml(ex.en)}</div>
          </div>
          <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(ex.fr)}" title="Écouter">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      `;
    });

    conceptsHtml += `
      <div class="concept-card">
        <h4 class="h6 fw-bold mb-2">${escapeHtml(c.title)}</h4>
        <p class="small text-muted mb-2">${escapeHtml(c.explanation)}</p>
        <ul class="rule-list small">${rulesList}</ul>
        ${examplesHtml}
      </div>
    `;
  });

  let vocabHtml = "";
  (mod.vocabulary || []).forEach(function (v) {
    const cleanFr = v.fr.split(" (")[0].split(" / ")[0].split(" (+")[0].trim();
    vocabHtml += `
      <div class="vocab-item">
        <div>
          <div class="fw-bold small">${escapeHtml(v.fr)}</div>
          <div class="small text-muted">${escapeHtml(v.en)}</div>
          ${v.note ? `<span class="badge bg-light text-dark border mt-1">${escapeHtml(v.note)}</span>` : ""}
        </div>
        <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(cleanFr)}" title="Écouter">
          <i class="fa-solid fa-volume-high"></i>
        </button>
      </div>
    `;
  });

  let oralChallengesHtml = "";
  (mod.oral_challenges || []).forEach(function (oc) {
    const mandatoryBadges = (oc.mandatory_structures || [])
      .map(s => `<span class="badge bg-danger me-1 mb-1">${escapeHtml(s)}</span>`)
      .join("");

    oralChallengesHtml += `
      <div class="strict-exam-box ${isMastered ? 'mastered' : ''} mb-4">
        <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-2">
          <div>
            <span class="badge ${isMastered ? 'bg-success' : 'bg-danger'} mb-1">
              ${isMastered ? '<i class="fa-solid fa-check-double me-1"></i>Module Validé à l\'Oral' : '<i class="fa-solid fa-gavel me-1"></i>Examen Oral Strict — Note minimale : 8 / 10'}
            </span>
            <h4 class="h6 fw-bold mb-0">${escapeHtml(oc.title)}</h4>
          </div>
          <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(oc.prompt_fr)}" title="Écouter la consigne">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>

        <p class="small mb-2">${escapeHtml(oc.prompt_fr)}</p>

        <div class="mb-3">
          <span class="small fw-bold text-danger d-block mb-1">
            <i class="fa-solid fa-list-check me-1"></i>Structures obligatoires vérifiées par Gemini :
          </span>
          ${mandatoryBadges}
        </div>

        <div class="mb-2">
          <textarea class="form-control form-control-sm" id="course-oral-input-${escapeHtml(oc.id)}" rows="3" placeholder="Cliquez sur 'Parler au micro' et répondez en faisant des phrases complètes..."></textarea>
        </div>

        <div class="d-flex flex-wrap gap-2">
          <button type="button" class="btn btn-sm btn-danger course-oral-record-btn" data-oc-id="${escapeHtml(oc.id)}">
            <i class="fa-solid fa-microphone me-1"></i> Parler au micro
          </button>
          <button type="button" class="btn btn-sm btn-primary evaluate-course-oral-btn"
            data-oc-id="${escapeHtml(oc.id)}"
            data-mod-id="${escapeHtml(mod.id)}"
            data-prompt="${escapeHtml(oc.prompt_fr)}"
            data-mandatory='${escapeHtml(JSON.stringify(oc.mandatory_structures || []))}'>
            <i class="fa-solid fa-gavel me-1"></i> Passer l'Évaluation Stricte (≥ 8/10 requis)
          </button>
        </div>

        <div id="course-oral-feedback-${escapeHtml(oc.id)}"></div>
      </div>
    `;
  });

  let writingTaskHtml = "";
  if (mod.writing_task_a2) {
    const wt = mod.writing_task_a2;
    const isWtDone = (courseProgress.completed_a2_writing || []).includes(mod.id);
    writingTaskHtml = `
      <div class="concept-card border-primary mt-3">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <span class="badge ${isWtDone ? 'bg-success' : 'bg-primary'}">
            <i class="fa-solid fa-pen-nib me-1"></i>Objectif Écrit Cible A2 ${isWtDone ? '— Validé ✅' : '(60–80 mots)'}
          </span>
        </div>
        <h4 class="h6 fw-bold">${escapeHtml(wt.title)}</h4>
        <p class="small mb-2">${escapeHtml(wt.prompt_fr)}</p>
        <textarea class="form-control form-control-sm mb-2" id="course-wt-input-${escapeHtml(mod.id)}" rows="4" placeholder="Écrivez votre courriel / message A2 ici (60 à 80 mots)..."></textarea>
        <button type="button" class="btn btn-sm btn-outline-primary evaluate-course-wt-btn"
          data-mod-id="${escapeHtml(mod.id)}"
          data-prompt="${escapeHtml(wt.prompt_fr)}">
          <i class="fa-solid fa-check me-1"></i> Vérifier mon Écrit A2
        </button>
        <div id="course-wt-feedback-${escapeHtml(mod.id)}"></div>
      </div>
    `;
  }

  const html = `
    <div class="d-flex flex-wrap justify-content-between align-items-start gap-2 mb-3 pb-3 border-bottom">
      <div>
        <div class="d-flex align-items-center gap-2 mb-1">
          <span class="badge bg-primary">${escapeHtml(mod.code)} (${escapeHtml(mod.level)})</span>
          <span class="badge bg-info text-dark"><i class="fa-solid fa-tag me-1"></i>Thème : ${escapeHtml(mod.theme)}</span>
          ${isMastered
            ? `<span class="badge bg-success"><i class="fa-solid fa-trophy me-1"></i>Maîtrisé (${bestScore}/10)</span>`
            : `<span class="badge bg-secondary">Meilleur score : ${bestScore ? bestScore + '/10' : 'Non testé'} (${attempts} essai${attempts > 1 ? 's' : ''})</span>`
          }
        </div>
        <h2 class="h4 fw-bold mb-0">${escapeHtml(mod.title)}</h2>
      </div>
      <div class="d-flex gap-2">
        <button type="button" class="btn btn-sm ${isReview ? 'btn-warning' : 'btn-outline-secondary'} toggle-review-flag-btn" data-mod-id="${escapeHtml(mod.id)}">
          <i class="fa-solid fa-bookmark me-1"></i> ${isReview ? 'Marqué à réviser' : 'Ajouter aux révisions'}
        </button>
        <button type="button" class="btn btn-sm btn-outline-primary go-chat-class-btn" data-class-id="${escapeHtml(mod.id)}">
          <i class="fa-solid fa-comments me-1"></i> Pratiquer avec Renée
        </button>
      </div>
    </div>

    <!-- Gemini Presentation Box -->
    <div class="gemini-presenter-box mb-4">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <div class="fw-bold text-primary small text-uppercase">
          <i class="fa-solid fa-wand-magic-sparkles me-1"></i> Présentation du Cours par Gemini
        </div>
        <button type="button" class="btn btn-sm btn-primary play-fr-btn" data-fr="${escapeHtml(mod.gemini_presentation)}">
          <i class="fa-solid fa-volume-high me-1"></i> Écouter la présentation
        </button>
      </div>
      <p class="small mb-0">${escapeHtml(mod.gemini_presentation)}</p>
    </div>

    <!-- Quick Refresher Formula Box -->
    <div class="refresher-formula-box mb-4">
      <div class="fw-bold small text-uppercase mb-1">
        <i class="fa-solid fa-bolt text-warning me-1"></i> Aide-Mémoire Express : ${escapeHtml(ref.rule_title || "")}
      </div>
      <div class="small font-monospace fw-bold text-primary mb-1">${escapeHtml(ref.formula || "")}</div>
      <div class="small text-muted"><strong>À retenir absolument :</strong> ${escapeHtml(ref.key_takeaway || "")}</div>
    </div>

    <!-- Strict Oral Mastery Section First (Speaking Priority!) -->
    <h3 class="h5 fw-bold mb-3"><i class="fa-solid fa-microphone-lines text-danger me-2"></i>1. Validation Orale Stricte du Concept (Priorité Speaking)</h3>
    ${oralChallengesHtml}

    <!-- Thematic Vocabulary with Audio -->
    <h3 class="h5 fw-bold mb-3"><i class="fa-solid fa-book-bookmark text-success me-2"></i>2. Vocabulaire du Thème : ${escapeHtml(mod.theme)} (Cliquez sur 🔊)</h3>
    <div class="vocab-grid mb-4">
      ${vocabHtml}
    </div>

    <!-- Detailed Concept Breakdown -->
    <h3 class="h5 fw-bold mb-3"><i class="fa-solid fa-graduation-cap text-primary me-2"></i>3. Explications Détaillées &amp; Exemples Audio</h3>
    ${conceptsHtml}

    ${writingTaskHtml}
  `;

  $detail.html(html);
}

function renderStrictCourseEvaluation(ev, containerSelector) {
  if (!ev) return;
  const passed = ev.passed;
  const score = ev.score || 0;
  const badgeClass = passed ? "bg-success" : "bg-danger";
  const boxClass = passed ? "feedback-box" : "feedback-box needs-work";

  const html = `
    <div class="${boxClass} mt-3">
      <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-2">
        <span class="badge ${badgeClass} fs-6">${escapeHtml(ev.verdict || "")} — Score : ${score}/10</span>
        ${ev.spoken_examiner_feedback_fr ? `
          <button type="button" class="btn btn-sm btn-outline-primary play-fr-btn" data-fr="${escapeHtml(ev.spoken_examiner_feedback_fr)}">
            <i class="fa-solid fa-volume-high me-1"></i> Réécouter l'examinateur
          </button>
        ` : ""}
      </div>

      <div class="small mb-2">
        <strong>📋 Vérification des structures obligatoires :</strong>
        <div class="text-muted mt-1">${escapeHtml(ev.structures_used_check || "")}</div>
      </div>

      <div class="small mb-2">
        <strong>✅ Votre réponse corrigée :</strong>
        <div class="d-flex justify-content-between align-items-center bg-light dark-surface p-2 rounded mt-1 border">
          <span class="text-primary fw-bold">${escapeHtml(ev.corrected_french || "")}</span>
          <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(ev.corrected_french || "")}">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      </div>

      <div class="small mb-2">
        <strong>🔍 Explication stricte de la règle :</strong>
        <div class="text-muted mt-1">${escapeHtml(ev.strict_explanation_en || "")}</div>
      </div>

      ${ev.model_answer_fr ? `
        <div class="small mb-2">
          <strong>🏆 Réponse Modèle (Niveau Cible) :</strong>
          <div class="d-flex justify-content-between align-items-center bg-light dark-surface p-2 rounded mt-1 border">
            <span>${escapeHtml(ev.model_answer_fr)}</span>
            <button type="button" class="btn btn-sm btn-outline-primary tts-btn play-fr-btn" data-fr="${escapeHtml(ev.model_answer_fr)}">
              <i class="fa-solid fa-volume-high"></i>
            </button>
          </div>
        </div>
      ` : ""}

      ${ev.follow_up_verification_question_fr ? `
        <div class="alert alert-warning small mb-0 mt-2 d-flex justify-content-between align-items-center gap-2">
          <div>
            <strong>🎤 Question orale supplémentaire de vérification :</strong><br>
            ${escapeHtml(ev.follow_up_verification_question_fr)}
          </div>
          <button type="button" class="btn btn-sm btn-outline-dark tts-btn play-fr-btn" data-fr="${escapeHtml(ev.follow_up_verification_question_fr)}">
            <i class="fa-solid fa-volume-high"></i>
          </button>
        </div>
      ` : ""}
    </div>
  `;

  $(containerSelector).html(html);
}

$(document).ready(function () {
  var currentLanguageIndex = 0;
  var prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
  var darkMode = prefersDarkScheme.matches;

  setDarkMode(darkMode);
  loadCurriculumData();
  loadStructuredCourseData();

  // Structured Course Event Handlers
  $(document).on("click", "#toggle-refresher-btn", function () {
    isRefresherOpen = !isRefresherOpen;
    renderCourseTrackerBanner();
    renderCourseRefresherPanel();
  });

  $(document).on("click", ".refresher-filter-btn", function () {
    refresherFilter = $(this).attr("data-filter");
    renderCourseRefresherPanel();
  });

  $(document).on("click", ".jump-to-course-module-btn", function () {
    selectedCourseModuleId = $(this).attr("data-mod-id");
    isRefresherOpen = false;
    renderCourseTrackerBanner();
    renderCourseRefresherPanel();
    renderCourseSidebar();
    renderCourseModuleDetail(selectedCourseModuleId);
  });

  $(document).on("click", "#flash-oral-quiz-btn", function () {
    if (allCourseModules.length === 0) return;
    const randomMod = allCourseModules[Math.floor(Math.random() * allCourseModules.length)];
    selectedCourseModuleId = randomMod.id;
    isRefresherOpen = false;
    renderCourseTrackerBanner();
    renderCourseRefresherPanel();
    renderCourseSidebar();
    renderCourseModuleDetail(selectedCourseModuleId);
    const oc = (randomMod.oral_challenges || [])[0];
    if (oc) {
      speakFrenchText(oc.prompt_fr, null);
    }
  });

  $(document).on("click", ".course-level-filter", function () {
    $(".course-level-filter").removeClass("btn-primary").addClass("btn-outline-primary");
    $(this).removeClass("btn-outline-primary").addClass("btn-primary");
    selectedCourseLevelFilter = $(this).attr("data-level");
    renderCourseSidebar();
  });

  $(document).on("click", ".toggle-review-flag-btn", function () {
    const modId = $(this).attr("data-mod-id");
    $.post("/api/toggle_course_review", { module_id: modId }, function (res) {
      if (res.progress) {
        courseProgress = res.progress;
        renderCourseTrackerBanner();
        renderCourseRefresherPanel();
        renderCourseSidebar();
        renderCourseModuleDetail(selectedCourseModuleId);
      }
    });
  });

  // Record Microphone for Structured Course Strict Oral Challenge
  $(document).on("click", ".course-oral-record-btn", function () {
    const $btn = $(this);
    const ocId = $btn.attr("data-oc-id");
    initAudio();

    if (activeOralRecordingId === ocId) {
      activeOralRecordingId = null;
      $btn.prop("disabled", true).removeClass("btn-warning").addClass("btn-danger").html('<i class="fa-solid fa-spinner fa-spin me-1"></i> Transcription...');
      stopRecording();
      activeOralBlobPromise.then(blob => {
        uploadAudio(blob).then(filename => {
          $.post("/transcribe_recording", { filename: filename }, function (res) {
            $btn.prop("disabled", false).html('<i class="fa-solid fa-microphone me-1"></i> Parler au micro');
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
      $btn.removeClass("btn-danger").addClass("btn-warning").html('<i class="fa-solid fa-stop me-1"></i> Arrêter l\'enregistrement');
      activeOralBlobPromise = startRecording();
    }
  });

  // Evaluate Strict Oral Challenge in Structured Course
  $(document).on("click", ".evaluate-course-oral-btn", function () {
    const $btn = $(this);
    const ocId = $btn.attr("data-oc-id");
    const modId = $btn.attr("data-mod-id");
    const promptText = $btn.attr("data-prompt");
    const mandatoryRaw = $btn.attr("data-mandatory") || "[]";
    const userVal = ($(`#course-oral-input-${ocId}`).val() || "").trim();

    if (!userVal) {
      showNotification("Parlez au micro ou écrivez votre réponse complète en français d'abord !");
      return;
    }

    initAudio();
    const origHtml = $btn.html();
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin me-1"></i> Évaluation stricte par Gemini...');

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
        renderCourseTrackerBanner();
        renderCourseSidebar();
      }
      renderStrictCourseEvaluation(res.evaluation, `#course-oral-feedback-${ocId}`);
      if (res.audio_url) {
        playSingleAudioFile(res.audio_url);
      }
    }).fail(function () {
      $btn.prop("disabled", false).html(origHtml);
    });
  });

  // Evaluate A2 Writing Task in Structured Course
  $(document).on("click", ".evaluate-course-wt-btn", function () {
    const $btn = $(this);
    const modId = $btn.attr("data-mod-id");
    const promptText = $btn.attr("data-prompt");
    const userVal = ($(`#course-wt-input-${modId}`).val() || "").trim();

    if (!userVal) {
      showNotification("Écrivez d'abord votre courriel / message A2.");
      return;
    }

    const origHtml = $btn.html();
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin me-1"></i> Vérification A2...');

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
        renderCourseTrackerBanner();
      }
      renderStrictCourseEvaluation(res.evaluation, `#course-wt-feedback-${modId}`);
    }).fail(function () {
      $btn.prop("disabled", false).html(origHtml);
    });
  });

  // Tab navigation
  $(document).on("click", ".tab-btn", function () {
    const tabId = $(this).data("tab");
    switchTab(tabId);
  });

  // Play any French snippet via TTS
  $(document).on("click", ".play-fr-btn", function () {
    const frText = $(this).attr("data-fr");
    speakFrenchText(frText, this);
  });

  // Jump from a class card to its Exercises tab
  $(document).on("click", ".go-practice-exercises-btn", function () {
    const classId = $(this).attr("data-class-id");
    selectedClassId = classId;
    $("#exercise-class-select").val(classId);
    renderExercisesForClass(classId);
    switchTab("tab-exercises");
  });

  // Jump from a class card or B1 simulator to Live Tutor Chat focused on that topic
  $(document).on("click", ".go-chat-class-btn", function () {
    const focusId = $(this).attr("data-class-id");
    $("#chat-focus-select").val(focusId);
    switchTab("tab-practice");
    startFocusedChat(focusId);
  });

  $("#jump-to-tutor-focus-btn").on("click", function () {
    const classId = $("#exercise-class-select").val();
    $("#chat-focus-select").val(classId);
    switchTab("tab-practice");
    startFocusedChat(classId);
  });

  $("#apply-chat-focus-btn").on("click", function () {
    const focusId = $("#chat-focus-select").val();
    startFocusedChat(focusId);
  });

  $("#begin-chat-btn").on("click", function () {
    initChat();
  });

  // Switch class inside Exercises tab
  $("#exercise-class-select").on("change", function () {
    selectedClassId = $(this).val();
    renderClassSidebar();
    renderClassDetail(selectedClassId);
    renderExercisesForClass(selectedClassId);
  });

  // Check Written Exercise (instant + rule explanation)
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
      showNotification("Écrivez d'abord votre réponse.");
      return;
    }

    const normalize = s => s.toLowerCase().replace(/[.!?]/g, "").replace(/\s+/g, " ").trim();
    const isMatch = accepted.some(a => normalize(a) === normalize(userVal)) || normalize(expected) === normalize(userVal);

    if (isMatch) {
      $.post("/api/mark_progress", { category: "completed_exercises", item_id: exId }, function (res) {
        if (res.progress) studyProgress = res.progress;
      });
      $(`#written-feedback-${exId}`).html(`
        <div class="feedback-box">
          <div class="fw-bold text-success small mb-1"><i class="fa-solid fa-circle-check me-1"></i> Bravo ! Réponse exacte : ${escapeHtml(expected)}</div>
          <div class="small text-muted">${escapeHtml(explanation)}</div>
        </div>
      `);
    } else {
      $(`#written-feedback-${exId}`).html(`
        <div class="feedback-box needs-work">
          <div class="fw-bold text-warning small mb-1"><i class="fa-solid fa-triangle-exclamation me-1"></i> Réponse attendue : <span class="text-primary">${escapeHtml(expected)}</span></div>
          <div class="small text-muted">${escapeHtml(explanation)}</div>
        </div>
      `);
    }
  });

  // Detailed AI Check for Written Exercise
  $(document).on("click", ".ai-check-written-btn", function () {
    const $btn = $(this);
    const exId = $btn.attr("data-ex-id");
    const classId = $btn.attr("data-class-id");
    const question = $btn.attr("data-question");
    const expected = $btn.attr("data-answer");
    const userVal = ($(`#written-input-${exId}`).val() || "").trim();

    if (!userVal) {
      showNotification("Écrivez d'abord votre réponse avant de demander l'analyse IA.");
      return;
    }

    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin"></i>');
    $.post("/api/evaluate_exercise", {
      class_id: classId,
      item_id: exId,
      prompt_text: question,
      user_answer: userVal,
      expected_answer: expected,
      mode: "written"
    }, function (res) {
      $btn.prop("disabled", false).html('<i class="fa-solid fa-robot"></i> Aide IA');
      if (res.error) {
        showNotification(res.error);
        return;
      }
      if (res.progress) studyProgress = res.progress;
      renderEvaluationCard(res.evaluation, `#written-feedback-${exId}`);
    });
  });

  // Record Oral Exercise Answer via Microphone
  $(document).on("click", ".oral-record-btn", function () {
    const $btn = $(this);
    const spId = $btn.attr("data-sp-id");
    initAudio();

    if (activeOralRecordingId === spId) {
      // Stop recording and transcribe
      activeOralRecordingId = null;
      $btn.prop("disabled", true).removeClass("btn-warning").addClass("btn-danger").html('<i class="fa-solid fa-spinner fa-spin me-1"></i> Transcription...');
      stopRecording();
      activeOralBlobPromise.then(blob => {
        uploadAudio(blob).then(filename => {
          $.post("/transcribe_recording", { filename: filename }, function (res) {
            $btn.prop("disabled", false).html('<i class="fa-solid fa-microphone me-1"></i> Parler au micro');
            if (res.error) {
              showNotification(res.error);
            }
            if (res.recorded_text) {
              const $input = $(`#oral-input-${spId}`);
              const existing = $input.val().trim();
              $input.val(existing ? existing + " " + res.recorded_text : res.recorded_text);
            }
          });
        });
      });
    } else {
      // Start recording
      activeOralRecordingId = spId;
      $btn.removeClass("btn-danger").addClass("btn-warning").html('<i class="fa-solid fa-stop me-1"></i> Arrêter l\'enregistrement');
      activeOralBlobPromise = startRecording();
    }
  });

  // Evaluate Spoken Answer with Gemini + Spoken Feedback
  $(document).on("click", ".evaluate-oral-btn", function () {
    const $btn = $(this);
    const spId = $btn.attr("data-sp-id");
    const classId = $btn.attr("data-class-id");
    const promptText = $btn.attr("data-prompt");
    const userVal = ($(`#oral-input-${spId}`).val() || "").trim();

    if (!userVal) {
      showNotification("Enregistrez votre voix au micro ou écrivez votre réponse d'abord !");
      return;
    }

    initAudio();
    const originalHtml = $btn.html();
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin me-1"></i> Analyse B1 par Renée...');

    $.post("/api/evaluate_exercise", {
      class_id: classId,
      item_id: spId,
      prompt_text: promptText,
      user_answer: userVal,
      mode: "speaking"
    }, function (res) {
      $btn.prop("disabled", false).html(originalHtml);
      if (res.error) {
        showNotification(res.error);
        return;
      }
      if (res.progress) studyProgress = res.progress;
      renderEvaluationCard(res.evaluation, `#oral-feedback-${spId}`);
      if (res.audio_url) {
        playSingleAudioFile(res.audio_url);
      }
    }).fail(function () {
      $btn.prop("disabled", false).html(originalHtml);
    });
  });

  // Generate Fresh AI Exercises for the Selected Class
  $("#generate-ai-exercises-btn").on("click", function () {
    const $btn = $(this);
    const classId = $("#exercise-class-select").val();
    const cls = curriculumClasses.find(c => c.id === classId);
    if (!cls) return;

    const orig = $btn.html();
    $btn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin me-1"></i> Génération IA en cours...');

    $.post("/api/generate_exercises", { class_id: classId }, function (res) {
      $btn.prop("disabled", false).html(orig);
      if (res.error) {
        showNotification(res.error);
        return;
      }
      if (res.generated) {
        if (res.generated.written_exercises) {
          cls.written_exercises = (cls.written_exercises || []).concat(res.generated.written_exercises);
        }
        if (res.generated.speaking_prompt) {
          cls.speaking_prompts = [res.generated.speaking_prompt].concat(cls.speaking_prompts || []);
        }
        renderExercisesForClass(classId);
      }
    }).fail(function () {
      $btn.prop("disabled", false).html(orig);
    });
  });

  // Native Dialog for Importing New Class PDF / Notes
  const importDialog = document.getElementById("import-class-dialog");
  $("#open-import-modal-btn").on("click", function () {
    $("#import-class-number").val(curriculumClasses.length + 1);
    if (importDialog && importDialog.showModal) {
      importDialog.showModal();
    }
  });
  $("#close-import-dialog-btn, #cancel-import-btn").on("click", function () {
    if (importDialog && importDialog.close) {
      importDialog.close();
    }
  });

  $("#import-class-form").on("submit", function (e) {
    e.preventDefault();
    const $submitBtn = $("#submit-import-btn");
    const origHtml = $submitBtn.html();
    $submitBtn.prop("disabled", true).html('<i class="fa-solid fa-spinner fa-spin me-1"></i> Analyse du PDF par Gemini...');

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
        if (res.classes) {
          curriculumClasses = res.classes;
        }
        if (res.new_class) {
          selectedClassId = res.new_class.id;
        }
        if (importDialog && importDialog.close) {
          importDialog.close();
        }
        renderClassSidebar();
        renderClassDetail(selectedClassId);
        populateClassSelectors();
        renderExercisesForClass(selectedClassId);
      },
      error: function () {
        $submitBtn.prop("disabled", false).html(origHtml);
        showNotification("Erreur lors de l'importation du cours.");
      }
    });
  });

  // =========================================================
  // EXISTING FREE PRACTICE TUTOR CHAT LOGIC
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
        if (error_message !== null) {
          showNotification(error_message);
        }
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
      recordButton.removeClass("btn-secondary off").addClass("btn-danger on");
      langToggleButton.removeClass("btn-secondary off").addClass("btn-danger on");
      recordedBlobPromise = startRecording();
    } else {
      recordButton.removeClass("btn-danger on").addClass("btn-secondary off");
      langToggleButton.removeClass("btn-danger on").addClass("btn-secondary off");
      toggleLoadingIcon("show");
      stopRecording();
      recordedBlobPromise.then(blob => {
        uploadAudio(blob).then(filename => {
          $.post("/transcribe_recording", { filename: filename }, function (response) {
            var recorded_text = response["recorded_text"];
            var error_message = response["error"];
            if (error_message !== null) {
              showNotification(error_message);
            }
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
          autoResize(textarea);
          toggleLoadingIcon("hide");
        });
      }).catch(error => {
        showNotification(error);
        autoResize(textarea);
        toggleLoadingIcon("hide");
      });
    }
  });

  Mousetrap.bindGlobal("alt+r", function (e) {
    if ($("#tab-practice").hasClass("active") && $("#record-button").attr("name") === "record") {
      e.preventDefault();
      $("#record-button").click();
    }
  });
  Mousetrap.bindGlobal("alt+l", function (e) {
    if ($("#tab-practice").hasClass("active") && $("#lang-toggle-button").attr("name") === "lang-record") {
      e.preventDefault();
      $("#lang-toggle-button").click();
    }
  });

  $("#message-input").keydown(function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      $("#message-form").submit();
      autoResize(this);
    } else if (event.key === "Enter" && event.shiftKey) {
      event.preventDefault();
      this.value += "\n";
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
    if (lang_button.hasClass("btn-danger on")) {
      return;
    } else if (lang_button.attr("name") === "pause") {
      pauseAudio();
      lang_button.attr("name", "unpause");
      lang_button.attr("title", "Unpause Audio");
      $("#pause-icon").removeClass("fa-pause").addClass("fa-play");
    } else if (lang_button.attr("name") === "unpause") {
      playAudio();
      lang_button.attr("name", "pause");
      lang_button.attr("title", "Pause Audio");
      $("#pause-icon").removeClass("fa-play").addClass("fa-pause");
    } else {
      currentLanguageIndex = (currentLanguageIndex + 1) % languages.length;
      $("#lang-text").text(languages[currentLanguageIndex]);
      $.post("/set_language", { language: languages[currentLanguageIndex] }, function () {});
    }
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
        showNotification("Aucune session sauvegardée trouvée.");
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
  var message_card = $('<div class="card flex-grow-1"></div>');
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
  if (has_user_recording && sender === "user") {
    var record_button = $('<div class="d-block"><button type="button" class="btn btn-link user-button play-user-button"><i class="fa-solid fa-user"></i></button></div>');
    button_container.append(record_button);
    record_button.on("click", function () {
      stopPlaying = false;
      $.post("/play_user_recording", { message_id: message_body.id }, function () {});
    });
  }
  if (sender === "user") {
    if (is_language_learning) {
      var sound_on_button = $('<div class="d-block"><button type="button" class="btn btn-link user-button sound-on-button"><i class="fas fa-volume-up"></i></button></div>');
      var translate_button = null;
      button_container.append(sound_on_button);
    } else {
      var sound_on_button = null;
      var translate_button = $('<div class="d-block"><button type="button" class="btn btn-link user-button translate-button"><i class="fa fa-language"></i></button></div>');
      button_container.append(translate_button);
    }
  } else {
    var translate_button = $('<div class="d-block"><button type="button" class="btn btn-link bot-button translate-button"><i class="fa fa-language"></i></button></div>');
    var sound_on_button = $('<div class="d-block"><button type="button" class="btn btn-link bot-button sound-on-button"><i class="fas fa-volume-up"></i></button></div>');
    button_container.append(translate_button);
    button_container.append(sound_on_button);
  }
  message_card.append(button_container);

  message_col.append(img).append(message_card);
  message_row.append(message_col);
  message_box.append(message_row);
  message_box.scrollTop(message_box.prop("scrollHeight"));

  var translated_message = false;
  if (translate_button !== null) {
    translate_button.on("click", function () {
      if (!translated_message) {
        $.post("/translate_text", { text: message_body.html(), sender: sender }, function (response) {
          var translated_text = (response["message"] || "").replace(/\n/g, "<br>");
          var original_text = message_body.html();
          var combined_text = original_text + "<hr><em>" + translated_text + "</em>";
          translated_message = true;
          message_body.html(combined_text);
        });
      }
    });
  }
  if (sound_on_button !== null) {
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
    var error_message = response["error"];
    if (error_message !== null) {
      showNotification(error_message);
    }
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
    bot_message = bot_message.replace(/\n/g, "<br>");
    updateLastMessage(bot_message);
    getNextMessage(message_index);
  });
}

function updateLastMessage(newContent) {
  var message_box = $("#message-box");
  var last_message_row = message_box.find(".row:last");
  var last_message_card_body = last_message_row.find(".card-body");
  last_message_card_body.html(newContent);
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
  toggleLoadingIcon("show");
  var message_box = $("#message-box");
  message_box.html("");
  for (var i = 0; i < messages.length; i++) {
    var msg = messages[i];
    addMessage(msg.role, msg.content, false, msg.is_language_learning, true);
  }
  toggleLoadingIcon("hide");
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
