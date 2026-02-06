<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const handleNext = () => {
  router.push('/female/q/1');
};
</script>

<template>
  <div>
    <h1>Female Player's Turn</h1>
    <p>It's time for the female player to answer the questions.</p>
    <button @click="handleNext">Next</button>
  </div>
</template>