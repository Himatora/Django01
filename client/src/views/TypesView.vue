<script setup>
import { ref, onBeforeMount,computed } from 'vue';
import axios from 'axios';
const nameFilter = ref('');
const types = ref([]);
const typeToAdd = ref({});
const typeToEdit = ref({});
const typesPictureRef = ref(); // Для добавления нового типа
const editPictureRef = ref(); // Для редактирования изображения
const typesAddImageUrl = ref(); // URL изображения для добавления
const typesEditImageUrl = ref(); // URL изображения для редактирования
const zoomImageUrl = ref(''); // Для увеличения изображения
const stats=ref({});
async function fetchTypes() {
    const r = await axios.get("/api/types/");
    types.value = r.data;
}
async function fetchStats() {
  const r = await axios.get("/api/types/stats/");
  stats.value = r.data;
}

async function onTypesAdd() {
    const formData = new FormData();
    formData.append('picture', typesPictureRef.value.files[0]);
    formData.set('name', typeToAdd.value.name);
    await axios.post("/api/types/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchTypes();
    await fetchStats();
}

async function onTypeEditClick(type) {
    typeToEdit.value = { ...type };
    typesEditImageUrl.value = type.picture; // Устанавливаем URL изображения для редактирования
}

async function onUpdateType() {
    const formData = new FormData();
    if (editPictureRef.value.files[0]) {
        formData.append('picture', editPictureRef.value.files[0]);
    }
    formData.set('name', typeToEdit.value.name);
    await axios.put(`/api/types/${typeToEdit.value.id}/`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchTypes();
}

async function onRemoveClick(type) {
    await axios.delete(`/api/types/${type.id}/`);
    await fetchTypes();
    await fetchStats();
}

async function typesAddPictureChange() {
    typesAddImageUrl.value = URL.createObjectURL(typesPictureRef.value.files[0]);
}

async function typesEditPictureChange() {
    typesEditImageUrl.value = URL.createObjectURL(editPictureRef.value.files[0]);
}

function zoomImage(item) {
    zoomImageUrl.value = item.picture; // Устанавливаем URL для увеличения
}
const filteredTypes = computed(() => {
    return types.value.filter(item => {
        return (
            (!nameFilter.value || item.name.includes(nameFilter.value))
        );
    });
});
onBeforeMount(async () => {
    await fetchTypes();
    await fetchStats();
});
</script>

<template>
    <div class="p-2">
        <div>
            <h3>Типы</h3>
        </div>
        <form @submit.prevent="onTypesAdd">
            <div class="container-fluid">
                <div class="row p-2">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="typeToAdd.name" required>
                            <label for="floatingInput">Название</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <input class="form-control" type="file" ref="typesPictureRef" @change="typesAddPictureChange">
                    </div>
                    <div class="col-auto">
                        <img :src="typesAddImageUrl" style="max-height: 60px;" alt="">
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
                    <input type="text" class="form-control" v-model="nameFilter" placeholder="Фильтр по типу" />
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
        <div v-for="item in filteredTypes" class="smeh-item" :key="item.id">
            <div>{{ item?.name }}</div>
            <div v-show="item.picture">
                <img :src="item.picture" style="max-height: 60px;" alt=""
                     @click="zoomImage(item)" data-bs-toggle="modal" data-bs-target="#zoomImageModal">
            </div>
            <button class="btn btn-success" @click="onTypeEditClick(item)" data-bs-toggle="modal"
                    data-bs-target="#editSmehModal">
                <i class="bi bi-pen-fill"></i>
            </button>
            <button class="btn btn-danger" @click="onRemoveClick(item)">
                <i class="bi bi-x"></i>
            </button>
        </div>
    </div>
    <div class="modal fade" id="editSmehModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Редактировать</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col">
                            <div class="form-floating">
                                <input type="text" class="form-control" v-model="typeToEdit.name">
                                <label for="floatingInput">Название</label>
                            </div>
                        </div>
                        <div class="col-auto">
                            <input class="form-control" type="file" ref="editPictureRef" @change="typesEditPictureChange">
                        </div>
                        <div class="col-auto">
                            <img :src="typesEditImageUrl" style="max-height: 60px;" alt="">
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateType">Сохранить</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" id="zoomImageModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5">Изображение</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col">
                            <img :src="zoomImageUrl" style="max-height: 200px;" alt="">
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
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
    grid-template-columns: 1fr auto auto auto;
    gap: 20px;
    justify-content: space-between;
    align-content: center;
    align-items: center;
}
</style>
