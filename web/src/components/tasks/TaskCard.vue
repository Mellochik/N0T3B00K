<script setup>
import { useRouter } from 'vue-router';
import HighPriorityIcon from '../icons/HighPriorityIcon.vue';
import MediumPriorityIcon from '../icons/MediumPriorityIcon.vue';
import LowPriorityIcon from '../icons/LowPriorityIcon.vue';

const router = useRouter()

defineProps({
    task: {
        type: Object,
        required: true
    }
})

function openTaskDetail(id) {
    router.push({ name: 'task-view', params: { id: id } })
}

function parseDate(date) {
    if (date != null) {
        const formattedDateEnd = new Date(date).toLocaleString('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        return formattedDateEnd;
    }
    else {
        return 'Нет';
    }
}
</script>

<template>
    <div class="task-card">
        <div class="title" @click="openTaskDetail(task.id)">
            {{ task.title }}
        </div>
        <div class="description">
            <div class="dateEnd-container">
                <div class="dateEnd">
                    {{ parseDate(task.date_end) }}
                </div>
            </div>
            <HighPriorityIcon v-if="task.priority.name == 'Срочно'" />
            <MediumPriorityIcon v-if="task.priority.name == 'Важно'" />
            <LowPriorityIcon v-if="task.priority.name == 'Неважно'" />
            <div class="labels-container">
                <div class="label" v-for="label in task.labels" :key="label">
                    {{ label.name }}
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.task-card {
    height: fit-content;
    background-color: #1f1f1f;
    border-radius: 20px;
}

.title {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
    padding: 10px;
    background-color: #2c2c2c;
    height: 50px;
    font-size: 20px;
    font-weight: 600;
    color: #cacaca;
    cursor: pointer;
}

.more-icon {
    cursor: pointer;
}

.description {
    padding: 10px;
    font-size: 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    color: #9f9f9f;
}

.labels-container {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}

.label {
    display: inline-block;
    border-radius: 5px;
    margin-right: 10px;
    padding: 1px 5px;
    color: #9f9f9f;
    border: 1px solid rgb(162, 162, 162);
}
</style>