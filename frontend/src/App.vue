<script setup>
import { RouterView, useRoute } from "vue-router";
const route = useRoute();
</script>

<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" :key="route.fullPath" />
    </transition>
  </router-view>
</template>
<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.btn {
  color: #dddc25;
  background-color: white;
  width: 25%;
  font-size: 2.5rem;
  border: none;
  border-radius: 1.6rem;
  padding: 0.5rem;
  background-image: linear-gradient(to top, #244f53, #3b878f);
  font-family: var(--font-btn);
  padding-top: 0.7rem;
  padding-bottom: 0.7rem;
}

.action-button {
  width: 100%;
  display: flex;
  justify-content: center;
}

</style>
