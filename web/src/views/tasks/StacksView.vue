<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { getRequest } from '@/api/requests.js';

import SearchIcon from '@/components/icons/SearchIcon.vue';
import BaseButton from '@/components/base/BaseButton.vue';
import BaseInput from '@/components/base/BaseInput.vue';
import CalendarIcon from '@/components/icons/CalendarIcon.vue';
import WaitIcon from '@/components/icons/WaitIcon.vue';
import WorkIcon from '@/components/icons/WorkIcon.vue';
import DoneIcon from '@/components/icons/DoneIcon.vue';
import CloseIcon from '@/components/icons/CloseIcon.vue';
import LabelIcon from '@/components/icons/LabelIcon.vue';
import AddIcon from '@/components/icons/AddIcon.vue';

const props = defineProps({
    id: {
        type: [String, Number],
        required: true
    }
});

const router = useRouter();

const stacks = ref([]);

async function loadStacks(space_id) {
    try {
        const response = await getRequest(`/stacks?space_id=${space_id}`);
        stacks.value = response;
    } catch (error) {
        console.error('Ошибка при загрузке стопок:', error);
    }
}

function openTaskDetail(id) {
    router.push({ name: 'task-view', params: { id: id } })
}

function parseDate(date) {
    if (date != null) {
        const formattedDateEnd = new Date(date).toLocaleString('ru-RU', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        });
        return formattedDateEnd;
    }
    else {
        return 'Нет';
    }
}

onMounted(() => {
    loadStacks(props.id);
});

watch(
    () => props.id,
    (newId, oldId) => {
        if (newId !== oldId) {
            loadStacks(newId);
        }
    }
);
</script>

<template>
    <div id="stacks-view">
        <div class="stacks-control-panel">
            <div class="stacks-contols-left">
                <base-input class="stacks-search" type="text" placeholder="Поиск">
                    <search-icon size="20px" />
                </base-input>
            </div>
            <div class="stacks-controls-right">
                <base-button style="padding: 5px 10px;">
                    <add-icon size="20px" />
                    Новая стопка
                </base-button>
            </div>
        </div>
        <div class="stacks">
            <div v-for="stack in stacks" :key="stack.id" class="stack">
                <div class="stack-title">
                    {{ stack.name }}
                    <base-button style="padding: 5px;">
                        <add-icon size="20px"/>
                    </base-button>
                </div>
                <div v-if="stack.tasks.length !== 0" class="tasks">
                    <div v-for="task in stack.tasks" 
                         :key="task.id" 
                         class="task-card"
                         :class="{
                            low: task.priority.name == 'Не важно',
                            medium: task.priority.name == 'Важно',
                            high: task.priority.name == 'Срочно'
                         }"
                         @click="openTaskDetail(task.id)">
                        <div class="task-card-title">
                            {{ task.title }}
                        </div>
                        <div class="date-end">
                            <calendar-icon size="20px" />
                            {{ parseDate(task.date_end) }}
                        </div>
                        <div class="status">
                            <wait-icon v-if="task.status.name === 'В ожидании'" size="20px" />
                            <work-icon v-if="task.status.name === 'В работе'" size="20px" />
                            <done-icon v-if="task.status.name === 'Готово'" size="20px" />
                            <close-icon v-if="task.status.name === 'Закрыто'" size="20px" />
                            {{ task.status.name }}
                        </div>
                        <div class="labels-container">
                            <div class="label" v-for="label in task.labels" :key="label">
                                <label-icon size="20px" />
                                {{ label.name }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!--
        <div id="task-view">
    
        </div>
    -->
</template>

<style scoped>
#stacks-view {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.stacks-control-panel {
    padding: 0 10px;
    height: 50px;
    min-height: 50px;
    background-color: var(--background-color);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stacks-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stacks-search {
    flex: 1;
    padding: 5px 10px;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    background-color: var(--accent-background-color);
    color: var(--text-color);
    margin-right: 10px;
}

.stacks {
    display: flex;
    flex-direction: row;
    overflow: auto;
}

.stack {
    padding: 10px;
    height: fit-content;
    width: 300px;
    min-width: 300px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.stack-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.tasks {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.task-card {
    padding: 10px;
    height: fit-content;
    background-color: var(--accent-background-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.low {
    border: 1px solid var(--info-color);
}

.medium {
    border: 1px solid var(--warning-color);
}

.high {
    border: 1px solid var(--error-color);
}

.author, .date-end, .status, .label {
    display: flex;
    gap: 5px;
    align-items: center;
    text-align: center;
}

.labels-container {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}

.label {
    margin-right: 10px;
    padding: 5px 10px;
    background-color: var(--border-color);
    border-radius: var(--border-radius-md);
}

.button {
    padding: 10px;
    border-radius: var(--border-radius-md);
    border: 1px solid var(--border-color);
    cursor: pointer;
    text-align: center;
    transition: background-color 0.3s ease;
}

.button:hover {
    background-color: var(--accent-background-color);
}

#task-view {
    width: 250px;
    border-left: 1px solid var(--border-color);
}
</style>