<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import SaveIcon from '@/components/icons/SaveIcon.vue';
import BackIcon from '@/components/icons/BackIcon.vue';
import TaskDescription from '@/components/tasks/TaskDescription.vue';
import TaskLabels from '@/components/tasks/TaskLabels.vue';

const router = useRouter();

const props = defineProps({
    id: {
        type: String,
        required: true
    },
    task: {
        type: Object,
        require: true
    }
});

const taskNew = ref(props.task);
const labels = ref([]);
const priorities = ref([]);
const statuses = ref([]);

function updateDescription(newDescription) {
    taskNew.value.description = newDescription;
}

function updateLabels(newLabels) {
    taskNew.value.labels = newLabels;
}

function parseDate(date) {
    if (date != null) {
        const formattedDate = new Date(date).toISOString().slice(0, -1);
        return formattedDate;
    } else {
        return null;
    }
}

function updateTask() {
    const taskData = {
        id: taskNew.value.id,
        title: taskNew.value.title,
        create_date: taskNew.value.create_date,
        date_end: taskNew.value.date_end == "" ? null : taskNew.value.date_end,
        description: taskNew.value.description,
        status_id: taskNew.value.status.id,
        priority_id: taskNew.value.priority.id,
        labels_id: taskNew.value.labels
    };

    if (taskData.title == "" || taskData.create_date == "" || taskData.description == "" || taskData.priority_id == "" || taskData.priority_id.lenght > 0) {
        alert("Заполните все поля");
    }
    else {
        fetch('http://127.0.0.1:8000/tasks/update', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                router.replace({ name: 'task-view', params: { id: props.id } });
            })
            .catch(error => console.error(error));
    }
}

onMounted(async () => {
    if (taskNew.value === undefined) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/tasks/show/${props.id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })

            var data = await response.json();
            taskNew.value = data;
            taskNew.value.create_date = parseDate(taskNew.value.create_date);
            taskNew.value.date_end = parseDate(taskNew.value.date_end);
        } catch (error) {
            alert('Задача не существует!!!');
        }
    }
    const responseStatuses = await fetch('http://127.0.0.1:8000/tasks/statuses');
    const dataStatuses = await responseStatuses.json()
    statuses.value = dataStatuses

    const responseLabels = await fetch('http://127.0.0.1:8000/tasks/labels')
    const dataLabels = await responseLabels.json()
    labels.value = dataLabels

    const responsePriorities = await fetch('http://127.0.0.1:8000/tasks/priorities')
    const dataPriorities = await responsePriorities.json()
    priorities.value = dataPriorities
})
</script>

<template>
    <div class="task" v-if="taskNew">
        <div class="title">
            <input placeholder="Заголовок" v-model="taskNew.title">
            <div class="buttons">
                <SaveIcon class="button" :color="'#cacaca'" :size="28" @click="updateTask()" />
                <BackIcon class="button" :color="'#cacaca'" :size="28" @click="router.back()" />
            </div>
        </div>
        <div class="info">
            <div class="dates">
                <h2>Даты</h2>
                <div class="date-container">
                    Создана: <input type="datetime-local" v-model="taskNew.create_date" />
                </div>
                <div class="date-container">
                    Окончание: <input type="datetime-local" v-model="taskNew.date_end" />
                </div>
            </div>
            <div class="detail">
                <h2>Детали</h2>
                <div class="status-container">
                    Статус:
                    <select v-model="taskNew.status">
                        <option v-for="status in statuses" :key="status.id" :value="status">
                            {{ status.name }}
                        </option>
                    </select>
                </div>
                <div class="priority-container">
                    Приоритет:
                    <select v-model="taskNew.priority">
                        <option v-for="priority in priorities" :key="priority.id" :value="priority">
                            {{ priority.name }}
                        </option>
                    </select>
                </div>
                <div class="labels-container">
                    Метки:
                    <TaskLabels :labels="taskNew.labels" @update:selectedLabels="updateLabels" />
                </div>
            </div>
        </div>
        <div class="description">
            <h2>Описание</h2>
            <TaskDescription :text="taskNew.description" @update:description="updateDescription" />
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

.date-container,
.status-container,
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