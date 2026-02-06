<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const handleNext = () => {
  router.push('/register');
};
</script>
<template>
  <div>
    <h1>Couple Quiz Challenge</h1>
    <p>How well do you know each other?</p>
    <button @click="handleNext">Next</button>
  </div>
</template>