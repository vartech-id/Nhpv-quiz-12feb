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
  <div v-if="currentQuestion">
    <h1>Question {{ no }}/5</h1>
    <p>{{ currentQuestion.question_text }}</p>

    <!-- Opsi A -->
    <div class="row">
      <button
        class="btn"
        :class="buttonClass('A')"
        @click="requestSelect('A')"
        :disabled="isLocked"
      >
        <span>{{ currentQuestion.option_a }}</span>
      </button>

      <!-- icon slot selalu ada -->
      <div class="iconSlot" :class="{ show: iconVisibleFor('A') }">
        <!-- sementara text, nanti ganti ke img -->
        <span class="iconText">{{ iconText() }}</span>
      </div>
    </div>

    <!-- Opsi B -->
    <div class="row">
      <button
        class="btn"
        :class="buttonClass('B')"
        @click="requestSelect('B')"
        :disabled="isLocked"
      >
        <span>{{ currentQuestion.option_b }}</span>
      </button>

      <div class="iconSlot" :class="{ show: iconVisibleFor('B') }">
        <span class="iconText">{{ iconText() }}</span>
      </div>
    </div>

    <button @click="handleNext">Next</button>

    <!-- Confirm modal -->
    <div v-if="showConfirm" class="modalOverlay">
      <div class="modalBox">
        <p>Anda yakin pilih {{ pendingChoice }}?</p>
        <button @click="confirmYes">Yes</button>
        <button @click="confirmNo">No</button>
      </div>
    </div>
  </div>

  <div v-else>Loading...</div>
</template>

<style scoped>
/* row layout: button + icon di kanan */
.row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
}

.btn {
  flex: 1;
  border: 2px solid transparent;
  padding: 12px 14px;
  text-align: left;
}

/* state */
.opt-selected {
  border-color: #999;
}
.opt-correct {
  border-color: green;
}
.opt-wrong {
  border-color: red;
}

/* icon slot selalu ambil tempat, tapi hide dulu */
.iconSlot {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;

  visibility: hidden; /* tempat tetap ada */
}
.iconSlot.show {
  visibility: visible;
}

.iconText {
  font-weight: 700;
}

.modalOverlay {
  position: fixed;
  inset: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  background: rgba(0, 0, 0, 0.5); /* ✅ hitam 50% */
}

.modalBox {
  border: 1px solid #ccc;
  padding: 16px;
  background: white;
  color: black;
}
</style>
