<template>
  <div class="flex flex-col items-center">
    <div class="relative w-full max-w-sm sm:max-w-md md:max-w-lg lg:max-w-xl">
      <!-- Icon inside the select box -->
      <img
        src="@/assets/search.svg"
        alt="Search icon"
        class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500 pointer-events-none"
      />

      <!-- Dropdown for Beach Selection -->
      <select
        v-model="selectedBeach"
        @change="goToDashboard"
        class="bg-white text-gray-700 pl-10 pr-4 py-2 border rounded-lg shadow-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option disabled value="">Find your beach</option>
        <option v-for="beach in beaches" :key="beach.beach_name" :value="beach">
          {{ beach.beach_name }} ({{ beach.town }})
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      beaches: [], // Holds the fetched beach data
      selectedBeach: "", // Default is empty to show "Find your beach"
    };
  },
  methods: {
    async fetchBeaches() {
      try {
        const response = await axios.get('https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/beaches');
        this.beaches = response.data.beaches; // Store the list of beaches
      } catch (error) {
        console.error('Error fetching beaches:', error);
      }
    },
    goToDashboard() {
      if (this.selectedBeach && this.selectedBeach !== "") {
        // Navigate to the dashboard with the selected beach name as a query parameter
        this.$router.push({ name: 'dashboard', query: { beach: this.selectedBeach.beach_name } });
      }
    },
  },
  mounted() {
    this.fetchBeaches(); // Fetch beaches on component mount
  },
};
</script>

<style scoped>
/* Consistent appearance for select while keeping native arrow */
select {
  -webkit-appearance: menulist; /* Keep native arrow on Safari */
  -moz-appearance: menulist; /* Keep native arrow on Firefox */
  appearance: menulist; /* Keep native arrow on modern browsers */
}

/* Fix for padding issues across browsers */
.pl-10 {
  padding-left: 2.5rem; /* Adds space for the icon */
}

.relative {
  position: relative;
}

img {
  pointer-events: none; /* Makes the icon non-interactive */
}

.left-3 {
  left: 0.75rem; /* Icon's left padding */
}

.top-1\/2 {
  top: 50%; /* Centers the icon vertically */
}

.transform {
  transform: translateY(-50%); /* Adjusts for the icon's alignment */
}
</style>
