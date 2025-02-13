<script setup>
import TaskCard from './TaskCard.vue'
import { ref, onMounted } from 'vue'

const props = defineProps({
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
    <div class="task-grid-container">
        <div class="task-grid">
            <TaskCard v-for="task in tasks" :key="task.id" :task="task" />
        </div>
    </div>
</template>

<style scoped>
.task-grid-container {
    flex: 1;
    overflow-y: auto;
    padding: 10px 10px 10px 10px;
}

.task-grid {
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(4, 1fr);
}

@media (max-width: 1400px) {
    .task-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 1200px) {
    .task-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 1000px) {
    .task-grid {
        grid-template-columns: repeat(1, 1fr);
    }
}
</style>