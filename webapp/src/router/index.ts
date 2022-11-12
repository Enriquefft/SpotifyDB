import { createRouter, createWebHistory } from "vue-router";

export const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomeView.vue"),
  },
  {
    path: "/about",
    name: "about",
    component: () => import("@/views/AboutView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginUser.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/RegisterUser.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
