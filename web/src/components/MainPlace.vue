<template>
    <main>
        <RouterView />
    </main>
</template>

<style scoped>
main {
    overflow-y: auto;
    margin: 0px 10px 10px 10px; 
    height: calc(100vh - 20px);
    max-height: 100vh;
}
</style>