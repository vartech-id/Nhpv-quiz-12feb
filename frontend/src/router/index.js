import { createRouter, createWebHistory } from "vue-router";

import Welcome from "../views/Welcome.vue";
import Register from "../views/Register.vue";
import MaleWelcome from "../views/MaleWelcome.vue";
import FemaleWelcome from "../views/FemaleWelcome.vue";
import Question from "../views/Question.vue";
import Score from "../views/Score.vue";
import Switching from "../views/Switching.vue";
import EndPage from "../views/EndPage.vue";

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "Welcome", component: Welcome },
    { path: "/register", name: "Register", component: Register },

    { path: "/male/welcome", name: "MaleWelcome", component: MaleWelcome },
    { path: "/female/welcome", name: "FemaleWelcome", component: FemaleWelcome },

    { path: "/:player(male|female)/q/:no", name: "Question", component: Question },
    { path: "/:player(male|female)/score", name: "Score", component: Score },

    { path: "/switching", name: "Switching", component: Switching },
    { path: "/end", name: "EndPage", component: EndPage },
  ],
});