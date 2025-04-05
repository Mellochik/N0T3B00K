<script setup>
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

import HomeIcon from '@/components/icons/HomeIcon.vue';
import TaskIcon from '@/components/icons/TaskIcon.vue';
import ProfileIcon from '@/components/icons/ProfileIcon.vue';

const route = useRoute();
const headerTitle = ref('');

const updateHeaderTitle = () => {
    if (route.path === '/') {
        headerTitle.value = 'Главная';
    } else if (route.path.startsWith('/tasks')) {
        headerTitle.value = 'Менеджер задач';
    } else {
        headerTitle.value = 'N0T3B00K';
    }
};

watch(route, updateHeaderTitle, { immediate: true });
</script>

<template>
    <header>{{ headerTitle }}</header>
    <nav>
        <div class="menu">
            <router-link :to="{ name: 'Home' }">
                <home-icon size="40px" />
            </router-link>
            <router-link :to="{ name: 'TasksWorkspaces' }">
                <task-icon size="40px" :color="`var(--text-color)`"/>
            </router-link>
        </div>
        <div class="profile">
            <router-link :to="{ name: 'Profile' }">
                <profile-icon size="40px" />
            </router-link>
        </div>
    </nav>
    <main>
        <router-view />
    </main>
</template>

<style scoped>
nav {
    grid-area: n;
    padding: 0px 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

header {
    grid-area: h;
    display: flex;
    align-items: center;
    justify-content: center;
}


main {
    grid-area: m;
    max-height: calc(100vh - 51px);
    border-top-left-radius: var(--border-radius-md);
    border-top: 1px solid var(--border-color);
    border-left: 1px solid var(--border-color);
    background-color: var(--background-color);
    display: flex;
    flex-direction: row;
    height: 100%;
    overflow: hidden;
}

.menu {
    display: flex;
    flex-direction: column;
    align-items: center; 
    gap: 10px;
}

.profile {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    align-items: center; 
    gap: 10px;
}

a {
    text-decoration: none;
    width: 50px;
    height: 50px;
    padding: 5px;
    background-color: var(--accent-background-color);
    font-size: var(--font-size-md);
    border-radius: var(--border-radius-md);
    display: flex;
    align-items: center; 
    justify-content: center;
    transition: background-color 0.3s ease;
}

a:hover {
    background-color: var(--primary-color);
}
</style>