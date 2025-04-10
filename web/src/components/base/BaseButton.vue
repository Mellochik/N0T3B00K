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
    <button :type="type" v-bind="$attrs" :style="{
        backgroundColor: isHovered ? hoverBackgroundColor : backgroundColor
    }" @mouseover="isHovered = true" @mouseleave="isHovered = false">
        <slot></slot>
    </button>
</template>

<style scoped>
button {
    padding: 10px;
    font-size: var(--font-size-lg);
    color: var(--text-color);
    background-color: var(--primary-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    cursor: pointer;
    display: flex;
    align-items: center;
    text-align: center;
    transition: opacity 0.3s ease;
}

button:hover {
    opacity: 0.75;
}

button:focus {
    opacity: 0.5;
}
</style>
