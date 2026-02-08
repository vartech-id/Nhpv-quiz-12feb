<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const handleNext = () => {
  router.push("/female/q/1");
};
</script>

<template>
  <div class="welcome-female greeting">
    <div class="subgreeting">
      <h1>Saatnya membalas!</h1>
      <h1>pasangan wanita</h1>
      <h1>sekarang giliranmu!</h1>
    </div>
    <div class="action-button">
      <button class="btn" @click="handleNext">NEXT</button>
    </div>
  </div>
</template>
