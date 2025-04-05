<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
    modelValue: [String, Number],
    options: {
        type: Array,
        required: true,
        default: () => [],
    },
});

const emit = defineEmits(['update:modelValue']);

const selectedLabel = ref('');
const isOpen = ref(false);
const hoveredIndex = ref(null);
const searchQuery = ref('');

const toggleDropdown = () => {
    isOpen.value = !isOpen.value;
    if (!isOpen.value) searchQuery.value = '';
};

const selectOption = (option) => {
    selectedLabel.value = option.label;
    emit('update:modelValue', option.value);
    isOpen.value = false;
    searchQuery.value = '';
};

const clearSelection = () => {
    selectedLabel.value = '';
    emit('update:modelValue', null);
};

const filteredOptions = computed(() => {
    if (!searchQuery.value) return props.options;
    return props.options.filter(option =>
        option.label.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});
</script>

<template>
    <div class="custom-select">
        <div class="selected" @click="toggleDropdown">
            <input
                v-if="isOpen"
                type="text"
                v-model="searchQuery"
                placeholder="Search..."
                @click.stop
            />
            <span v-else>
                {{ selectedLabel || 'Выберите' }}
            </span>
            <button v-if="selectedLabel" class="clear-btn" @click.stop="clearSelection">×</button>
        </div>
        <ul v-if="isOpen" class="dropdown">
            <li v-if="filteredOptions.length === 0" class="no-options">
                Sorry, no matching options.
            </li>
            <li
                v-for="(option, index) in filteredOptions"
                :key="index"
                :class="{ hover: hoveredIndex === index }"
                @mouseover="hoveredIndex = index"
                @mouseleave="hoveredIndex = null"
                @click="selectOption(option)"
            >
                {{ option.label }}
            </li>
        </ul>
    </div>
</template>

<style scoped>
.custom-select {
    position: relative;
    width: 200px;
    border: 1px solid var(--primary-color);
    border-radius: 4px;
    background-color: var(--quinary-color);
    cursor: pointer;
}

.selected {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px;
    font-size: var(--font-size-md);
    color: var(--primary-color);
}

.selected input {
    width: 100%;
    border: none;
    outline: none;
    font-size: var(--font-size-md);
    color: var(--primary-color);
    background-color: transparent;
}

.clear-btn {
    background: none;
    border: none;
    font-size: 16px;
    cursor: pointer;
    color: var(--primary-color);
}

.dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    border: 1px solid var(--primary-color);
    border-radius: 4px;
    background-color: var(--quinary-color);
    list-style: none;
    margin: 0;
    padding: 0;
    z-index: 10;
}

.dropdown li {
    padding: 10px;
    font-size: var(--font-size-md);
    color: var(--primary-color);
    cursor: pointer;
}

.dropdown li.hover {
    background-color: var(--tertiary-color);
    color: var(--quaternary-color);
}

.no-options {
    padding: 10px;
    font-size: var(--font-size-md);
    color: var(--secondary-color);
    text-align: center;
}
</style>