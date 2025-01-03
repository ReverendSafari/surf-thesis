<template>
  <div class="p-4 border rounded-lg w-full max-w-md text-left bg-white font-jakarta">
    <h1 class="text-3xl font-bold mb-1">{{ beachName }} Surf Report</h1>
    <p class="text-gray-600 mb-4">Surf Report for {{ town }}, {{ state }}</p>

    <!-- Beach Image (square) -->
    <div class="relative mb-4">
      <img :src="beachImageUrl" :alt="beachName" class="w-full h-auto aspect-square object-cover rounded-lg shadow-md" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    beach: String, // Beach name passed from the parent component
  },
  data() {
    return {
      beachName: '', // Stores the beach name
      town: '', // Stores the beach town
      state: '', // Stores the beach state
      beachImageUrl: '', // Stores the image URL for the beach
    };
  },
  methods: {
    // Fetch beach data from the API
    async fetchBeachData() {
      try {
        const response = await axios.get('https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/beaches');
        const beachData = response.data.beaches.find(b => b.beach_name === this.beach);
        if (beachData) {
          this.beachName = beachData.beach_name;
          this.town = beachData.town;
          this.state = beachData.state;
          this.beachImageUrl = require(`@/assets/${this.town}.jpg`);
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
/* Import Plus Jakarta Sans font */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700&display=swap');

/* Apply the font to the component */
.font-jakarta {
  font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Ensure image is centered and uses the full container */
img {
  object-position: center;
}
</style>
