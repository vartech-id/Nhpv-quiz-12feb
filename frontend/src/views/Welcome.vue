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
    <button @click="handleNext" class="welcome btn">MULAI!</button>
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
}
.title {
  font-size: 2.2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
</style>
