<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { getRequest } from '@/api/requests.js';

const spaces = ref([]);
const route = useRoute();
const router = useRouter();

const selectedSpaceId = computed(() => Number(route.params.id));

async function loadSpaces() {
    try {
        const response = await getRequest('/spaces');
        spaces.value = response;
    } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
    }
}

async function selectSpace(spaceId) {
    router.push({ name: 'TasksStacks', params: { id: spaceId } });
}

onMounted(() => {
    loadSpaces();
});
</script>

<template>
    <div id="spaces-view">
        <div class="control-panel">
            <div class="title">
                Рабочие пространства
            </div>
            <div class="controls">

            </div>
        </div>
        <div class="spaces">
            <div 
                class="space" 
                v-for="space in spaces" 
                :key="space.id" 
                @click="selectSpace(space.id)" 
                :class="{ selected: selectedSpaceId === space.id }"
            >
                {{ space.name }}
            </div>
        </div>
    </div>
    <router-view />
</template>

<style scoped>
#spaces-view {
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
}

.control-panel {
    height: 50px;
    background-color: var(--background-color);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.title {
    margin-left: 10px;
    padding: 10px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.spaces {
    width: 300px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;
    padding: 10px;
}


.space {
    padding: 10px;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-md);
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.space:hover {
    background-color: var(--accent-background-color);
}

.space.selected {
    background-color: var(--accent-background-color);
}
</style>
