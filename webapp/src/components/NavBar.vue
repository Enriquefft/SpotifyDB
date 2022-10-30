<template class>
  <header class="flex flex-row mx-auto items-center bg-gray-800">
    <div class="left-0 flex">
      <picture> </picture>

      <h1>SpotifyDB</h1>
    </div>

    <nav class="w-full">
      <ul class="flex mx-auto justify-around">
        <li v-for="link in links" :key="link.id">
          <router-link :to="link.route">{{ link.label }}</router-link>
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

<script lang="ts">
type Link = {
  id: number;
  label: string;
  icon: string;
  route: string;
};

interface NavBarProps {
  links: Link[];
}
</script>
<script setup lang="ts">
defineProps<NavBarProps>();
</script>
