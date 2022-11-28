<template>
  <header class="flex flex-row mx-auto items-center bg-gray-800">
    <div class="left-0 flex">
      <picture> </picture>

      <h1>SpotifyDB</h1>
    </div>

    <nav class="w-full">
      <ul class="flex mx-auto justify-around">
        <li v-for="link in allowedRoutes" :key="link">
          <routerLink :to="{ name: link }">{{ link }}</routerLink>
        </li>
      </ul>
    </nav>

    <div v-if="!userStore.isAuthorized">
      <button @click="authorize">authorize</button>
    </div>
    <!--logout-->
    <div v-if="userStore.isLoggedIn" class="right-0 flex">
      <button @click="userStore.logout">Logout</button>
    </div>

    <div v-if="userStore.isAuthorized" class="right-0 flex">
      <button>Send Query</button>

      <a>
        <figure>
          <picture />
          <figcaption>Profile</figcaption>
        </figure>
      </a>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useUserStore } from "@/stores/user";
import { API_LOCATION } from "@/../config";

const userStore = useUserStore();

type Link = {
  name: string;
  restrictions: string[];
};
const props = defineProps<{
  links: Link[];
}>();

const allowedRoutes = computed(() => {
  return props.links
    .filter((link) => {
      return link.restrictions.every((restriction) =>
        userStore.permits.includes(restriction)
      );
    })
    .map((link) => link.name);
});

function authorize() {
  console.log("authorizing");
  fetch(`${API_LOCATION}/authorize`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${userStore.access_token}`,
    },
  })
    .then((res) => {
      if (res.ok) {
        return res.json();
      } else {
        throw new Error("Authorization failed");
      }
    })
    .then((data) => {
      console.log(data.redirect);
      window.location.href = data.redirect;
    })
    .catch((error) => {
      console.log(error);
    });
}
</script>
