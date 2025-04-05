<script setup>
import { ref, computed } from 'vue';

import CloseIcon from '../icons/CloseIcon.vue';
import ArrowDropDownIcon from '../icons/ArrowDropDownIcon.vue';

const props = defineProps({
    modelValue: [String, Number],
    placeholder: {
        type: String,
        default: '',
    },
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
    <div class="select" v-bind="$attrs">
        <div class="selected" @click="toggleDropdown">
            <input
                v-if="isOpen"
                type="text"
                v-model="searchQuery"
                placeholder="Поиск..."
                @click.stop
            />
            <div v-else class="search">
                {{ selectedLabel || placeholder }}
            </div>
            <div class="buttons">
                <CloseIcon v-if="selectedLabel" class="clear" @click.stop="clearSelection" width="16px" :color="`var(--secondary-color)`"/>
                <ArrowDropDownIcon class="arrow" :class="{ open: isOpen }" width="20px" :color="`var(--secondary-color)`" />
            </div>
        </div>
        <ul v-if="isOpen" class="dropdown">
            <li v-if="filteredOptions.length === 0" class="no-options">
                Ничего, не найдено...
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
.select {
    position: relative;
    max-width: 300px;
    border: 1px solid var(--tertiary-color);
    border-radius: 10px;
    cursor: pointer;
}

.selected {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px;
    font-size: var(--font-size-md);
    color: var(--secondary-color);
    border-radius: 10px;
    background-color: var(--quinary-color);
}

.buttons {
    display: flex;
    align-items: center;
}

.selected input {
    width: 100%;
    border: none;
    outline: none;
    font-size: var(--font-size-md);
    background-color: transparent;
}

.arrow {
    transition: transform 0.3s ease;
}

.arrow.open {
    transform: rotate(180deg);
}

.clear {
    cursor: pointer;
}

.dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    border: 1px solid var(--tertiary-color);
    border-radius: 10px;
    background-color: var(--quinary-color);
    list-style: none;
    margin: 2px 0;
    padding: 0;
    z-index: 10;
}

.dropdown li {
    padding: 10px;
    font-size: var(--font-size-md);
    color: var(--secondary-color);
    cursor: pointer;
    border-radius: 10px;
}

.dropdown li.hover {
    background-color: var(--quaternary-color);
}

.no-options {
    padding: 10px;
    font-size: var(--font-size-sm);
    color: var(--secondary-color);
}
</style>