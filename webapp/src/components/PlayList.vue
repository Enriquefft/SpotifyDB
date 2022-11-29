<template>
  <div>
    <h2 class="text-center">Play List: {{ props.name }}</h2>
    <figure>
      <img :src="props.imgUrl" alt="Play List Image" />
    </figure>
    <!-- droppable box -->
    <div
      class="droppable"
      @drop="handleDrop"
      @dragenter.prevent
      @dragover.prevent
    >
      <p>Drop Here</p>
    </div>
    <ul>
      <li
        v-for="track in tracks"
        :key="track.name"
        draggable="true"
        @dragstart="handreDragStart($event, track)"
      >
        <figure>
          <picture>
            <source v-for="url in track.images" :srcset="url" :key="url" />
            <img :src="track.images[track.images.length]" alt="album cover" />
          </picture>
          <figcaption>{{ track.name }} image</figcaption>
        </figure>

        <a :href="track.url">{{ track.name }}</a>

        <!-- artists -->
        <div v-if="track.artists.length > 1">
          <ul>
            <li v-for="artist in track.artists" :key="artist.name">
              <a :href="artist.url">{{ artist.name }}</a>
            </li>
          </ul>
        </div>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
type TrackItem = {
  id: string;
  name: string;
  images: string[];
  artists: { name: string; url?: string }[];
  url: string;
};
</script>

<script setup lang="ts">
import type { Ref } from "vue";
import { ref } from "vue";
import { API_LOCATION } from "@/../config";
import { useUserStore } from "../stores/user";

const userStore = useUserStore();

const props = defineProps<{
  id: string;
  name: string;
  imgUrl: string;
}>();

const tracks: Ref<TrackItem[]> = ref([]);

function handreDragStart(event: DragEvent, track: TrackItem) {
  if (!event.dataTransfer) return; // check not null
  event.dataTransfer.dropEffect = "move";
  event.dataTransfer.effectAllowed = "move";
  event.dataTransfer?.setData("trackID", track.id);
  console.log("drag start", track.id);
}

function handleDrop(event: DragEvent) {
  const trackID = event.dataTransfer?.getData("trackID");
  const track = tracks.value.find((t) => t.id === trackID);
  if (track) {
    tracks.value = tracks.value.filter((t) => t.id !== trackID);
  }
  console.log("drop", track);
  removeSong(trackID, props.id);
}

function removeSong(trackID: string | undefined, playlistID: string) {
  if (!trackID || !playlistID) return;
  fetch(`${API_LOCATION}/playlist/${playlistID}/remove/${trackID}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${userStore.access_token}`,
    },
    body: null,
  })
    .then((res) => {
      if (res.status === 200) {
        console.log("removed");
        return res.json();
      }
      console.error("error removing song", res.statusText);
    })
    .then((data) => {
      console.log(data);
    })
    .catch((err) => {
      console.error(err);
    });
}

function fetchTracks() {
  fetch(`${API_LOCATION}/playlists/${props.id}`, {
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
      tracks.value = data.tracks;
    })
    .catch((error) => console.log(error));
}
fetchTracks();
</script>

<style>
div.droppable {
  background-color: #f1f1f1;
  width: 100%;
  height: 100px;
  border: 1px solid #d3d3d3;
  text-align: center;
  padding: 10px;
  margin: 10px 0;
}
</style>
