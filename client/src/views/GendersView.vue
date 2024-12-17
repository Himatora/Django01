<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';


const genders = ref([]);
const nameFilter = ref('');
const genderToAdd = ref({})
const genderToEdit = ref({})
const stats = ref({});
async function fetchGenders() {
    const r = await axios.get("/api/genders/");
    genders.value = r.data;
}
async function fetchStats() {
    const r = await axios.get("/api/genders/stats/");
    stats.value = r.data;
}

async function onGendersAdd() {
    const r = await axios.post("/api/genders/", {
        ...genderToAdd.value,
    });
    await fetchGenders();
}

async function onGenderEditClick(gender) {
    genderToEdit.value = { ...gender };
}

async function onUpdateGender() {
    const r = await axios.put(`/api/genders/${genderToEdit.value.id}/`, {
        ...genderToEdit.value
    })
    await fetchGenders();
    await fetchStats();
}

async function onRemoveClick(gender) {
    const r = await axios.delete(`/api/genders/${gender.id}/`)
    await fetchGenders();
    await fetchStats();
}
const filteredGenders = computed(() => {
    return genders.value.filter(item => {
        return (
            (!nameFilter.value || item.name.includes(nameFilter.value))
        );
    });
});
onBeforeMount(async () => {
    await fetchGenders();
    await fetchStats();
})
</script>

<template>
    <div class="p-2">
        <div>
            <h3>Пол</h3>
        </div>
        <form @submit.prevent.stop="onGendersAdd">
            <div class="container-fluid">
                <div class="row p-2">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="genderToAdd.name" required>
                            <label for="floatingInput">Название</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-primary">Добавить</button>
                    </div>
                </div>
            </div>
        </form>
        <div class="filters mb-4">
            <div class="row g-3">
                <div class="col-md-3">
                    <input type="text" class="form-control" v-model="nameFilter" placeholder="Фильтр по полу" />
                </div>
            </div>
        </div>
    </div>
    <div class="container ">
        <table class="table table-bordered">
            <thead class="thead-light">
                <tr>
                    <th>Всего</th>
                    <th>Среднее</th>
                    <th>Максимум</th>
                    <th>Минимум</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{{ stats.count }}</td>
                    <td>{{ stats.avg }}</td>
                    <td>{{ stats.max }}</td>
                    <td>{{ stats.min }}</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div>
        <div v-for="item in filteredGenders" class="smeh-item" :key="item.id">
            <div>{{ item?.name }}</div>
            <button class="btn btn-success" @click="onGenderEditClick(item)" data-bs-toggle="modal"
                data-bs-target="#editSmehModal">
                <i class="bi bi-pen-fill"></i></button>
            <button class="btn btn-danger" @click="onRemoveClick(item)"><i class="bi bi-x"></i></button>
        </div>
    </div>
    <div class="modal fade" id="editSmehModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">
                        редактировать
                    </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="genderToEdit.name">
                                <label for="floatingInput">Название</label>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                Close
                            </button>
                            <button data-bs-dismiss="modal" type="button" class="btn btn-primary"
                                @click="onUpdateGender">
                                Сохранить
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.smeh-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    box-shadow: 0 0 4px silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr auto auto;
    gap: 20px;
    justify-content: space-between;
    align-content: center;
    align-items: center;
}
</style>
