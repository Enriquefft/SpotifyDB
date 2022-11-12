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

const username: string = "";
const password: string = "";
const rememberMe: boolean = false;

async function login() {
  await fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      data.remember_user = rememberMe;
      const user = useUserStore();
      user.login(data);
    })
    // catch errors
    .catch((error) => console.error(error));
}
</script>
