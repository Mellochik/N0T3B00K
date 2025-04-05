<script setup>
defineProps({
    size: {
        type: String,
        default: '20px'
    }
})
</script>

<template>
    <svg xmlns="http://www.w3.org/2000/svg" :height="size" viewBox="0 -960 960 960" :width="size" fill="var(--text-color)"><path d="M480-344 240-584l56-56 184 184 184-184 56 56-240 240Z"/></svg>
</template>