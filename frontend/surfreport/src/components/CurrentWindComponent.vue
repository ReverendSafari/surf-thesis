<template>
  <div class="flex flex-col items-start">
    <h3 class="text-center text-sm font-semibold mb-6 whitespace-nowrap">Current Wind</h3>
    
    <!-- Check if wind data is available -->
    <div v-if="closestWind">
      <p class="text-gray-600 whitespace-nowrap">Wind Speed</p>
      <p class="text-2xl font-bold mb-4 whitespace-nowrap">{{ closestWind.speed }} kn</p>
      <p class="text-gray-600 whitespace-nowrap">Wind Direction</p>
      <p class="text-2xl font-bold whitespace-nowrap">{{ windDirectionLabel }} ({{ closestWind.direction }}°)</p>
    </div>
  
    <div v-else>
      <p>No wind data available.</p>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios';


export default {
  props: {
    beach: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      windData: [], // Stores the fetched wind data
      closestWind: null, // Stores the closest wind data to the current time
    };
  },
  computed: {
    // Compute the cardinal direction label from degrees
    windDirectionLabel() {
      if (!this.closestWind) return '';
      const direction = this.closestWind.direction;
      return this.convertDegreesToCardinal(direction);
    },
  },
  methods: {
    // Fetch wind data from the API
    async fetchWind() {
      if (this.beach) {
        try {
          const response = await axios.get(`https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/wind/${this.beach.beach_name}`);
          const windData = JSON.parse(response.data.wind);
  
          // Find the closest wind data point
          const closestTimeIndex = this.findClosestTimeIndex(windData.hourly.time);
          this.closestWind = {
            time: windData.hourly.time[closestTimeIndex],
            speed: windData.hourly.wind_speed_10m[closestTimeIndex],
            direction: windData.hourly.wind_direction_10m[closestTimeIndex],
          };
        } catch (error) {
          console.error('Error fetching wind data:', error);
        }
      }
    },

    // Find the closest time index to the current time (EST)
    findClosestTimeIndex(times) {
      const currentTime = new Date();
      const timeDifferences = times.map(time => {
        const windTime = new Date(time);
        return Math.abs(windTime - currentTime);
      });
      return timeDifferences.indexOf(Math.min(...timeDifferences));
    },

    // Convert degrees to cardinal direction
    convertDegreesToCardinal(degrees) {
      const directions = [
        'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
        'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N'
      ];
      const index = Math.round((degrees % 360) / 22.5);
      return directions[index];
    },
  },
  watch: {
    // Refetch the wind data whenever the beach changes
    beach: {
      immediate: true,
      handler() {
        this.fetchWind();
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
