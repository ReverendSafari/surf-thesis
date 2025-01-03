<template>
  <div class="flex justify-center mt-4">
    <!-- Beach Dropdown -->
    <select
      v-if="beaches.length > 0"
      v-model="selectedBeach"
      @change="updateBeach"
      class="bg-white text-gray-700 pl-4 pr-4 py-2 border rounded-lg shadow-md w-full max-w-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option v-for="beach in beaches" :key="beach.beach_name" :value="beach">
        {{ beach.beach_name }} ({{ beach.town }})
      </option>
    </select>

    <!-- Fallback while loading -->
    <div v-else class="text-gray-700 text-sm text-center">Loading beaches...</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      beaches: [], // Holds the fetched beach data
      selectedBeach: null, // Now this will hold the full beach object, not just the name
    };
  },
  methods: {
    // Fetch beaches from the API
    async fetchBeaches() {
      try {
        const response = await axios.get('https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/beaches');
        this.beaches = response.data.beaches;

        if (this.beaches.length > 0) {
          const queryBeachName = this.$route.query.beach;

          // Match the query parameter with the beach list, or default to the first
          const matchedBeach = this.beaches.find(beach => beach.beach_name === queryBeachName);
          this.selectedBeach = matchedBeach || this.beaches[0];

          this.updateBeach(); // Ensure the selected beach is emitted and the URL is updated
        }
      } catch (error) {
        console.error('Error fetching beaches:', error);
      }
    },

    // Emit the entire selected beach object to the parent component
    updateBeach() {
      if (this.selectedBeach) {
        this.$emit('beachSelected', this.selectedBeach); // Emit the selected beach
        this.$router.replace({ query: { beach: this.selectedBeach.beach_name } }); // Update the URL without reloading
      }
    },
  },
  mounted() {
    // Fetch beaches when the component is mounted
    this.fetchBeaches();
  },
};
</script>

<style scoped>
/* Add optional margin for spacing */
.mt-4 {
  margin-top: 1rem;
}
</style>
