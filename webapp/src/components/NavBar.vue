<template class>
  <header class="flex flex-row mx-auto items-center bg-gray-800">
    <div class="left-0 flex">
      <picture> </picture>

      <h1>SpotifyDB</h1>
    </div>

    <nav class="w-full">
      <ul class="flex mx-auto justify-around">
        <li v-for="link in links" :key="link">
          <router-link :to="{ name: link }">{{ link }}</router-link>
        </li>
      </ul>
    </nav>

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
defineProps<{
  links: string[];
}>();
</script>
