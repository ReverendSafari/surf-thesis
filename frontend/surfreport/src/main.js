import { createApp } from 'vue'
import App from './App.vue'
import './assets/tailwind.css';
import VueGoogleMaps from '@fawmi/vue-google-maps';
import VueApexCharts from 'vue3-apexcharts';
import router from './router';

const app = createApp(App);

app.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyD3zTdrhqdGfdj1s783gmTHnQNUpPzOBcQ',  // Replace with your actual API key
  },
});

app.use(VueApexCharts);

app.component('ApexChart', VueApexCharts);

app.use(router)

app.mount('#app');
