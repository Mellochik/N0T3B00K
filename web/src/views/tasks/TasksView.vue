<script setup>
    import TaskColumn from '@/components/tasks/TaskColumn.vue';
</script>

<template>
    <div class="page">
        <div class="spaces">
        </div>
        <div class="tasks">
        </div>
    </div>
</template>

<style scoped>
.page {
    display: flex;
    flex-direction: row;
    gap: 10px;
}

.spaces {
    min-width: 400px;
    background-color: #1f1f1f;
    border-radius: 20px;
    flex: 1;
}

.tasks {
    overflow-x: auto;
    overflow-y: auto;
    background-color: #1f1f1f;
    border-radius: 20px;
    flex: 3;
    display: flex;
    flex-direction: row;
    gap: 10px;
}
</style>