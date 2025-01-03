<template>
  <div class="p-6 border rounded-lg w-full max-w-md mt-4 ">
    <h3 class="text-xl mb-4 heading-text">Beach Location</h3>

    <!-- Google Map -->
    <GMapMap
      :center="{ lat: beachLat, lng: beachLong }"
      :zoom="12"
      style="width: 100%; height: 400px"
    >
      <GMapMarker :position="{ lat: beachLat, lng: beachLong }" />
    </GMapMap>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    beach: String,  // Beach name passed from the parent component
  },
  data() {
    return {
      beachLat: null,  // Latitude of the beach
      beachLong: null, // Longitude of the beach
    };
  },
  methods: {
    // Fetch beach data to get latitude and longitude
    async fetchBeachData() {
      try {
        const response = await axios.get('https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/beaches');
        const beachData = response.data.beaches.find(b => b.beach_name === this.beach);
        if (beachData) {
          this.beachLat = beachData.lat;
          this.beachLong = beachData.long;
        }
      } catch (error) {
        console.error('Error fetching beach data:', error);
      }
    },
  },
  watch: {
    // Refetch the beach data whenever the beach changes
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
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400&display=swap');

.heading-text {
  text-align: left;
  font-family: 'Rubik', sans-serif;
  color: black;
}
</style>
