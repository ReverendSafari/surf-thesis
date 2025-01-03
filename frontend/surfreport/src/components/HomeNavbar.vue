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
    </nav>
  </template>
  
  <script>
  import Faq from "./FaqComponent.vue";
  
  export default {
    components: {
      Faq,
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
  