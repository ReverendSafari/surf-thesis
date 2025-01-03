<template>
  <div :class="['px-3 py-1 rounded-lg text-sm font-semibold flex justify-center items-center', gradeColorClass]">
    <span>{{ gradeText }}</span>
  </div>
</template>

<script>
export default {
  props: {
    grade: String // The grade is passed down from the parent
  },
  computed: {
    // Compute the color class for the text and background based on the grade
    gradeColorClass() {
      return this.grade === 'green' ? 'text-green-700 bg-green-100' :
             this.grade === 'yellow' ? 'text-yellow-700 bg-yellow-100' :
             'text-red-700 bg-red-100';
    },
    // Compute the text label based on the grade
    gradeText() {
      return this.grade === 'green' ? 'Good' :
             this.grade === 'yellow' ? 'Fair' :
             'Poor';
    }
  }
};
</script>

<style scoped>
/* Add any specific styling adjustments here if needed */
</style>
