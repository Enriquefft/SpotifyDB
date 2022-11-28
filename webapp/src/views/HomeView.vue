<script setup lang="ts">
import PlayListVue from "../components/PlayList.vue";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();

type TrackItem = {
  images: string[];
  name: string;
  artists: { name: string; url?: string }[];
  url: string;
  id: string;
};

const playList: {
  imgUrl: string;
  name: string;
  trackItems: TrackItem[];
  id: string;
} = {
  imgUrl: "https://picsum.photos/200/300",
  name: "PlayList",
  trackItems: [
    {
      images: ["https://picsum.photos/200/300"],
      name: "Track 1",
      artists: [{ name: "Artist 1" }],
      url: "https://picsum.photos/200/300",
      id: "1",
    },
    {
      images: ["https://picsum.photos/200/300"],
      name: "Track 2",
      artists: [{ name: "Artist 2" }],
      url: "https://picsum.photos/200/300",
      id: "2",
    },
    {
      images: ["https://picsum.photos/200/300"],
      name: "Track 3",
      artists: [{ name: "Artist 3" }],
      url: "https://picsum.photos/200/300",
      id: "3",
    },
  ],
  id: "playlist_id",
};
</script>

<template>
  <span v-if="userStore.isLoggedIn"> USER IS LOGGED IN</span>
  <PlayListVue v-bind="playList"></PlayListVue>
</template>
