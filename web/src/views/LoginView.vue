<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import BaseInput from '@/components/base/BaseInput.vue';
import BaseButton from '@/components/base/BaseButton.vue';

const username = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();

const handleSubmit = async () => {
    errorMessage.value = '';

    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                username: username.value,
                password: password.value
            }).toString()
        });

        if (response.status === 401) {
            errorMessage.value = 'Неверный логин или пароль';
            return;
        }

        if (response.status >= 500) {
            return new Error('Серверная ошибка. Попробуйте позже.');
        }

        const data = await response.json();
        if (data.access_token) {
            localStorage.setItem('access_token', data.access_token);
            router.push('/');
        } else {
            return new Error('Токен отсутствует в ответе');
        }
    } catch (error) {
        console.error(error);
        alert(error);
    }
};
</script>

<template>
    <div id="login-view">
        <form @submit.prevent="handleSubmit" class="login-form">
            <h1>Вход</h1>
            <div class="form-group">
                <label for="login">Логин</label>
                <BaseInput id="login" v-model="username" required />
            </div>
            <div class="form-group">
                <label for="password">Пароль</label>
                <BaseInput id="password" type="password" v-model="password" required />
            </div>
            <BaseButton type="submit">Войти</BaseButton>
            <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
            <p class="register-link">
                Нет аккаунта? <BaseLink href="/register">Зарегистрироваться</BaseLink>
            </p>
        </form>
    </div>
</template>

<style scoped>
#login-view {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.login-form {
    padding: 20px;
    width: 300px;
    background: var(--background-color);
    border-radius: 20px;
    text-align: center;
}

.form-group {
    margin-bottom: 20px;
    text-align: left;
}

h1 {
    margin: 0px 0px 20px 0px;
    font-size: var(--font-size-xl)
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: var(--font-size-lg);
}

.register-link {
    font-size: var(--font-size-sm);
    margin: 0px;
}

.error-message {
    color: red;
    margin-top: 10px;
    font-size: var(--font-size-sm);
}
</style>