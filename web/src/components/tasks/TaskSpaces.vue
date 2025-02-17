<template>
    <div class="spaces">
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
</template>

<style scoped>
.spaces {
    background-color: #f0f0f0;
}
</style>