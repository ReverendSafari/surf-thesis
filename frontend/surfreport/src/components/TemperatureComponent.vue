<template>
  <div class="flex flex-col items-start">
    <h3 class="text-center text-sm font-semibold mb-6">Temperature</h3>
    <div v-if="airTemp !== null && waterTemp !== null">
      <p class="text-sm text-gray-600 whitespace-nowrap">Air temperature</p>
      <p class="text-sm font-bold mb-4">{{ airTemp }}°F</p>
      <p class="text-sm text-gray-600 whitespace-nowrap">Water temperature</p>
      <p class="text-sm font-bold mb-4">{{ waterTemp }}°F</p>
      <p class="text-sm text-gray-600 whitespace-nowrap">Wetsuit Recommendation</p>
      <p class="text-sm font-semibold text-blue-600">{{ wetsuitRecommendation }}</p>
    </div>
    <div v-else>
      <p>No temperature data available.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    beach: {
      type: Object,
      required: true
    },
  },
  data() {
    return {
      airTemp: null,
      waterTemp: null,
    };
  },
  computed: {
    wetsuitRecommendation() {
      if (this.waterTemp >= 70) {
        return 'No Wetsuit needed';
      } else if (this.waterTemp >= 65) {
        return '2mm spring suit';
      } else if (this.waterTemp >= 55) {
        return '3/2mm  wetsuit';
      } else if (this.waterTemp >= 48) {
        return '4/3mm wetsuit with booties and gloves.';
      } else if (this.waterTemp < 48) {
        return '5/4mm wetsuit with booties, gloves, and a hood.';
      } else {
        return 'No recommendation available.';
      }
    },
  },
  methods: {
    async fetchTemps() {
      if (this.beach && this.beach.beach_name) {
        try {
          const response = await axios.get(`https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/temps/${this.beach.beach_name}`);
          this.airTemp = response.data.air_temp;
          this.waterTemp = response.data.water_temp;
        } catch (error) {
          console.error('Error fetching temperature data:', error);
        }
      }
    },
  },
  watch: {
    beach: {
      immediate: true,
      handler() {
        this.fetchTemps();
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
