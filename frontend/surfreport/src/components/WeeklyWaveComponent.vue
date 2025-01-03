<template>
  <div
    class="p-4 border rounded-lg bg-white shadow-md mx-auto flex flex-col h-full"
  >
    <!-- Card Header -->
    <h3 class="text-lg font-semibold mb-2 text-center">Weekly Wave Forecast</h3>

    <!-- Chart Container -->
    <div v-if="chartOptions && chartSeries.length > 0" class="flex-grow">
      <ApexChart
        :type="chartType"
        :options="chartOptions"
        :series="chartSeries"
        :height="chartHeightNumeric"
        class="block"
      />
    </div>

    <!-- Loading Message -->
    <div v-else class="text-center mt-4">
      <p>Loading chart...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { getWaveQuality } from "../utils/waveGrading.js";
import VueApexCharts from "vue3-apexcharts";

export default {
  components: {
    ApexChart: VueApexCharts,
  },
  props: {
    beach: String,
    beachAngle: Number,
  },
  data() {
    return {
      waveData: [],
      windData: [],
      chartSeries: [],
      chartOptions: null,
      chartType: "bar", // Dynamically change type based on screen width
      chartHeight: "100%", // Set height to auto-fill
    };
  },
  computed: {
    chartHeightNumeric() {
      return this.chartType === "bar" && window.innerWidth < 768
        ? 800 // Taller chart on mobile for readability
        : "100%"; // Default to container height
    },
  },
  mounted() {
    this.fetchData();
    this.setChartType();
    window.addEventListener("resize", this.setChartType);
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.setChartType);
  },
  methods: {
    async fetchData() {
      try {
        const waveResponse = await axios.get(
          `https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/waves/${this.beach}`
        );
        const windResponse = await axios.get(
          `https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/wind/${this.beach}`
        );
        const waveData = JSON.parse(waveResponse.data.waves);
        const windData = JSON.parse(windResponse.data.wind);

        this.waveData = waveData.hourly || [];
        this.windData = windData.hourly || [];

        if (this.waveData.wave_height && this.windData.wind_speed_10m) {
          this.setupChart();
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    setupChart() {
      const waveHeights = this.waveData.wave_height || [];
      const colors = waveHeights.map((height, index) => {
        const windSpeed = this.windData.wind_speed_10m[index];
        const windDirection = this.windData.wind_direction_10m[index];
        const wavePeriod = this.waveData.wave_period[index];
        const beachAngle = this.beachAngle || 120;
        const waveGrade = getWaveQuality(
          windDirection,
          windSpeed,
          wavePeriod,
          beachAngle,
          height
        );
        return waveGrade === "green"
          ? "#2ecc71"
          : waveGrade === "yellow"
          ? "#f1c40f"
          : "#e74c3c";
      });

      const labels = this.waveData.time.map((time) => {
        const date = new Date(time);
        return date.toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
        });
      });

      // Group times under day labels
      const groups = [];
      for (let i = 0; i < labels.length; i += 8) {
        const date = new Date(this.waveData.time[i]);
        const dayLabel = date.toLocaleDateString("en-US", {
          weekday: "short",
        });
        groups.push({
          title: dayLabel,
          cols: 8, // Number of times in this group
        });
      }

      this.chartSeries = [
        {
          name: "Wave Height (ft)",
          data: waveHeights,
        },
      ];

      this.chartOptions = {
        chart: {
          type: this.chartType,
        },
        plotOptions: {
          bar: {
            borderRadius: 4,
            distributed: true,
            horizontal: this.chartType === "bar" && window.innerWidth < 768, // Horizontal bars on mobile
          },
        },
        xaxis: {
          categories: labels,
          tickPlacement: "on",
          group: {
            style: {
              fontSize: "12px",
              fontWeight: 700,
            },
            groups: groups, // Set up day groupings
          },
          labels: {
            style: {
              fontSize: "10px",
            },
          },
        },
        yaxis: {
          labels: {
            style: {
              fontSize: "12px",
            },
          },
        },
        colors: colors,
        tooltip: {
          custom: ({ dataPointIndex }) => {
            const waveHeight = this.waveData.wave_height[dataPointIndex];
            const wavePeriod = this.waveData.wave_period[dataPointIndex];
            const windSpeed = this.windData.wind_speed_10m[dataPointIndex];
            const windDirectionDegrees =
              this.windData.wind_direction_10m[dataPointIndex];
            const windDirectionCardinal =
              this.convertDegreesToCardinal(windDirectionDegrees);

            const date = new Date(this.waveData.time[dataPointIndex]);
            const dayLabel = date.toLocaleDateString("en-US", {
              weekday: "short",
              month: "short",
              day: "numeric",
            });
            const timeLabel = date.toLocaleTimeString("en-US", {
              hour: "2-digit",
              minute: "2-digit",
            });

            return `<div style="padding:8px; border-radius: 4px; background: #fff;">
              <div style="font-weight: bold; font-size: 14px; margin-bottom: 6px;">
                ${dayLabel}, ${timeLabel}
              </div>
              <strong>Height:</strong> ${waveHeight} ft<br>
              <strong>Period:</strong> ${wavePeriod} s<br>
              <strong>Wind Speed:</strong> ${windSpeed} kn<br>
              <strong>Wind Direction:</strong> ${windDirectionCardinal} (${windDirectionDegrees}°)
            </div>`;
          },
        },
        legend: {
          show: false,
        },
        dataLabels: {
          enabled: false,
        },
      };
    },
    setChartType() {
      this.chartType = window.innerWidth < 768 ? "bar" : "bar";
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
      ];
      const index = Math.round((degrees % 360) / 22.5);
      return directions[index];
    },
  },
};
</script>

<style scoped>
.flex-grow {
  flex-grow: 1;
}
</style>
