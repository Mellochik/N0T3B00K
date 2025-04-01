<script setup>
    import TaskSpaces from '@/components/tasks/TaskSpaces.vue';
    import TaskStacks from '@/components/tasks/TaskStacks.vue';
</script>

<template>
    <div class="page">
        <div class="spaces">
            <TaskSpaces/>
        </div>
        <div class="tasks">
            <TaskStacks title="Test"/>
            <TaskStacks title="Test1"/>
            <TaskStacks title="Test2"/>
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
    display: flex;
    flex: 1;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
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