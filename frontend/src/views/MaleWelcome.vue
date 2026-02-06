<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const handleNext = () => {
  router.push('/male/q/1');
};
</script>

<template>
  <div>
    <h1>Male Player's Turn</h1>
    <p>It's time for the male player to answer the questions.</p>
    <button @click="handleNext">Next</button>
  </div>
</template>