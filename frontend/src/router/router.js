import { createRouter, createWebHistory } from "vue-router";
import Home from "../components/Home.vue";
import ChatPanel from "../components/ChatPanel.vue"

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/chat",
    name: "chat",
    component: ChatPanel
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
