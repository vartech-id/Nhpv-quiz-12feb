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
    <button class="next-btn" @click="handleNext">NEXT</button>
  </div>
</template>
<style>
.greeting {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: aqua;
  width: 100%;
  gap: 3rem;
}

.subgreeting {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: aqua;
  font-size: 1.7rem;
  gap: 1rem;
  width: 100%;
}
</style>
