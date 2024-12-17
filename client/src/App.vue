<script setup>
import { storeToRefs } from 'pinia';
import useUserStore from './stores/userStore';
const userStore = useUserStore();
const {
  isAuthenticated,
  username,
  userId
} = storeToRefs(userStore);
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Navbar</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Смешарики</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/genders">Пол</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/ages">Возрасты</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/types">Типы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/actors">Актеры</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item dropdown" v-if="isAuthenticated">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                aria-expanded="false">
                {{ username }}
              </a>
              <ul class="dropdown-menu">
                <li>
                  <a href="/admin" class="dropdown-item">Админка</a>
                  <a href="/user" class="dropdown-item">Профиль</a>
                </li>
              </ul>
            </li>
            <li class="nav-item" v-else>
              <router-link class="nav-link" to="/user">Вход</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <div class="container">
    <router-view />
  </div>
</template>

<style scoped></style>