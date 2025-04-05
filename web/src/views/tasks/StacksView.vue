<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { getRequest } from '@/api/requests.js';

import SearchIcon from '@/components/icons/SearchIcon.vue';
import BaseButton from '@/components/base/BaseButton.vue';
import BaseInput from '@/components/base/BaseInput.vue';
import CalendarIcon from '@/components/icons/CalendarIcon.vue';
import LowPriorityIcon from '@/components/icons/LowPriorityIcon.vue';
import MediumPriorityIcon from '@/components/icons/MediumPriorityIcon.vue';
import HighPriorityIcon from '@/components/icons/HighPriorityIcon.vue';
import LabelIcon from '@/components/icons/LabelIcon.vue';

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
        <div class="control-panel">
            <div class="contols-left">
                <base-input class="search" type="text" placeholder="Поиск">
                    <search-icon size="20px" />
                </base-input>
            </div>
            <div class="controls-right">
                <base-button>+ Новая стопка</base-button>
            </div>
        </div>
        <div class="stacks">
            <div v-for="stack in stacks" :key="stack.id" class="stack">
                <div class="title">
                    {{ stack.name }}
                </div>
                <div v-if="stack.tasks.length !== 0" class="tasks">
                    <div v-for="task in stack.tasks" :key="task.id" class="task-card" @click="openTaskDetail(task.id)">
                        <div class="title">
                            {{ task.title }}
                        </div>
                        <div class="date-end">
                            <calendar-icon size="20px" />
                            {{ parseDate(task.date_end) }}
                        </div>
                        <div class="priority">
                            <low-priority-icon v-if="task.priority.name === 'Не важно'" size="20px" />
                            <medium-priority-icon v-if="task.priority.name === 'Важно'" size="20px" />
                            <high-priority-icon v-if="task.priority.name === 'Срочно'" size="20px" />
                            {{ task.priority.name }}
                        </div>
                        <div class="labels-container">
                            <div class="label" v-for="label in task.labels" :key="label">
                                <label-icon size="20px" />
                                {{ label.name }}
                            </div>
                        </div>
                    </div>
                </div>
                <base-button>
                    Добавить задачу
                </base-button>
            </div>
        </div>
    </div>
    <div id="task-view">

    </div>
</template>

<style scoped>
#stacks-view {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.control-panel {
    padding: 0 10px;
    height: 50px;
    background-color: var(--background-color);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stacks {
    display: flex;
    flex-direction: row;
    overflow: auto;
    padding: 10px;
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


.search {
    flex: 1;
    padding: 5px 10px;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    background-color: var(--accent-background-color);
    color: var(--text-color);
    margin-right: 10px;
}

.new-task {
    padding: 5px 10px;
    border: none;
    border-radius: var(--border-radius-md);
    background-color: var(--primary-color);
    color: var(--text-color);
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.new-task:hover {
    background-color: var(--secondary-color);
}

.tasks {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.task-card {
    padding: 20px;
    height: fit-content;
    background-color: var(--accent-background-color);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.title {
    cursor: pointer;
}

.author, .date-end, .priority, .label {
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