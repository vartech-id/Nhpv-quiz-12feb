<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const handleNext = () => {
  router.push("/male/q/1");
};
</script>

<template>
  <div class="welcome-male greeting">
    <div class="subgreeting">
      <h1>Ladies, santai dulu</h1>
      <h1>saatnya pasangan laki-</h1>
      <h1>laki dulu yang menjawab</h1>
    </div>
    <div class="action-button">
      <button class="btn" @click="handleNext">NEXT</button>
    </div>
  </div>
</template>
<style>
.greeting {
  height: 100vh;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background-image: url(..//assets/bg-quiz.png);
  gap: 3.5rem;
}

.subgreeting {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-family: var(--font-welcome);
  color: var(--color-text);
  font-size: 2.4rem;
  width: 100%;
}
</style>
