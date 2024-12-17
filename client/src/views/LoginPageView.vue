<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import useUserStore from '@/stores/userStore';
import axios from 'axios';
const username = ref("");
const pass = ref("");
const useStore = useUserStore();
const router = useRouter();

async function login() {
    let token = $cookies.get('csrftoken')
    console.log(token);
    
    try {
        const response = await axios.post("/api/user/login/", {
            user: username.value,
            pass: pass.value
        }, {headers: {
            'X-CSRFToken': token,
        }});
        await useStore.fetchUser();
        router.push("/");
    } catch (error) {
        console.error("Ошибка при входе:", error);
        // Здесь можно добавить обработку ошибок, например, уведомление пользователя
    }
}
</script>

<template>
    <div class="container mt-5">
        <h1 class="text-center">Вход</h1>
        <form @submit.prevent="login" class="w-50 mx-auto">
            <div class="mb-3">
                <label for="username" class="form-label">Имя пользователя:</label>
                <input type="text" class="form-control" id="username" v-model="username" required />
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Пароль:</label>
                <input type="password" class="form-control" id="password" v-model="pass" required />
            </div>
            <button type="submit" class="btn btn-primary w-100">Войти</button>
        </form>
    </div>
</template>