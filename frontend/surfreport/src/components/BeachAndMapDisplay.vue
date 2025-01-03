<template>
  <div class="p-4 border rounded-lg w-full max-w-md bg-white shadow-md flex flex-col h-full">
    <!-- Beach Information -->
    <h1 class="text-3xl font-bold mb-1">{{ beachName }}</h1>
    <p class="text-gray-600 mb-4">Surf Report for {{ town }}, {{ state }}</p>


    <!-- Beach Image -->
    <div class="relative mb-4 flex-grow-0">
      <img
        :src="beachImageUrl"
        :alt="beachName"
        class="w-full object-cover rounded-lg shadow-md"
        style="aspect-ratio: 4 / 3;"
      />
    </div>

    <!-- Map Section -->
    <div class="flex-grow h-[300px] lg:h-full">
      <GMapMap
        :center="{ lat: beachLat, lng: beachLong }"
        :zoom="12"
        class="w-full h-full lg:rounded-lg rounded-none"
      >
        <GMapMarker :position="{ lat: beachLat, lng: beachLong }" />
      </GMapMap>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { GMapMap, GMapMarker } from "@fawmi/vue-google-maps";

export default {
  components: {
    GMapMap,
    GMapMarker,
  },
  props: {
    beach: String, // Beach name passed from the parent component
  },
  data() {
    return {
      beachName: "",
      town: "",
      state: "",
      beachImageUrl: "",
      beachLat: null,
      beachLong: null,
    };
  },
  methods: {
    async fetchBeachData() {
      try {
        const response = await axios.get(
          "https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/beaches"
        );
        const beachData = response.data.beaches.find(
          (b) => b.beach_name === this.beach
        );
        if (beachData) {
          this.beachName = beachData.beach_name;
          this.town = beachData.town;
          this.state = beachData.state;
          this.beachImageUrl = require(`@/assets/${this.town}.jpg`);
          this.beachLat = beachData.lat;
          this.beachLong = beachData.long;
        }
      } catch (error) {
        console.error("Error fetching beach data:", error);
      }
    },
  },
  watch: {
    beach: {
      immediate: true,
      handler() {
        this.fetchBeachData();
      },
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Rubik:wght@400&display=swap");

.heading-text {
  text-align: left;
  font-family: "Rubik", sans-serif;
  color: black;
}

.font-jakarta {
  font-family: "Plus Jakarta Sans", sans-serif;
}

img {
  object-position: center;
}
</style>
