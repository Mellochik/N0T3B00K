<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import AddIcon from '@/components/icons/AddIcon.vue';
import BackIcon from '@/components/icons/BackIcon.vue';
import TaskDescription from '@/components/tasks/TaskDescription.vue';
import TaskLabels from '@/components/tasks/TaskLabels.vue';

const router = useRouter();

const task = ref({
    title: '',
    create_date: new Date().toISOString().slice(0, 16),
    date_end: '',
    description: '',
    priority_id: 0,
    labels_id: []
});
const labels = ref([]);
const priorities = ref([]);

function createTask() {
    const taskData = {
        title: task.value.title,
        create_date: task.value.create_date,
        date_end: task.value.date_end == "" ? null : task.value.date_end,
        description: task.value.description,
        priority_id: task.value.priority_id,
        labels_id: task.value.labels_id
    };

    if (taskData.title == "" || taskData.create_date == "" || taskData.description == "" || taskData.priority_id == "" || taskData.priority_id.lenght > 0) {
        alert("Заполните все поля");
    }
    else {
        fetch('http://127.0.0.1:8000/tasks/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .then(() => {
                router.replace({ name: 'tasks' });
            })
            .catch(error => console.error(error));
    }
}

function updateDescription(newDescription) {
    task.value.description = newDescription;
}

function updateLabels(newLabels) {
    task.value.labels_id = newLabels;
}

onMounted(async () => {
    const responseLabels = await fetch('http://127.0.0.1:8000/tasks/labels')
    const dataLabels = await responseLabels.json()
    labels.value = dataLabels

    const responsePriorities = await fetch('http://127.0.0.1:8000/tasks/priorities')
    const dataPriorities = await responsePriorities.json()
    priorities.value = dataPriorities
})
</script>

<template>
    <div class="task">
        <div class="title">
            <input placeholder="Заголовок" v-model="task.title">
            <div class="buttons">
                <AddIcon class="button" :color="'#cacaca'" :size="28" @click="createTask()" />
                <BackIcon class="button" :color="'#cacaca'" :size="28" @click="router.back()" />
            </div>
        </div>
        <div class="info">
            <div class="dates">
                <h2>Даты</h2>
                <div class="date">
                    Создана: <input type="datetime-local" v-model="task.create_date" />
                </div>
                <div class="date">
                    Окончание: <input type="datetime-local" v-model="task.date_end" />
                </div>
            </div>
            <div class="detail">
                <h2>Детали</h2>
                <div class="priority-container">
                    Приоритет:
                    <select v-model="task.priority_id">
                        <option v-for="priority in priorities" :key="priority.id" :value="priority.id">
                            {{ priority.name }}
                        </option>
                    </select>
                </div>
                <div class="labels-container">
                    Метки:
                    <TaskLabels @update:selectedLabels="updateLabels" />
                </div>
            </div>
        </div>
        <div class="description">
            <h2>Описание</h2>
            <TaskDescription :text="task.description" @update:description="updateDescription" />
        </div>
    </div>
</template>

<style scoped>
main {
    padding: 100px 30%;
}

h2 {
    padding: 0px 0px;
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
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.title>input {
    font-size: 28px;
    background-color: transparent;
    font-weight: bold;
    padding: 8px 10px;
    color: #cacaca;
}

.buttons {
    display: flex;
    gap: 10px;
    margin-right: 10px;
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

.info {
    display: flex;
    flex-direction: row;
    gap: 10px;
}

.date,
.priority-container,
.labels-container {
    display: flex;
    align-items: center;
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

input {
    font-size: 20px;
    border-color: transparent;
    border-radius: 10px;
    color: #a5a5a5;
    background-color: #2c2c2c;
    padding: 2px 10px;
}

input:focus {
    outline: none;
    border-color: transparent;
    box-shadow: none;
}

select {
    font-size: 20px;
    border-color: transparent;
    border-radius: 10px;
    color: #a5a5a5;
    background-color: #2c2c2c;
    max-width: fit-content;
    padding: 2px 10px;
}

select:focus {
    outline: none;
    border-color: transparent;
    box-shadow: none;
}

@media (max-width: 1200px) {
    .info {
        flex-direction: column;
    }
}
</style>