import { createRouter, createWebHistory } from "vue-router";

export const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomeView.vue"),
    restrictions: [],
  },
  {
    path: "/about",
    name: "about",
    component: () => import("@/views/AboutView.vue"),
    restrictions: [],
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginUser.vue"),
    restrictions: ["unlogged"],
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/RegisterUser.vue"),
    restrictions: ["unlogged"],
  },
  /*
  {
    path: "/playlist/:name",
    name: "playlist",
    component: () => import("@/views/PlaylistView.vue"),
  },
  */
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
