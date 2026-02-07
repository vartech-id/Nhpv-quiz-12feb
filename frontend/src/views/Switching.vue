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
    <p>SAATNYA MEMBALAS</p>
    <p>PASANGAN WANITA</p>
    <p>SEKARANG GILIRANMU!</p>
    <button @click="handleNext">Next</button>
  </div>
</template>