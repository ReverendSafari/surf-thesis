<template>
    <div>
      <!-- Button for Navbar -->
      <button
        class="bg-white text-blue-500 text-sm font-semibold px-4 py-2 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        @click="toggleFaq"
      >
        FAQ
      </button>
  
      <!-- FAQ Modal -->
      <div
        v-if="isFaqOpen"
        class="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center z-50"
      >
        <div class="bg-blue-500 rounded-lg shadow-lg w-11/12 max-w-md p-6">
          <h3 class="text-xl font-semibold mb-4">Frequently Asked Questions</h3>
          <div>
            <p class="font-bold mb-2">Q: What is this app?</p>
            <p class="mb-4">A: SwellSeeker provides surfers with realtime swell and weather data to know the waves before you even leave the house.</p>
            <p class="font-bold mb-2">Q: How often is the data updated?</p>
            <p class="mb-4">A: The data is updated every 24 hours and comes in three hour increments</p>
            <p class="font-bold mb-2">Q: How can I contact support?</p>
            <p>A: Please reach out to s.swanson24@ncf.edu with any questions, suggestions, or concerns.</p>
          </div>
          <div class="mt-6 text-right">
            <button
              class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
              @click="toggleFaq"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isFaqOpen: false, // Tracks if the FAQ modal is open
      };
    },
    methods: {
      toggleFaq() {
        this.isFaqOpen = !this.isFaqOpen;
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add additional styles if needed */
  </style>
  