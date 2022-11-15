<template>
  <form @submit.prevent="login">
    <label for="username">Username</label>
    <input
      v-model="username"
      id="username"
      type="text"
      placeholder="username"
    />
    <br />
    <label for="password">Username</label>
    <input
      v-model="password"
      id="password"
      type="password"
      placeholder="password"
    />
    <br />
    <label for="remember_me">Remember me</label>
    <input v-model="rememberMe" id="remember_me" type="checkbox" />
    <br />
    <button type="submit">Login</button>
    <br />
    <br />

    <!-- <router-link to="/register">Don't have an account? Register</router-link> -->
  </form>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/stores/user";
import { ref } from "vue";
import type { Ref } from "vue";
import { API_LOCATION } from "@/../config";

const username: Ref<string> = ref("");
const password: Ref<string> = ref("");
const rememberMe: Ref<boolean> = ref(false);

async function login() {
  await fetch(API_LOCATION, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
    }),
  })
    .then((res) => {
      if (!res.ok) {
        throw Error(res.statusText);
      }
      return res.json();
    })
    .then((data) => {
      data.remember_user = rememberMe.value;
      const user = useUserStore();
      user.login(data);
    })
    // catch errors
    .catch((error) => console.error(error));
}
</script>
