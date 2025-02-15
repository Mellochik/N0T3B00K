<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
</script>

<template>
    <main>
        <RouterView />
    </main>
</template>

<style scoped>
main {
    overflow-y: auto;
    margin: 10px;
    border-radius: 20px;
    background-color: #1f1f1f;
}
</style>