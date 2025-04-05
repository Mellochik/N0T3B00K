<script setup>
defineProps({
    size: {
        type: String,
        default: '20px'
    }
})
</script>

<template>
    <svg xmlns="http://www.w3.org/2000/svg" :height="size" viewBox="0 -960 960 960" :width="size" fill="var(--error-color)"><path d="m291-192-51-51 240-240 240 240-51 51-189-189-189 189Zm0-285-51-51 240-240 240 240-51 51-189-189-189 189Z"/></svg>
</template>