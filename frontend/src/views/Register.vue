<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const maleName = ref("");
const femaleName = ref("");

const forceUppercase = (event) => {
  return event.target.value.toUpperCase();
};

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

</script>

<template>
  <div id="register-page">
    <div class="register-msg">
      <h1>Silahkan Tuliskan Nama</h1>
      <h1>masing - masing</h1>
    </div>
    <div class="form-wrapper">
      <form class="register form" @submit.prevent>
          <label for="maleName">Nama Pasangan Pria:</label>
          <input id="maleName" v-model="maleName" @input="maleName = forceUppercase($event)" type="text" required />
          <label for="femaleName">Nama Pasangan Wanita:</label>
          <input id="femaleName" v-model="femaleName" @input="femaleName = forceUppercase($event)" type="text" required />
      </form>
    </div>
    <div class="action-button">
      <button class="btn" type="submit" @click="handleSubmit">NEXT</button>
    </div>
  </div>
</template>
<style>
#register-page {
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

.register-msg {
  font-size: 1.8rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: var(--color-text);
}

.register-msg > h1 {
  font-family: var(--font-text);
}

.form-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}

form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  color: var(--color-text);
  font-family: var(--font-text);
  gap: 2.2rem; 
}


label {
  font-size: 2.8rem;
  margin-bottom: -1rem;
}

input {
  width: 70%;
  font-size: 3rem;
  font-family: var(--font-text);
  color: var(--color-text);
  text-align: center;
  background: transparent;        
  border: none;                   
  border-bottom: 4px solid var(--color-text); 
  padding: 1rem 0.8rem;         
  outline: none;
}

input:focus {
  border-bottom: 4px solid var(--color-text);
}


input::placeholder {
  color: rgba(0, 0, 0, 0.35);
}

</style>
