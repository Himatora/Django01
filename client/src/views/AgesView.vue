<script setup>
import { computed, ref, onBeforeMount } from 'vue';
import axios from 'axios';
import _ from 'lodash';


const ages = ref([]);
const nameFilter = ref('');
const ageToAdd = ref({})
const ageToEdit = ref({})
const stats=ref({});
async function fetchAges() {
    const r = await axios.get("/api/ages/");
    ages.value = r.data;
}
async function fetchStats() {
  const r = await axios.get("/api/ages/stats/");
  stats.value = r.data;
}
async function onAgesAdd() {
    const r = await axios.post("/api/ages/", {
        ...ageToAdd.value,
    });
    await fetchAges();
    await fetchStats();
}

async function onAgeEditClick(age) {
    ageToEdit.value = { ...age };
}

async function onUpdateAge() {
    const r = await axios.put(`/api/ages/${ageToEdit.value.id}/`, {
        ...ageToEdit.value
    })
    await fetchAges();
    await fetchStats();
}

async function onRemoveClick(age) {
    const r = await axios.delete(`/api/ages/${age.id}/`)
    await fetchAges();
}
const filteredAges = computed(() => {
    return ages.value.filter(item => {
        return (
            (!nameFilter.value || item.name.includes(nameFilter.value))
        );
    });
});
onBeforeMount(async () => {
    await fetchAges();
    await fetchStats();
})
</script>

<template>
    <div class="p-2">
        <div><h3>Возрасты</h3></div>
        <form @submit.prevent.stop="onAgesAdd">
            <div class="container-fluid">
                <div class="row p-2">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="ageToAdd.name" required>
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
                    <input type="text" class="form-control" v-model="nameFilter" placeholder="Фильтр по возрасту" />
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
          <td>{{stats.avg}}</td>
          <td>{{stats.max}}</td>
          <td>{{stats.min}}</td>
        </tr>
      </tbody>
    </table>
  </div>
    <div>
        <div v-for="item in filteredAges" class="smeh-item">
            <div>{{ item?.name }}</div>
            <button class="btn btn-success" @click="onAgeEditClick(item)" data-bs-toggle="modal"
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
                                <input type="text" class="form-control" v-model="ageToEdit.name">
                                <label for="floatingInput">Название</label>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                Close
                            </button>
                            <button data-bs-dismiss="modal" type="button" class="btn btn-primary"
                                @click="onUpdateAge">
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
