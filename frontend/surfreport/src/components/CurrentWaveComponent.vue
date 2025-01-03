<template>
  <div class="w-full max-w-3xl mx-auto">
    <!-- Title centered at the top -->
    <h3 class="text-center text-sm font-semibold mb-6">Current Wave</h3>

    <!-- Single Column Layout -->
    <div class="flex flex-col space-y-6">
      <!-- Swell Summary -->
      <div>
        <p class=" text-sm text-gray-600">Swell Summary</p>
        <p :class="[waveTextColorClass, 'font-bold whitespace-nowrap']">
          {{ waveHeightRange }} ({{ closestWave ? closestWave.height : 'N/A' }} ft)
        </p>
        <GradeDisplay v-if="waveGrade" :grade="waveGrade" />
      </div>

      <!-- Wave Period -->
      <div>
        <p class="text-sm text-gray-600">Wave Period</p>
        <p class="text-sm font-bold whitespace-nowrap">
          {{ closestWave ? closestWave.period : 'N/A' }} seconds
        </p>
      </div>

      <!-- Wave Direction -->
      <div>
        <p class="text-sm text-gray-600">Wave Direction</p>
        <div class="flex items-center space-x-2">
          <!-- Box containing the rotated arrow -->
          <div class="w-6 h-6 flex items-center justify-center bg-gray-100 rounded-md">
            <span
              v-if="closestWave"
              :style="{ transform: 'rotate(' + closestWave.direction + 'deg)' }"
              class=" font-bold"
            >
              ↑
            </span>
            <span v-else>N/A</span>
          </div>

          <!-- Display the direction in cardinal format and degrees -->
          <span v-if="closestWave" class="text-sm font-bold whitespace-nowrap">
            ({{ waveDirectionCardinal }} - {{ closestWave.direction }}°)
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { getWaveQuality } from "../utils/waveGrading.js";
import GradeDisplay from "./GradeDisplay.vue";

export default {
  props: {
    beach: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      waveData: [],
      closestWave: null,
      waveGrade: "", // This will store 'green', 'yellow', or 'red'
      beachAngle: 0,
    };
  },
  components: {
    GradeDisplay,
  },
  computed: {
    waveHeightRange() {
      const height = this.closestWave ? this.closestWave.height : 0;
      if (height < 1) return "Flat";
      if (height < 2) return "1-2 ft";
      if (height < 3) return "2-3 ft";
      if (height < 4) return "3-4 ft";
      if (height < 6) return "4-6 ft";
      return "6+ ft";
    },
    waveDirectionCardinal() {
      if (!this.closestWave) return "";
      return this.convertDegreesToCardinal(this.closestWave.direction);
    },
    waveTextColorClass() {
      return this.waveGrade === "green"
        ? "text-green-700"
        : this.waveGrade === "yellow"
        ? "text-yellow-700"
        : "text-red-700";
    },
  },
  methods: {
    async fetchWaves() {
      if (this.beach && this.beach.beach_name) {
        try {
          const response = await axios.get(
            `https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/waves/${this.beach.beach_name}`
          );
          const waveData = JSON.parse(response.data.waves);
          const closestTimeIndex = this.findClosestTimeIndex(
            waveData.hourly.time
          );

          this.closestWave = {
            time: waveData.hourly.time[closestTimeIndex],
            height: waveData.hourly.wave_height[closestTimeIndex],
            direction: waveData.hourly.wave_direction[closestTimeIndex],
            period: waveData.hourly.wave_period[closestTimeIndex],
          };

          const beachResponse = await axios.get(
            "https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/beaches"
          );
          const beachData = beachResponse.data.beaches.find(
            (b) => b.beach_name === this.beach.beach_name
          );

          if (beachData) {
            this.beachAngle = beachData.beach_angle;
          }

          this.waveGrade = getWaveQuality(
            this.closestWave.direction,
            10, // Example wind speed, replace with actual data if available
            this.closestWave.period,
            this.beachAngle,
            this.closestWave.height
          );
        } catch (error) {
          console.error("Error fetching wave or beach data:", error);
        }
      }
    },
    findClosestTimeIndex(times) {
      const currentTime = new Date();
      const timeDifferences = times.map((time) => {
        const waveTime = new Date(time);
        return Math.abs(waveTime - currentTime);
      });
      return timeDifferences.indexOf(Math.min(...timeDifferences));
    },
    convertDegreesToCardinal(degrees) {
      const directions = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
        "N",
      ];
      const index = Math.round((degrees % 360) / 22.5);
      return directions[index];
    },
  },
  watch: {
    beach: {
      immediate: true,
      handler() {
        this.fetchWaves();
      },
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700&display=swap");

* {
  font-family: "Plus Jakarta Sans", sans-serif;
}
</style>
