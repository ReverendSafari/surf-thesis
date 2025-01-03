import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue'; // Your new homepage component
import DashboardPage from '../components/DashboardPage.vue'; // Your existing dashboard component

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
