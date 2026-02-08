<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const exports = async () => {
  try {
    const response = await fetch("http://localhost:8000/reports/couple-results.xlsx");
    if (!response.ok) {
      throw new Error(`Export failed: ${response.status}`);
    }

    const blob = await response.blob();
    const fileUrl = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = fileUrl;
    link.download = "couple-results.xlsx";
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(fileUrl);
  } catch (error) {
    console.error("Error exporting results:", error);
    alert("Failed to export Excel file. Please try again.");
  }
};

const handleNext = () => {
  router.push("/register");
};

</script>
<template>
  <div id="export-page">
    <div class="action-button">
      <button @click="exports" class="btn">EXPORT</button>
      <button @click="handleNext" class="btn">HOME!</button>
    </div>
  </div>
</template>
<style>
#export-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: aquamarine;
  gap: 3rem;
  width: 100%;
  background-image: url(../assets/bg-quiz.png);
  height: 100vh;
}

.title {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.title > h1 {
  font-size: 5rem;
  font-family: var(--font-welcome);
  color: var(--color-text)
}
</style>
