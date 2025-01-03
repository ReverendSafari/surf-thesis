<template>
  <div class="flex flex-col items-start">
    <h3 class="text-center text-sm font-semibold mb-6 whitespace-nowrap">Current Tide</h3>
    
    <!-- Check if we have tide data -->
    <div v-if="tides.length > 0">
      <div>
        <p class="text-gray-700 mb-2 whitespace-nowrap">High Tides</p>
        <ul class=" font-bold mb-2 whitespace-nowrap">
          <li v-for="tide in highTides" :key="tide.time">
            {{ formatTime(tide.time) }} - {{ tide.height }} ft
          </li>
        </ul>
      </div>

      <div class="mt-4">
        <p class="text-gray-700 mb-2">Low Tides</p>
        <ul class="text-lg font-bold whitespace-nowrap">
          <li v-for="tide in lowTides" :key="tide.time">
            {{ formatTime(tide.time) }} - {{ tide.height }} ft
          </li>
        </ul>
      </div>
    </div>

    <div v-else>
      <p>No tide data available.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    beach: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      tides: [],  // Stores the fetched tide data
    };
  },
  computed: {
    // Filter high tides
    highTides() {
      return this.tides.filter(tide => tide.type === 'high');
    },
    // Filter low tides
    lowTides() {
      return this.tides.filter(tide => tide.type === 'low');
    },
  },
  methods: {
    // Fetch tide data from the API
    async fetchTides() {
      if (this.beach) {
        try {
          const response = await axios.get(`https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/tides/${this.beach.beach_name}`);
          this.tides = response.data.tides;
        } catch (error) {
          console.error('Error fetching tides:', error);
        }
      }
    },
    // Format the tide time for display
    formatTime(time) {
      const date = new Date(time);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
  },
  watch: {
    // Refetch the tides whenever the beach changes
    beach: {
      immediate: true,
      handler() {
        this.fetchTides();
      },
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700&display=swap');

* {
  font-family: 'Plus Jakarta Sans', sans-serif;
}
</style>
