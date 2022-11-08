<template>
  <form @submit.prevent="login">
    <label for="username">Username</label>
    <input type="text" v-model="username" placeholder="username" />
    <br />
    <label for="password">Username</label>
    <input v-model="password" placeholder="password" type="password" />
    <br />
    <button type="submit">Login</button>
    <br />
    <br />

    <!-- <router-link to="/register">Don't have an account? Register</router-link> -->
  </form>
</template>

<script lang="ts" setup>
import { ref } from "vue";

const username = ref("");
const password = ref("");

function login() {
  console.log("login");
  fetch("http://127.0.0.1:5000/", {
    method: "PUT",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      username: username.value,
      password: password.value,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
    });
}
</script>
