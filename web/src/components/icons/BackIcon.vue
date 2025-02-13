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
    <svg xmlns="http://www.w3.org/2000/svg" :height="`${size}px`" viewBox="0 -960 960 960" :width="`${size}px`" :fill="color"><path d="m313-440 224 224-57 56-320-320 320-320 57 56-224 224h487v80H313Z"/></svg>
</template>