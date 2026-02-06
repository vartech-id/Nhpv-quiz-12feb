<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const handleNext = () => {
  router.push('/');
};
</script>

<template>
  <div>
    <h1>Quiz Completed!</h1>
    <p>Thank you for taking the couple quiz challenge.</p>
    <button @click="handleNext">Back to Welcome</button>
  </div>
</template>