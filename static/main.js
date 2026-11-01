$.getScript("/static/common.js");
$.getScript("/static/audio.js");

let curriculumClasses = [];
let b1Roadmap = null;
let studyProgress = { completed_exercises: [], completed_speaking: [], mastered_classes: [] };
let selectedClassId = "class-11"; // Default to latest class (Class 11) so user sees their current lesson immediately
let activeOralRecordingId = null;
let activeOralBlobPromise = null;

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

$(document).ready(function () {
  var currentLanguageIndex = 0;
  var prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
  var darkMode = prefersDarkScheme.matches;

  setDarkMode(darkMode);
  loadCurriculumData();

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
