<script setup>
import { ref } from 'vue';

defineProps({
    type: {
        type: String,
        default: 'button'
    }
});

const isHovered = ref(false);
</script>

<template>
    <button 
    :type="type" 
    v-bind="$attrs"
    :style="{
        backgroundColor: isHovered ? hoverBackgroundColor : backgroundColor
    }"
    @mouseover="isHovered = true"
    @mouseleave="isHovered = false"
    >
        <slot></slot>
    </button>
</template>

<style scoped>
button {
    font-size: var(--font-size-lg);
    color: var(--text-color);
    background-color: transparent;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: flex;
    align-items: center;
    text-align: center;
}

button:hover {
    background-color: var(--accent-background-color);
}
</style>
