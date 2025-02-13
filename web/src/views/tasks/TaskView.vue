<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import BackIcon from '@/components/icons/BackIcon.vue';
import EditIcon from '@/components/icons/EditIcon.vue';
import TaskDescription from '@/components/tasks/TaskDescription.vue';

const router = useRouter();

const props = defineProps({
    id: {
        type: String,
        required: true
    }
});

const task = ref();

function parseDate(date) {
    if (date != null) {
        const formattedDate = new Date(date).toISOString().slice(0, -1);
        return formattedDate;
    } else {
        return null;
    }
}

onMounted(async () => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/tasks/show/${props.id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })

        var data = await response.json();
        task.value = data;
    } catch (error) {
        alert('Задача не существует!!!');
    }
})
</script>

<template>
    <div class="task" v-if="task">
        <div class="title">
            <h1>{{ task.title }}</h1>
            <div class="buttons">
                <EditIcon class="button" :size="28" :color="'#cacaca'"
                    @click="router.push({ name: 'task-update', params: { task: task, id: props.id } })" />
                <BackIcon class="button" :size="28" :color="'#cacaca'" @click="router.back()" />
            </div>
        </div>
        <div class="info">
            <div class="dates">
                <h2>Даты</h2>
                <div class="date">
                    Создана: <input type="datetime-local" :value="parseDate(task.create_date)" readonly />
                </div>
                <div class="date">
                    Окончание: <input type="datetime-local" :value="parseDate(task.date_end)" readonly />
                </div>
            </div>
            <div class="detail">
                <h2>Детали</h2>
                <div class="status-container">
                    Статус:
                    <div class="status">
                        {{ task.status.name }}
                    </div>
                </div>
                <div class="priority-container">
                    Приоритет:
                    <div class="status">
                        {{ task.priority.name }}
                    </div>
                </div>
                <div class="labels-container">
                    Метки:
                    <div v-for="label in task.labels" :key="label.id" class="label">
                        {{ label.name }}
                    </div>
                </div>
            </div>
        </div>
        <div class="description">
            <h2>Описание</h2>
            <TaskDescription :text="task.description" :readonly="true" />
        </div>
    </div>
</template>

<style scoped>
h1 {
    padding: 10px 0px;
}

h2 {
    padding: 0px;
}

.task {
    display: flex;
    flex-direction: column;
    font-size: 20px;
    color: #a5a5a5;
    gap: 10px;
}

.title {
    border-radius: 10px;
    background-color: #1f1f1f;
    padding: 0px 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.buttons {
    display: flex;
    gap: 10px;
}

.button {
    background-color: #2c2c2c;
    border-radius: 10px;
    padding: 5px;
    cursor: pointer;
}

.button:hover {
    background-color: #3c3c3c;
}

.dropdown-menu {
    position: absolute;
    background-color: #1f1f1f;
    border-radius: 10px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    z-index: 1;
}

.info {
    display: flex;
    flex-direction: row;
    gap: 10px;
}

.dates,
.detail,
.description {
    padding: 10px;
    border-radius: 10px;
    background-color: #1f1f1f;
    display: flex;
    flex: 1;
    flex-direction: column;
    gap: 10px;
}

.date {
    font-size: 20px;
    color: #a5a5a5;
    max-width: fit-content;
}

.status-container,
.priority-container,
.labels-container {
    display: flex;
    align-items: center;
    gap: 10px;
}

.status,
.priority,
.label {
    background-color: #2c2c2c;
    border-radius: 10px;
    padding: 2px 10px;
}

input {
    font-size: 20px;
    border-color: transparent;
    border-radius: 10px;
    color: #a5a5a5;
    background-color: #2c2c2c;
    max-width: fit-content;
    padding: 2px 10px;
}

input:focus {
    outline: none;
    border: none;
}

textarea {
    font-size: 20px;
    border-color: transparent;
    border-radius: 10px;
    color: #a5a5a5;
    background-color: #2c2c2c;
    height: auto;
    overflow-y: auto;
    resize: vertical;
    min-height: 50px;
    max-height: 200px;
}

textarea:focus {
    outline: none;
    border: none;
}

.form-grid textarea {
    height: 200px;
    resize: none;
}

@media (max-width: 1200px) {
    .info {
        flex-direction: column;
    }
}
</style>