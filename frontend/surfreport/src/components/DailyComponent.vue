<template>
  <div class="p-6 border rounded-lg bg-white shadow-md h-full overflow-hidden">
    <!-- Title Section -->
    <div class="mb-4">
      <h2 class="text-xl text-center font-semibold text-gray-800">
        Daily Waves - {{ formattedDate }}
      </h2>
    </div>

    <!-- Grid Content -->
    <div
      class="grid gap-6 h-full"
      :class="{
        'grid-cols-5': !isMobile,
        'grid-cols-1': isMobile,
      }"
    >
      <!-- Temperature Component -->
      <div class="lg:border-r lg:pr-6">
        <TemperatureComponent :beach="beach" />
      </div>

      <hr v-if="isMobile" class="border-gray-300 w-full my-2" />

      <!-- Tide Component -->
      <div class="lg:border-r lg:pr-6">
        <TideComponent :beach="beach" />
      </div>

      <hr v-if="isMobile" class="border-gray-300 w-full my-2" />

      <!-- Wave Component -->
      <div class="lg:border-r lg:pr-6">
        <CurrentWaveComponent :beach="beach" />
      </div>

      <hr v-if="isMobile" class="border-gray-300 w-full my-2" />

      <!-- Wind Component -->
      <div class="lg:border-r lg:pr-6">
        <CurrentWindComponent :beach="beach" />
      </div>

      <hr v-if="isMobile" class="border-gray-300 w-full my-2" />

      <!-- SunriseSunset Component -->
      <div>
        <SunriseSunsetComponent :lat="beach.lat" :long="beach.long" />
      </div>
    </div>
  </div>
</template>

<script>
import TemperatureComponent from './TemperatureComponent.vue';
import TideComponent from './TideComponent.vue';
import CurrentWaveComponent from './CurrentWaveComponent.vue';
import CurrentWindComponent from './CurrentWindComponent.vue';
import SunriseSunsetComponent from './SunriseSunsetComponent.vue';

export default {
  components: {
    TemperatureComponent,
    TideComponent,
    CurrentWaveComponent,
    CurrentWindComponent,
    SunriseSunsetComponent,
  },
  props: {
    beach: {
      type: Object,
      required: true,
    },
  },
  computed: {
    formattedDate() {
      const now = new Date();
      const options = { month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
      return now.toLocaleString('en-US', options); // Adjust locale as needed
    },
    isMobile() {
      return window.innerWidth < 1024; // Tailwind's "lg" breakpoint
    },
  },
  mounted() {
    window.addEventListener('resize', this.updateIsMobile);
    this.updateIsMobile(); // Set the initial state
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateIsMobile);
  },
  methods: {
    updateIsMobile() {
      this.$forceUpdate(); // Rerender component on viewport resize
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700&display=swap');

* {
  font-family: 'Plus Jakarta Sans', sans-serif;
}

.h-full {
  height: 100%; /* Ensure component fills the available height */
}

.grid {
  align-items: start; /* Align grid items to start of rows */
}

.overflow-hidden {
  overflow: hidden; /* Prevent scrollbars */
}
</style>
