<template>
  <nav class="bg-blue-500 text-white p-4 flex flex-wrap items-center justify-between">
    <!-- First Row: Logo and FAQ -->
    <div class="flex items-center justify-between w-full md:w-auto space-x-4">
      <!-- Logo -->
      <router-link
        to="/"
        class="text-3xl font-bold transition-transform transform hover:scale-110 hover:text-yellow-400"
      >
        SwellSeeker
      </router-link>

      <!-- FAQ Button -->
      <Faq />
    </div>

    <!-- Second Row (Mobile) or Inline (Desktop): Beach Selector -->
    <div class="w-full md:w-auto mt-4 md:mt-0 md:ml-4">
      <select
        v-if="beaches.length > 0"
        v-model="selectedBeach"
        @change="onBeachSelected"
        class="bg-white text-gray-700 pl-4 pr-4 py-2 border rounded-lg shadow-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option v-for="beach in beaches" :key="beach.beach_name" :value="beach">
          {{ beach.beach_name }} ({{ beach.town }})
        </option>
      </select>
      <div v-else class="text-gray-700 text-sm">Loading beaches...</div>
    </div>
  </nav>
</template>

<script>
import axios from "axios";
import Faq from "./FaqComponent.vue";

export default {
  components: {
    Faq,
  },
  props: ["onBeachSelect"], // Callback prop for passing selected beach back to parent
  data() {
    return {
      beaches: [],
      selectedBeach: null,
    };
  },
  methods: {
    async fetchBeaches() {
      try {
        const response = await axios.get(
          "https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/beaches"
        );
        this.beaches = response.data.beaches;

        if (this.beaches.length > 0) {
          const queryBeachName = this.$route.query.beach;

          // Match query parameter with the beach list, or default to the first beach
          const matchedBeach = this.beaches.find(
            (beach) => beach.beach_name === queryBeachName
          );
          this.selectedBeach = matchedBeach || this.beaches[0];

          // Emit the selected beach to the parent component
          this.$emit("beachSelected", this.selectedBeach);
        }
      } catch (error) {
        console.error("Error fetching beaches:", error);
      }
    },
    onBeachSelected() {
      if (this.selectedBeach) {
        // Emit the selected beach to the parent
        this.$emit("beachSelected", this.selectedBeach);

        // Update the URL without reloading the page
        this.$router.replace({ query: { beach: this.selectedBeach.beach_name } });
      }
    },
  },
  mounted() {
    this.fetchBeaches(); // Fetch the list of beaches when the component mounts
  },
};
</script>

<style scoped>
/* Basic navbar styling */
.bg-blue-500 {
  background-color: #0077b6;
}

/* Add spacing between Logo and FAQ */
.space-x-4 > :not([hidden]) ~ :not([hidden]) {
  margin-left: 1rem; /* Add space between elements */
}
</style>
