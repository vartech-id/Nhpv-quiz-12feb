<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const handleNext = () => {
  router.push("/register");
};
</script>
<template>
  <div id="welcome-page">
    <div class="title">
      <h1>Sudah pahamkah kamu</h1>
      <h1>dengan kata-kata</h1>
      <h1>pasanganmu ?</h1>
    </div>
    <div class="action-button">
      <button @click="handleNext" class="welcome btn">MULAI!</button>
    </div>
  </div>
</template>
<style>
#welcome-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: aquamarine;
  gap: 3rem;
  width: 100%;
  background-image: url(../assets/bg-quiz.png);
  height: 100vh;
}
.title {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.title > h1 {
  font-size: 5rem;
  font-family: var(--font-welcome);
  color: var(--color-text)
}
</style>
