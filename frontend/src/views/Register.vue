<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const maleName = ref("");
const femaleName = ref("");

const handleSubmit = async () => {
  try {
    const response = await fetch("http://localhost:8000/couple-sessions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        male_name: maleName.value,
        female_name: femaleName.value,
      }),
    });

    if (!response.ok) throw new Error(await response.text());

    const result = await response.json();

    // simpan sessionId & nama
    localStorage.setItem("sessionId", String(result.id));
    localStorage.setItem("maleName", maleName.value);
    localStorage.setItem("femaleName", femaleName.value);

    // optional: bersihin cache jawaban/soal sesi lain (kalau perlu)
    localStorage.removeItem(`questions_${result.id}_male`);
    localStorage.removeItem(`questions_${result.id}_female`);
    localStorage.removeItem(`answers_${result.id}_male`);
    localStorage.removeItem(`answers_${result.id}_female`);

    router.push("/male/welcome");
  } catch (error) {
    console.error("Error creating session:", error);
    alert("Failed to start quiz. Please try again.");
  }
};

onMounted(() => {
  maleName.value = "Male test dev";
  femaleName.value = "Female test dev";
});
</script>


<template>
  <div>
    <h1>Register Players</h1>
    <form @submit.prevent="handleSubmit">
      <div>
        <label for="maleName">Male Name:</label>
        <input id="maleName" v-model="maleName" type="text" required />
      </div>
      <div>
        <label for="femaleName">Female Name:</label>
        <input id="femaleName" v-model="femaleName" type="text" required />
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>
