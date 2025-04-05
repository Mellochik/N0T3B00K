<script setup>
import { ref } from 'vue';

defineProps({
    type: {
        type: String,
        default: 'button'
    },
    backgroundColor: {
        type: String,
        default: ''
    },
    hoverBackgroundColor: {
        type: String,
        default: 'var(--accent-background-color)'
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
    padding: 5px 10px;
    font-size: var(--font-size-lg);
    color: var(--text-color);
    background-color: transparent;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    cursor: pointer;
    transition: background-color 0.3s ease;
    align-items: center;
}
</style>
