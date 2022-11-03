import { defineStore } from "pinia";

import { ref,  }

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
  }),
  actions: {
    async fetchUser() {
      const res = await fetch("https://localhost:3000/user");

      const user = await res.json();
      this.user = user;
    },
    async signUp(email, password) {
      const res = await fetch("https://localhost:3000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
      const user = await res.json();
      this.user = user;
    },
    async signIn(email, password) {
      const res = await fetch("https://localhost:3000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
      const user = await res.json();
      this.user = user;
    },
  },
});

export const UserStore = defineStore('user', () => {
  const user = ref(null)
  async function fetchUser() {
    const response = await fetch('https://spotify-db.vercel.app/user')
  }
})
