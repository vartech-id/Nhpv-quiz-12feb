<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const handleNext = () => {
  router.push('/female/welcome');
};
</script>

<template>
  <div>
    <h1>Switch Players</h1>
    <p>Please switch with your partner now.</p>
    <button @click="handleNext">Next</button>
  </div>
</template>