<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const answer = ref(""); // jawaban final yang sudah dikunci
const pendingChoice = ref(""); // pilihan menunggu konfirmasi

const questions = ref([]);
const answers = ref([]);

const showFeedback = ref(false);
const isCorrect = ref(false);
const isLocked = ref(false);

const showConfirm = ref(false);

const player = computed(() => route.params.player);
const no = computed(() => Number(route.params.no));
const idx = computed(() => no.value - 1);

const sessionId = localStorage.getItem("sessionId");
const currentQuestion = computed(() => questions.value[idx.value] || null);
const correctSfx = new Audio("/correct.mp3");
const wrongSfx = new Audio("/wrong.mp3");

correctSfx.preload = "auto";
wrongSfx.preload = "auto";

function playAnswerSfx(correct) {
  const sfx = correct ? correctSfx : wrongSfx;
  sfx.currentTime = 0;
  sfx.play().catch(() => {
    // ignore autoplay-block errors
  });
}

function resetQuestionUI() {
  pendingChoice.value = "";
  showConfirm.value = false;
  showFeedback.value = false;
  isCorrect.value = false;
  isLocked.value = false;
}

async function loadQuestionsOnce() {
  const cacheKey = `questions_${sessionId}_${player.value}`;
  const cached = localStorage.getItem(cacheKey);

  const cachedAnswersKey = `answers_${sessionId}_${player.value}`;
  const cachedAnswers = localStorage.getItem(cachedAnswersKey);

  if (cached) {
    questions.value = JSON.parse(cached);
    answers.value = cachedAnswers
      ? JSON.parse(cachedAnswers)
      : Array(5).fill(null);

    const saved = answers.value[idx.value];
    answer.value = saved || "";

    resetQuestionUI();
    if (answer.value && currentQuestion.value) {
      isLocked.value = true;
      showFeedback.value = true;
      isCorrect.value = answer.value === currentQuestion.value.correct_answer;
    }
    return;
  }

  const res = await fetch(
    `http://localhost:8000/couple-sessions/${sessionId}/questions?player=${player.value}`,
  );
  if (!res.ok) throw new Error(await res.text());
  const data = await res.json();

  questions.value = data.questions;
  answers.value = Array(5).fill(null);

  localStorage.setItem(cacheKey, JSON.stringify(questions.value));
  localStorage.setItem(cachedAnswersKey, JSON.stringify(answers.value));

  answer.value = "";
  resetQuestionUI();
}

function requestSelect(v) {
  if (isLocked.value) return;
  pendingChoice.value = v;
  showConfirm.value = true;
}

function confirmNo() {
  showConfirm.value = false;
  pendingChoice.value = "";
}

function confirmYes() {
  if (!currentQuestion.value) return;

  showConfirm.value = false;

  answer.value = pendingChoice.value;
  pendingChoice.value = "";

  answers.value[idx.value] = answer.value;
  localStorage.setItem(
    `answers_${sessionId}_${player.value}`,
    JSON.stringify(answers.value),
  );

  isLocked.value = true;
  showFeedback.value = true;
  isCorrect.value = answer.value === currentQuestion.value.correct_answer;
  playAnswerSfx(isCorrect.value);
}

function buttonClass(choice) {
  let cls = "opt";

  // sementara selected saat confirm
  if (pendingChoice.value === choice && showConfirm.value) {
    cls += " opt-selected";
  }

  // setelah locked: warnai hanya pilihan yang dipilih
  if (showFeedback.value && answer.value === choice) {
    cls += isCorrect.value ? " opt-correct" : " opt-wrong";
  }

  return cls;
}

/** icon visibility: selalu ada, tapi hidden sampai jawab */
function iconVisibleFor(choice) {
  return showFeedback.value && answer.value === choice;
}

/** text sementara (nanti kamu ganti jadi img) */
function iconText() {
  return isCorrect.value ? "✓" : "✗";
}

async function handleNext() {
  if (!answer.value) {
    alert("Kamu harus pilih A atau B dulu");
    return;
  }

  if (no.value < 5) {
    router.push(`/${player.value}/q/${no.value + 1}`);
    return;
  }

  const missingIndex = answers.value.findIndex((v) => !v);
  if (missingIndex !== -1) {
    alert(`Soal nomor ${missingIndex + 1} belum dijawab.`);
    router.push(`/${player.value}/q/${missingIndex + 1}`);
    return;
  }

  const payload = {
    player: player.value,
    answers: questions.value.map((q, i) => ({
      question_id: q.id,
      answer: answers.value[i],
    })),
  };

  const res = await fetch(
    `http://localhost:8000/couple-sessions/${sessionId}/submit`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
  );

  if (!res.ok) throw new Error(await res.text());
  await res.json();

  router.push(`/${player.value}/score`);
}

onMounted(async () => {
  await loadQuestionsOnce();
});

watch([player, no], () => {
  if (!questions.value.length) return;

  const saved = answers.value[idx.value];
  answer.value = saved || "";

  resetQuestionUI();
  if (answer.value && currentQuestion.value) {
    isLocked.value = true;
    showFeedback.value = true;
    isCorrect.value = answer.value === currentQuestion.value.correct_answer;
  }
});
</script>

<template>
  <div id="quiz-page">
    <div class="quiz-dom" v-if="currentQuestion">
      <!-- <h1>Question {{ no }}/5</h1> -->
      <h1 class="questions">{{ currentQuestion.question_text }}</h1>
      <div class="option-wrapper">
        <!-- Opsi A -->
        <div class="option-a selections">
          <button
            class="A row"
            :class="buttonClass('A')"
            @click="requestSelect('A')"
            :disabled="isLocked"
          >
            <h1 class="tag-option">A.</h1>
            <span>{{ currentQuestion.option_a }}</span>
          </button>
          <!-- icon slot selalu ada -->
          <div class="iconSlot" :class="{ show: iconVisibleFor('A') }">
            <!-- sementara text, nanti ganti ke img -->
            <span class="iconText">{{ iconText() }}</span>
          </div>
        </div>

        <div class="option-b selections">
          <button
            class="B row"
            :class="buttonClass('B')"
            @click="requestSelect('B')"
            :disabled="isLocked"
          >
            <h1 class="tag-option">B.</h1>
            <span>{{ currentQuestion.option_b }}</span>
          </button>
          <!-- icon slot selalu ada -->
          <div class="iconSlot" :class="{ show: iconVisibleFor('B') }">
            <!-- sementara text, nanti ganti ke img -->
            <span class="iconText">{{ iconText() }}</span>
          </div>
        </div>
      </div>

      <button class="next-btn" @click="handleNext">NEXT</button>

      <!-- Confirm modal -->
      <div v-if="showConfirm" class="modal-backdrop">
        <div class="modal">
          <h2>Anda yakin pilih {{ pendingChoice }}?</h2>
          <div class="modal-actions">
            <button class="modal-btn" @click="confirmYes">YA</button>
            <button class="modal-btn" @click="confirmNo">TIDAK</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else>Loading...</div>
  </div>
</template>

<style>
#quiz-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  background-color: rgb(125, 125, 255);
}

.quiz-dom {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  background-color: rgb(220, 255, 125);
  gap: 1.5rem;
}

.questions {
  font-size: 3.4rem;
  text-align: center;
}

.option-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: aqua;
  width: 100%;
  background-color: 10px solid blue;
  gap: 2rem;
}

.selections {
  display: flex;
  /* background-color: rgb(255, 255, 255); */
  justify-content: center;
  align-items: center;
  width: 90%;
  margin-left: 3rem;
}

.row {
  display: flex;
  width: 100%;
  gap: 1rem;
  min-height: 110px;
  border-radius: 40px;
  padding-left: 0;
  border: none;
  align-items: stretch;
  color: #124F5A;
}

.A{
    background-image: linear-gradient(to top, #66CBE4, #A5DAEC);
}

.B{
    background-image: linear-gradient(to top, #E3C726, #fff677);
}

span {
  text-align: left;
  /* border: 2px solid yellow; */
}

.row span {
  font-size: 2.2rem;
  line-height: 1.1;
  white-space: normal;
  min-width: 0;
  flex: 1;

  /* center vertikal */
  display: flex;
  align-items: center; /* ✅ bikin teks di tengah vertikal */

  /* biar ada jarak kanan */
  padding-right: 16px;
}

.row > button {
  font-size: 1rem;
  width: 100%;
  text-align: left;
  border: none;
}

.tag-option {
  background-color: aliceblue;
  padding: 0; /* biar centernya akurat */
  min-width: 120px; /* optional: biar lebar badge konsisten */
  min-height: 110px; /* sama seperti .row */
  border-radius: 40px 40px 40px 40px;
  color:  #124F5A;
  display: flex;
  align-items: center; /* center vertikal */
  justify-content: center; /* center horizontal */
  font-size: 2.5rem;
  font-weight: 200;
  margin: -1px;
}

/* state */
/* .opt-selected {
  border: 6px solid #999;
} */

.opt-correct {
  border: 6px solid green;
}
.opt-wrong {
  border: 6px solid red;
}

/* icon slot selalu ambil tempat, tapi hide dulu */
.iconSlot {
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  /* background-color: rgb(255, 0, 0); */
  visibility: hidden; /* tempat tetap ada */
}
.iconSlot.show {
  visibility: visible;
}

.iconText {
  font-weight: 700;
  font-size: 3rem;
}

/* MODAL ACTIONS */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  z-index: 20;
  backdrop-filter: blur(4px);
}

.modal {
  background: #F2E8D6;
  border-radius: 32px;
  padding: clamp(2rem, 5vw, 3rem);
  text-align: center;
  color: #fff;
  min-width: min(rem, 90vw);
  min-height: min(30rem, 90vw);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.35);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.modal > h2 {
  font-size: 84px;
  margin: 0 0 5rem;
  font-weight: 700;
  font-family: "Poppins", sans-serif;
  font-style: normal;
  color: #124F5A;
}

.modal-actions {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.modal-btn {
  min-width: 20rem;
  padding: 1rem 2.5rem;
  font-size: 3.5rem;
  border-radius: 999px;
  cursor: pointer;
  transition:
    transform 150ms ease,
    box-shadow 150ms ease;
      color: #dddc25;
  background-image: linear-gradient(to top, #244f53, #3b878f);
  border: none;
}
</style>
