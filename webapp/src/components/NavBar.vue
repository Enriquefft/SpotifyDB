<template>
  <header class="flex flex-row mx-auto items-center bg-gray-800">
    <div class="left-0 flex">
      <picture> </picture>

      <h1>SpotifyDB</h1>
    </div>

    <nav class="w-full">
      <ul class="flex mx-auto justify-around">
        <li v-for="link in allowedRoutes" :key="link">
          <router-link :to="{ name: link }">{{ link }}</router-link>
        </li>
      </ul>
    </nav>

    <!--logout-->
    <div v-if="userStore.logged_in" class="right-0 flex">
      <button @click="userStore.logout">Logout</button>
    </div>

    <div class="right-0 flex">
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
</script>
