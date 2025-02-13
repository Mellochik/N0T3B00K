<script setup>
import TaskIcon from '@/components/icons/TaskIcon.vue';
import TasksColumn from '@/components/tasks/TasksColumn.vue';
</script>

<template>
    <div class="page">
        <h1>
            <TaskIcon :size="40" />
            Задачи
        </h1>
        <div class="content">
            <div>
                <TasksColumn :title="'Не выполнено'" :status="'Не выполнено'" />
            </div>
            <div>
                <TasksColumn :title="'В работе'" :status="'В работе'" />
            </div>
            <div>
                <TasksColumn :title="'Готово'" :status="'Готово'" />
            </div>
        </div>
    </div>
</template>

<style scoped>
h1 {
    padding: 10px 10px;
}

.page {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.content {
    display: flex;
    flex-direction: row;
    gap: 10px;
}

.content > div {
  flex: 1 1 0px;
}

@media (max-width: 1200px) {
  .content {
    flex-direction: column;
  }
}
</style>