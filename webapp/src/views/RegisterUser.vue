<template>
  <form @submit.prevent="register">
    <label for="username">Username</label>
    <input
      v-model="username"
      type="text"
      id="username"
      placeholder="username"
      required
    />
    <br />
    <label for="passw">Password</label>
    <input
      v-model="password"
      type="password"
      id="passw"
      placeholder="password"
      required
      :pattern="`^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?!.*${username}).*`"
      title="
              At least one number, one uppercase and lowercase letter.
              At least 8 or more characters.
              Additionally can't contain the username"
      minlength="8"
    />
    <br />
    <button type="submit">Register</button>
    <br />
    <br />

    <!-- <router-link to="/register">Don't have an account? Register</router-link>
      title="&#010;&#013;At least one number, one uppercase and lowercase letter.&#010;At least 8 or more characters.&#010;Additionally can't contain the username"-->
  </form>
</template>

<script lang="ts" setup>
import { useUserStore } from "@/stores/user";
import { ref } from "vue";
import type { Ref } from "vue";
import { API_LOCATION } from "@/../config";

const username: Ref<string> = ref("");
const password: Ref<string> = ref("");

function register() {
  console.log(password);
  fetch(API_LOCATION + "/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: username.value,
      password: password.value,
    }),
  })
    // if not ok
    .then((res) => {
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      return res.json();
    })
    .then((data) => {
      const user = useUserStore();
      user.login(data);
    });
}
</script>

<style>
input {
  color: black;
}
</style>
