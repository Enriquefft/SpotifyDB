<template>
  <span v-if="userStore.isLoggedIn"> USER IS LOGGED IN</span>
  <!--<PlaylistList v-bind="playLists"></PlaylistList>-->
  <div class="flex">
    <PlayList
      id="69ts0XXLotPGTe9QV2410q"
      name="my shazams"
      imgUrl="stock photo"
    />
    <PlayList
      id="3nP9lqFEry1vK60CJwESQg"
      name="villain songs"
      imgUrl="stock photo"
    />
  </div>
</template>

<script setup lang="ts">
import PlayList from "@/components/PlayList.vue";
import PlaylistList from "../components/PlaylistList.vue";
import { useUserStore } from "../stores/user";
import type { Ref } from "vue";
import { ref } from "vue";
import { API_LOCATION } from "@/../config";

const userStore = useUserStore();

const playLists: Ref<{
  playlists: {
    name: string;
    url: string;
    images: string[];
    id: string;
  }[];
  size: number;
}> = ref({ playlists: [], size: 0 });

fetchPlaylists();
console.log(`${API_LOCATION}/playlists`);
function fetchPlaylists() {
  fetch(`${API_LOCATION}/playlists`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${userStore.access_token}`,
    },
  })
    .then((res) => {
      if (!res.ok) {
        throw Error(res.statusText);
      }
      return res.json();
    })
    .then((data) => {
      playLists.value = data;
    })
    .catch((error) => console.log(error));
}
</script>
