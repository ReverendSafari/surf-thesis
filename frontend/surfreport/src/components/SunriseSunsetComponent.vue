<template>
    <div class="flex flex-col items-start">
      <h3 class="text-sm font-semibold mb-6">Sunrise & Sunset</h3>
  
      <!-- Sunrise with Sun Icon -->
      <div class="flex items-center text-gray-700 mb-4">
        <img src="@/assets/sun.svg" alt="Sunrise icon" class="w-5 h-5 mr-2" />
        <p class="text-2xl font-bold whitespace-nowrap">{{ sunriseTime }}</p>
      </div>
  
      <!-- Sunset with Moon Icon -->
      <div class="flex items-center text-gray-700">
        <img src="@/assets/moon.svg" alt="Sunset icon" class="w-5 h-5 mr-2" />
        <p class="text-2xl font-bold whitespace-nowrap">{{ sunsetTime }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: {
      lat: {
        type: Number,
        required: true,
      },
      long: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        sunriseTime: '',
        sunsetTime: '',
      };
    },
    mounted() {
      this.fetchSunriseSunset();
    },
    methods: {
      async fetchSunriseSunset() {
        try {
          const response = await axios.get(
            `https://api.sunrise-sunset.org/json?lat=${this.lat}&lng=${this.long}&formatted=0`
          );
          const { sunrise, sunset } = response.data.results;
          this.sunriseTime = this.formatTime(sunrise);
          this.sunsetTime = this.formatTime(sunset);
        } catch (error) {
          console.error('Error fetching sunrise and sunset times:', error);
        }
      },
      formatTime(utcTime) {
        const date = new Date(utcTime);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add custom styling here, if necessary */
  </style>
  