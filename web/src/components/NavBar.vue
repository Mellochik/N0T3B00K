<script setup>
import HomeIcon from './icons/HomeIcon.vue';
import TaskIcon from './icons/TaskIcon.vue';
</script>

<template>
    <nav>
        <div class="links">
            <div class="logo">N0T3B00K</div>
            <router-link to="/" class="link">
                <HomeIcon />
                Домашняя
            </router-link>
            <router-link to="/tasks" class="link">
                <TaskIcon />
                Задачи
            </router-link>
        </div>
        <div class="profile">
            Профиль
        </div>
    </nav>
</template>

<style scoped>
nav {
    margin: 10px 10px 0px 10px; 
    padding: 10px;
    background-color: var(--quaternary-color);
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
    color: var(--primary-color);
    text-decoration: transparent;
}

.logo {
    font-size: 20px;
    font-weight: bold;
    color: var(--primary-color);
    padding-left: 10px;
    padding-right: 10px;
}

.link {
    font-size: 16px;
    color: var(--primary-color);
    background-color: var(--tertiary-color);
    padding: 5px 10px;
    border-radius: 10px;
    display: flex;
    text-align: center;
    gap: 10px;
    align-items: center;
}

.link:hover {
    background-color: var(--secondary-color);
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