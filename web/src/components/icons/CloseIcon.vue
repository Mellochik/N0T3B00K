<script setup>
defineProps({
  size: {
    type: Number,
    default: 20
  },
  color: {
    type: String,
    default: 'black'
  }
})
</script>

<template>
    <svg xmlns="http://www.w3.org/2000/svg" :height="`${size}px`" viewBox="0 -960 960 960" :width="`${size}px`" :fill="color"><path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/></svg>
</template>