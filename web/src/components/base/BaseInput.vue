<script setup>
defineProps({
    id: String,
    type: {
        type: String,
        default: 'text'
    },
    modelValue: [String, Number]
});

defineEmits(['update:modelValue']);
</script>

<template>
    <div class="base-input">
        <slot></slot>
        <input
            :id="id"
            :type="type"
            v-bind="$attrs"
            :value="modelValue"
            @input="$emit('update:modelValue', $event.target.value)"
        />
    </div>
</template>

<style scoped>
.base-input {
    background-color: var(--accent-background-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    display: flex;
    align-items: center;
    gap: 5px;
}

input {
    padding: 10px;
    color: var(--text-color);
    font-size: var(--font-size-lg);
    background-color: transparent;
    border: transparent;
}

input:focus {
    outline: none;
    border-color: var(--border-color);
}
</style>
