<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import HomeIcon from './icons/HomeIcon.vue';
import AddIcon from './icons/AddIcon.vue';
import TaskIcon from './icons/TaskIcon.vue';

const route = useRoute();
const isActiveLink = ref('Home');

onMounted(() => {
    updateActiveLink(route.path);
});

watch(() => route.path, (newPath) => {
    updateActiveLink(newPath);
});

function updateActiveLink(newPath) {
    if (newPath === '/') {
        isActiveLink.value = 'Home';
    } else if (newPath === '/tasks' || /^\/task(\/|$)/.test(newPath)) {
        isActiveLink.value = 'Tasks';
    }
}
</script>

<template>
    <nav>
        <div class="links">
            <div class="logo">N0T3B00K</div>
            <RouterLink to="/" class="link">
                <HomeIcon />
                Домашняя
            </RouterLink>
            <RouterLink to="/tasks" class="link">
                <TaskIcon />
                Задачи
            </RouterLink>
            <RouterLink to="/documents" class="link">
                <TaskIcon />
                Документы
            </RouterLink>
        </div>
        <div class="profile">
            Профиль
        </div>
    </nav>
</template>

<style scoped>
nav {
    margin: 10px calc(25% - 170px) 0px calc(25% - 170px); 
    padding: 10px;
    background-color: #1f1f1f;
    border-radius: 20px;
    display: flex;
    justify-content: space-between;
}

.links {
    display: flex;
    gap: 10px;
    align-items: center;
}

a {
    color: #8b8b8b;
    text-decoration: transparent;
}

.logo {
    font-size: 20px;
    font-weight: bold;
    color: #8b8b8b;
    padding-left: 10px;
    padding-right: 10px;
}

.link {
    font-size: 16px;
    color: #8b8b8b;
    padding: 5px 10px;
    border-radius: 10px;
    display: flex;
    text-align: center;
    gap: 10px;
    align-items: center;
}

.router-link-active {
    background-color: #2c2c2c;
}

.link:hover {
    background-color: #373737;
}

.profile {
    font-size: 16px;
    color: #8b8b8b;
    padding: 5px 10px;
    border-radius: 10px;
    display: flex;
    align-items: center;
}

.profile:hover {
    background-color: #373737;
}
</style>