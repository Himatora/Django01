import ActorsView from '../views/ActorsView.vue'
import AgesView from '../views/AgesView.vue'
import TypesViews from '../views/TypesView.vue'
import GendersView from '../views/GendersView.vue'
import SmehsView from '../views/SmehsView.vue'
import LoginPageView from '@/views/LoginPageView.vue';
import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name:"SmehsView",
      component:SmehsView
    },
    {
      path: "/genders",
      name:"GendersView",
      component:GendersView
    },
    {
      path: "/ages",
      name:"AgesView",
      component:AgesView
    },
    {
      path: "/types",
      name:"TypesView",
      component:TypesViews
    },
    {
      path: "/actors",
      name:"ActorsView",
      component:ActorsView
    },
    {
      path: "/user",
      name:"LoginPageView",
      component:LoginPageView
    }
  ]
})

export default router
