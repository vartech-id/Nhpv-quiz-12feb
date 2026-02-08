<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const player = computed(() => String(route.params.player)); // "male" / "female"
const sessionId = localStorage.getItem("sessionId");

const loading = ref(true);
const error = ref("");

const maleName = localStorage.getItem("maleName") || "Male";
const femaleName = localStorage.getItem("femaleName") || "Female";

const score = ref(null); // number 0..5
const resultImageUrl = ref("");

const playerLabel = computed(() => (player.value === "male" ? maleName : femaleName));

const title = computed(() => {
  if (score.value === null) return "";
  if (score.value === 5) return "WOW, Kamu sudah Peka banget sama Bahasa Pasanganmu!";
  if (score.value >= 3) return "Hebat!, Kamu Sudah Cukup Paham Bahasa Pasanganmu";
  return "Kamu masih belum Peka sama pasanganmu nih...";
});

const subtitle = computed(() => {
  if (score.value === null) return "";
  if (score.value === 5) return "";
  if (score.value >= 3) return "Bagus! Tinggal sedikit lagi menuju sempurna.";
  return "Yuk coba belajar lagi pahamin bahasa pasangan kamu, supaya hubungan kalian semakin langgeng!";
});

const scoreText = computed(() => {
  if (score.value === null) return "";
  return `for ${score.value}/5 Correct Answer`;
});

async function loadScore() {
  loading.value = true;
  error.value = "";

  if (!sessionId) {
    error.value = "Session belum ada. Balik ke Register.";
    loading.value = false;
    return;
  }

  try {
    const res = await fetch(`http://localhost:8000/couple-sessions/${sessionId}`);
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();

    if (player.value === "male") {
      score.value = data.male_score;
      resultImageUrl.value = data.male_result_image_url || "";
    } else if (player.value === "female") {
      score.value = data.female_score;
      resultImageUrl.value = data.female_result_image_url || "";
    } else throw new Error("Invalid player param");

    if (score.value === null || score.value === undefined) {
      throw new Error("Score belum tersedia. Pastikan sudah submit jawaban.");
    }
  } catch (e) {
    error.value = e?.message || "Gagal load score";
  } finally {
    loading.value = false;
  }
}

function handleNext() {
  if (player.value === "male") router.push("/female/welcome");
  else router.push("/");
}

onMounted(() => {
  loadScore();
});
</script>

<template>
  <div class="result-wapper">
    <!-- <h1>RESULT</h1> -->

    <div v-if="loading">Loading...</div>

    <div v-else-if="error">
      <p>{{ error }}</p>
      <button @click="router.push('/register')">Back to Register</button>
    </div>

    <div class="result" v-else>
      <!-- <p>Player: {{ playerLabel }}</p>

      <h2>{{ title }}</h2>
      <p>{{ subtitle }}</p>

      <p>{{ scoreText }}</p> -->
      <img class="result-image" :src="resultImageUrl" alt="result-image">

      <button class="next-btn" @click="handleNext">
        {{ player === "male" ? "NEXT" : "NEXT" }}
      </button>
    </div>
  </div>
</template>
<style>
.result {
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 2rem;
}

.result-image{ 
  max-width: 80%;
}
</style>
