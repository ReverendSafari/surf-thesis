<template>
  <div class="flex flex-col h-screen pb-5">
    <!-- Navbar Component -->
    <Navbar @beachSelected="setSelectedBeach" />

    <div
      class="flex flex-col lg:flex-row lg:space-x-6 w-full relative mt-3 space-y-3 lg:space-y-0 flex-grow lg:overflow-hidden px-4 lg:px-6"
    >
      <!-- Loading Overlay -->
      <div
        v-if="isLoading"
        class="absolute inset-0 flex items-center justify-center bg-white bg-opacity-90 z-10"
      >
        <div class="loader"></div>
        <p class="ml-4 text-lg font-semibold">Loading...</p>
      </div>

      <!-- Left Column: BeachAndMapDisplay -->
      <div class="w-full lg:w-1/5 flex-shrink-0 overflow-hidden">
        <div class="h-full overflow-y-auto">
          <BeachAndMapDisplay
            v-if="selectedBeach"
            :beach="selectedBeach.beach_name"
            class="w-full"
          />
        </div>
      </div>

      <!-- Right Column: Main Content -->
      <div class="flex flex-col w-full lg:w-4/5 overflow-hidden gap-4">
        <!-- Daily Component: 3/5 Height on Desktop -->
        <div class="flex-grow lg:flex-none lg:basis-3/5 overflow-y-auto">
          <DailyComponent
            v-if="selectedBeach"
            :beach="selectedBeach"
            class="w-full h-full"
          />
        </div>

        <!-- Weekly Wave Component: 2/5 Height on Desktop -->
        <div class="flex-grow lg:flex-none lg:basis-2/5 overflow-y-auto">
          <WeeklyWaveComponent
            v-if="selectedBeach"
            :key="selectedBeach.beach_name"
            :beach="selectedBeach.beach_name"
            :beachAngle="selectedBeach.beach_angle"
            class="w-full h-full"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "./AppNavbar.vue";
import DailyComponent from "./DailyComponent.vue";
import WeeklyWaveComponent from "./WeeklyWaveComponent.vue";
import BeachAndMapDisplay from "./BeachAndMapDisplay.vue";

export default {
  name: "DashboardPage",
  components: {
    Navbar,
    DailyComponent,
    WeeklyWaveComponent,
    BeachAndMapDisplay,
  },
  data() {
    return {
      selectedBeach: null,
      isLoading: false,
    };
  },
  methods: {
    async setSelectedBeach(beach) {
      this.selectedBeach = beach;
      this.isLoading = true;
      try {
        await this.fetchAllComponentsData();
      } finally {
        this.isLoading = false;
      }
    },
    async fetchAllComponentsData() {
      // Simulated delay or fetch logic
      return new Promise((resolve) => setTimeout(resolve, 1000));
    },
  },
};
</script>

<style scoped>
/* Full height for the screen */
.h-screen {
  height: 100vh;
}
</style>
