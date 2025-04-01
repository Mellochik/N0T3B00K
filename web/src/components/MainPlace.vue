<template>
    <main>
        <RouterView />
    </main>
</template>

<style scoped>
main {
    margin: 0px 10px 10px 10px; 
    height: calc(100vh - 20px);
    max-height: 100vh;
    min-width: 600px;
}

main > * {
    height: 100%;
}
</style>