<template>
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
</template>

<script lang="ts">
type TrackItem = {
  images: string[];
  name: string;
  artists: { name: string; url?: string }[];
  url: string;
  id: string;
};
</script>

<script setup lang="ts">
import type { Ref } from "vue";
import { ref } from "vue";
const props = defineProps<{
  imgUrl: string;
  name: string;
  trackItems: TrackItem[];
  id: string;
}>();

const tracks: Ref<TrackItem[]> = ref(props.trackItems);

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
}
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
