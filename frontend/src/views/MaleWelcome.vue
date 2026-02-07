<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const handleNext = () => {
  router.push("/male/q/1");
};
</script>

<template>
  <div class="welcome-male greeting">
    <div class="male-wording">
      <h1>LADIES, SANTAI DULU</h1>
      <h1>SAATNYA PASANGAN LAKI-</h1>
      <h1>LAKI DULU YANG MENJAWAB</h1>
    </div>

    <button class="next-btn" @click="handleNext">NEXT</button>
  </div>
</template>
<style>
.welcome-male {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: aqua;
  width: 100%;
  gap: 3rem;
}

.male-wording {
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
