<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; 

import BaseInput from '@/components/base/BaseInput.vue';
import BaseButton from '@/components/base/BaseButton.vue';

const login = ref('');
const password = ref('');
const email = ref('');
const firstName = ref('');
const lastName = ref('');
const router = useRouter();

const handleSubmit = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        login: login.value,
        password: password.value,
        email: email.value,
        first_name: firstName.value,
        last_name: lastName.value
      })
    });

    const data = await response.json();
    console.log('Response:', data);

    if (!response.ok) {
      throw new Error(data.detail || 'Ошибка регистрации');
    }
    
    router.push('/login');
  } catch (error) {
    console.error(error.message);
    alert(error.message);
  }
};
</script>

<template>
  <div class="register-container">
    <form @submit.prevent="handleSubmit" class="register-form">
      <h1>Регистрация</h1>
      <div class="form-group">
        <label for="login">Логин</label>
        <BaseInput id="login" v-model="login" required />
      </div>
      <div class="form-group">
        <label for="password">Пароль</label>
        <BaseInput id="password" type="password" v-model="password" required />
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <BaseInput id="email" type="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="firstName">Имя</label>
        <BaseInput id="firstName" v-model="firstName" required />
      </div>
      <div class="form-group">
        <label for="lastName">Фамилия</label>
        <BaseInput id="lastName" v-model="lastName" required />
      </div>
      <BaseButton type="submit">Зарегистрироваться</BaseButton>
      <p class="login-link">
        Уже есть аккаунт? <BaseLink href="/login">Войти</BaseLink>
      </p>
    </form>
  </div>
</template>

<style scoped>
.register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: var(--quinary-color);
}

.register-form {
    background: var(--quaternary-color);
    padding: 20px;
    border-radius: 20px;
    width: 300px;
    text-align: center;
}

.form-group {
    margin-bottom: 20px;
    text-align: left;
}

h1 {
    margin: 0px 0px 20px 0px;
    color: var(--primary-color);
    font-size: var(--font-size-xxl)
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: var(--font-size-md);
}

.login-link {
    font-size: var(--font-size-sm);
    margin: 0px;
}
</style>