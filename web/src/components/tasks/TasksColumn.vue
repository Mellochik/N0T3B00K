<script setup>
import TaskCard from './TaskCard.vue'
import { ref, onMounted } from 'vue'

const props = defineProps({
    title: String,
    status: String
});

const tasks = ref([]);

const statusValue = ref(props.status)

onMounted(async () => {
    var response;
    if (statusValue.value) {
        response = await fetch(`http://127.0.0.1:8000/tasks/read/${statusValue.value}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
    } else {
        response = await fetch(`http://127.0.0.1:8000/tasks/read/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
    }

    const data = await response.json()
    tasks.value = data
});
</script>

<template>
    <h2 v-if="title">
        {{ title }}
    </h2>
    <div class="task-column">
        <TaskCard v-for="task in tasks" :key="task.id" :task="task" />
    </div>
</template>

<style scoped>
h2 {
    padding: 10px 20px;
}

.task-column {
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;
    padding: 10px;
}
</style>