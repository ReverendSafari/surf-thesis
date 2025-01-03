<template>
    <div class="p-6" style="height:500px">
      <canvas ref="windChart" style="height: 100px; width: 700px;"></canvas>
      <div v-if="hoveredWind" class="hover-details">
        <p><strong>Wind Strength:</strong> {{ hoveredWind.speed }} kn</p>
        <p><strong>Wind Direction:</strong> {{ hoveredWind.direction }}° ({{ hoveredWind.cardinal }})</p>
      </div>
    </div>
  </template>
  
  <script>
  import { Chart, BarController, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js';
  import axios from 'axios';
  
  export default {
    props: {
      beach: String,
    },
    data() {
      return {
        windData: [],
        hoveredWind: null,
      };
    },
    mounted() {
      this.fetchWindData();
    },
    methods: {
      async fetchWindData() {
        try {
          const response = await axios.get(`https://3k7dz8sjwk.execute-api.us-east-2.amazonaws.com/TestStage/wind/${this.beach}`);
          const windData = JSON.parse(response.data.wind).hourly;
          this.windData = windData;
          this.buildChart();
        } catch (error) {
          console.error('Error fetching wind data:', error);
          this.windData = { wind_speed_10m: [], wind_direction_10m: [] };
        }
      },
      buildChart() {
        const ctx = this.$refs.windChart.getContext('2d');
        Chart.register(BarController, CategoryScale, LinearScale, BarElement, Tooltip, Legend);
  
        const windSpeeds = this.windData.wind_speed_10m;
        const windDirections = this.windData.wind_direction_10m;
        const labels = this.windData.time.map(time => {
          const date = new Date(time);
          return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        });
  
        const directionArrows = windDirections.map(dir => this.getArrowDirection(dir));
  
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: labels,
            datasets: [{
              label: 'Wind Speed (kn)',
              data: windSpeeds,
              backgroundColor: 'lightblue',
            }],
          },
          options: {
            responsive: true,
            plugins: {
              tooltip: {
                callbacks: {
                  label: (tooltipItem) => {
                    const index = tooltipItem.dataIndex;
                    const windSpeed = windSpeeds[index];
                    const windDirection = windDirections[index];
                    const cardinalDirection = this.getCardinalDirection(windDirection);
                    
                    this.hoveredWind = {
                      speed: windSpeed,
                      direction: windDirection,
                      cardinal: cardinalDirection,
                    };
                    return `Speed: ${windSpeed} kn, Direction: ${windDirection}° (${cardinalDirection})`;
                  }
                }
              }
            },
            scales: {
              x: {
                ticks: {
                  callback: (value, index) => labels[index],
                }
              }
            }
          },
          plugins: [{
            id: 'directionArrows',
            afterDraw: (chart) => {
              const ctx = chart.ctx;
              const xAxis = chart.scales['x'];
              directionArrows.forEach((arrow, i) => {
                ctx.fillText(arrow, xAxis.getPixelForTick(i), chart.chartArea.bottom + 10);
                ctx.fillText(windSpeeds[i] + ' kn', xAxis.getPixelForTick(i), chart.chartArea.bottom + 25);
              });
            }
          }]
        });
      },
      getArrowDirection(degree) {
        // Logic to convert degrees to arrow symbol
        if (degree >= 0 && degree < 45) return '↑';
        if (degree >= 45 && degree < 135) return '→';
        if (degree >= 135 && degree < 225) return '↓';
        if (degree >= 225 && degree < 315) return '←';
        return '↑';
      },
      getCardinalDirection(degree) {
        // Return cardinal direction based on degrees
        if (degree >= 0 && degree < 45) return 'N';
        if (degree >= 45 && degree < 90) return 'NE';
        if (degree >= 90 && degree < 135) return 'E';
        if (degree >= 135 && degree < 180) return 'SE';
        if (degree >= 180 && degree < 225) return 'S';
        if (degree >= 225 && degree < 270) return 'SW';
        if (degree >= 270 && degree < 315) return 'W';
        return 'NW';
      },
    },
  };
  </script>
  
  <style scoped>
  .hover-details {
    margin-top: 20px;
    padding: 10px;
    border: 1px solid #ddd;
    background-color: #f9f9f9;
  }
  </style>
  