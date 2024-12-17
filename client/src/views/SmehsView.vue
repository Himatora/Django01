<script setup>
import axios from '../axiosConfig';
import { computed, ref, onBeforeMount } from 'vue';
//import axios from 'axios';
import _ from 'lodash';
import { storeToRefs } from 'pinia';
import useUserStore from '../stores/userStore';
const smehs = ref([]);
const genders = ref({});
const ages = ref({});
const types = ref({});
const actors = ref({});
const users = ref({});//добавила
const selectedUser = ref(null); // Добавлено для фильтрации по пользователю
const smehsPictureRef = ref(); // Для добавления новоыго смеха
const smehAddImageUrl = ref(); // URL изображения для добавления
const smehToAdd = ref({});
const smehToEdit = ref({});
const loading = ref(false);
const editPictureRef = ref(); // Для редактирования изображения
const smehsEditImageUrl = ref(); // URL изображения для редактирования
const zoomImageUrl = ref(''); // Для увеличения изображения
const stats = ref({});
const gendersById = computed(() => _.keyBy(genders.value, x => x.id));
const agesById = computed(() => _.keyBy(ages.value, x => x.id));
const typesById = computed(() => _.keyBy(types.value, x => x.id));
const actorsById = computed(() => _.keyBy(actors.value, x => x.id));
const nameFilter = ref('');
const genderFilter = ref('');
const ageFilter = ref('');
const typeFilter = ref('');
const actorFilter = ref('');

const userStore = useUserStore();
const { isAuthenticated, username, userId, isSuperUser } = storeToRefs(userStore);

async function fetchGenders() {
  const r = await axios.get("/api/genders/");
  genders.value = r.data;
}

async function fetchAges() {
  const r = await axios.get("/api/ages/");
  ages.value = r.data;
}

async function fetchTypes() {
  const r = await axios.get("/api/types/");
  types.value = r.data;
}

async function fetchActors() {
  const r = await axios.get("/api/actors/");
  actors.value = r.data;
}
async function fetchStats() {
  const r = await axios.get("/api/smehs/stats/");
  stats.value = r.data;
}
async function fetchSmehs() {
  loading.value = true; // Устанавливаем состояние загрузки в true

  const params = isAuthenticated.value && userStore.isSuperUser
    ? {} // Если суперпользователь, параметры пустые, чтобы получить все записи
    : { user_id: selectedUser.value }; // В противном случае, используем user_id

  const r = await axios.get("/api/smehs/", { params }); // Делаем GET-запрос к API
  console.log(r.data); // Выводим данные в консоль
  smehs.value = r.data; // Сохраняем полученные данные в переменной smehs
  loading.value = false; // Устанавливаем состояние загрузки в false
}

async function fetchUsers() {

  const r = await axios.get("/api/user/");
  users.value = r.data; // Обновляем состояние с полученными пользователями

}

async function smehsAddPictureChange() {
  smehAddImageUrl.value = URL.createObjectURL(smehsPictureRef.value.files[0]);
}

async function smehsEditPictureChange() {
  smehsEditImageUrl.value = URL.createObjectURL(editPictureRef.value.files[0]);
}

function zoomImage(item) {
  zoomImageUrl.value = item.picture; // Устанавливаем URL для увеличения
}

async function onSmehsAdd() {
  const formData = new FormData();
  formData.append('picture', smehsPictureRef.value.files[0]);
  formData.set('name', smehToAdd.value.name);
  formData.set('gender', smehToAdd.value.gender);
  formData.set('type', smehToAdd.value.type);
  formData.set('age', smehToAdd.value.age);
  formData.set('actor', smehToAdd.value.actor);

  await axios.post("/api/smehs/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  await fetchSmehs();
  await fetchStats();
}

async function onSmehEditClick(smeh) {
  smehToEdit.value = { ...smeh };
  smehsEditImageUrl.value = smeh.picture; // Сохраняем текущее изображение для редактирования
}

async function onUpdateSmeh() {
  const formData = new FormData();
  if (editPictureRef.value.files[0]) {
    formData.append('picture', editPictureRef.value.files[0]);
  }
  formData.set('name', smehToEdit.value.name);
  formData.set('gender', smehToEdit.value.gender);
  formData.set('type', smehToEdit.value.type);
  formData.set('age', smehToEdit.value.age);
  formData.set('actor', smehToEdit.value.actor);

  await axios.put(`/api/smehs/${smehToEdit.value.id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  await fetchSmehs();
}
async function fetchSelectSmehs() {
  if (selectedUser.value == "") {
    console.log("Привет");
    const r = await axios.get("/api/smehs/");
    smehs.value = r.data;
  }
  else {
    const params = {
      user_id: selectedUser.value || (isAuthenticated.value && userStore.isSuperUser ? userId.value : null)
    };
    const r = await axios.get("/api/smehs/", { params });
    console.log(selectedUser.value);
    smehs.value = r.data;
    loading.value = false;
  }
}

async function onRemoveClick(smeh) {
  await axios.delete(`/api/smehs/${smeh.id}/`);
  await fetchSmehs();
  await fetchStats();
}
const filteredSmehs = computed(() => {
  return smehs.value.filter(item => {
    return (
      (!nameFilter.value || item.name.includes(nameFilter.value)) &&
      (!genderFilter.value || item.gender === genderFilter.value) &&
      (!ageFilter.value || item.age === ageFilter.value) &&
      (!typeFilter.value || item.type === typeFilter.value) &&
      (!actorFilter.value || item.actor === actorFilter.value)
    );
  });
});


onBeforeMount(async () => {
  await fetchUsers();
  await fetchSmehs();
  await fetchGenders();
  await fetchAges();
  await fetchTypes();
  await fetchActors();
  await fetchStats();
});
</script>

<template>
  <div class="p-2">
    <form @submit.prevent.stop="onSmehsAdd">
      <div class="container-fluid">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="smehToAdd.name" required>
              <label for="floatingInput">Имя</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="smehToAdd.gender" required>
                <option :value="g.id" v-for="g in genders" :key="g.id">{{ g.name }}</option>
              </select>
              <label for="floatingInput">Пол</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="smehToAdd.age" required>
                <option :value="a.id" v-for="a in ages" :key="a.id">{{ a.name }}</option>
              </select>
              <label for="floatingInput">Возраст</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="smehToAdd.type" required>
                <option :value="t.id" v-for="t in types" :key="t.id">{{ t.name }}</option>
              </select>
              <label for="floatingInput">Типы</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="smehToAdd.actor" required>
                <option :value="a.id" v-for="a in actors" :key="a.id">{{ a.name }}</option>
              </select>
              <label for="floatingInput">Актеры</label>
            </div>
          </div>
          <div class="col-auto" v-if="userStore.isSuperUser"><!--  -->
            <div class="form-floating">
              <select class="form-select" v-model="selectedUser" @change="fetchSelectSmehs">
                <option value="">Все</option>
                <option :value="user.id" v-for="user in users" :key="user.id">{{ user.username }}</option>
              </select>
              <label for="floatingInput">Пользователь</label>
            </div>
          </div>
          <div class="col-auto">
            <input class="form-control" type="file" ref="smehsPictureRef" @change="smehsAddPictureChange">
          </div>
          <div class="col-auto">
            <img :src="smehAddImageUrl" style="max-height: 60px;" alt="">
          </div>
          <div class="col-auto p-2">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </div>
    </form>
    <div class="filters mb-4">
      <div class="row g-3">
        <div class="col-md-3">
          <input type="text" class="form-control" v-model="nameFilter" placeholder="Фильтр по имени" />
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="genderFilter">
            <option value="">Все</option>
            <option :value="g.id" v-for="g in genders" :key="g.id">{{ g.name }}</option>
          </select>
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="ageFilter">
            <option value="">Все</option>
            <option :value="a.id" v-for="a in ages" :key="a.id">{{ a.name }}</option>
          </select>
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="typeFilter">
            <option value="">Все</option>
            <option :value="t.id" v-for="t in types" :key="t.id">{{ t.name }}</option>
          </select>
        </div>
        <div class="col-md-2">
          <select class="form-select" v-model="actorFilter">
            <option value="">Все</option>
            <option :value="a.id" v-for="a in actors" :key="a.id">{{ a.name }}</option>
          </select>
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
  <div v-if="loading">Гружу...</div>
  <div>
    <div v-for="item in filteredSmehs" class="smeh-item" :key="item.id">
      <div>{{ item?.name }}</div>
      <div>{{ gendersById[item.gender]?.name }}</div>
      <div>{{ agesById[item.age]?.name }}</div>
      <div>{{ typesById[item.type]?.name }}</div>
      <div>{{ actorsById[item.actor]?.name }}</div>
      <div v-show="item.picture">
        <img :src="item.picture" style="max-height: 60px;" alt="" @click="zoomImage(item)" data-bs-toggle="modal"
          data-bs-target="#zoomImageModal">
      </div>
      <button class="btn btn-success" @click="onSmehEditClick(item)" data-bs-toggle="modal"
        data-bs-target="#editSmehModal">
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>
    </div>
  </div>

  <!-- Модальное окно для увеличения изображения -->
  <div class="modal fade" id="zoomImageModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Изображение</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <img :src="zoomImageUrl" style="max-height: 200px;" class="img-fluid" alt="">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="editSmehModal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">Редактировать</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="row">
            <div class="col">
              <div class="form-floating">
                <input type="text" class="form-control" v-model="smehToEdit.name">
                <label for="floatingInput">Имя</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="smehToEdit.gender">
                  <option :value="g.id" v-for="g in genders" :key="g.id">{{ g.name }}</option>
                </select>
                <label for="floatingInput">Пол</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="smehToEdit.age">
                  <option :value="a.id" v-for="a in ages" :key="a.id">{{ a.name }}</option>
                </select>
                <label for="floatingInput">Возраст</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="smehToEdit.type">
                  <option :value="t.id" v-for="t in types" :key="t.id">{{ t.name }}</option>
                </select>
                <label for="floatingInput">Тип</label>
              </div>
            </div>
            <div class="col-auto">
              <div class="form-floating">
                <select class="form-select" v-model="smehToEdit.actor">
                  <option :value="a.id" v-for="a in actors" :key="a.id">{{ a.name }}</option>
                </select>
                <label for="floatingInput">Актер</label>
              </div>
            </div>
            <div class="col-auto">
              <input class="form-control" type="file" ref="editPictureRef" @change="smehsEditPictureChange">
            </div>
            <div class="col-auto">
              <img :src="smehsEditImageUrl" style="max-height: 60px;" alt="">
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
          <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateSmeh">Сохранить</button>
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
  grid-template-columns: 1fr auto auto auto auto auto auto auto;
  gap: 20px;
  justify-content: space-between;
  align-content: center;
  align-items: center;
}
</style>
