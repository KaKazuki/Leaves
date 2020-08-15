import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/primer',
    name: 'Primer',
    component: () => import('../views/Primer.vue')
  },
  {
    path: '/blast',
    name: 'Blast',
    component: () => import('../views/Blast.vue')
  },
  {
    path: '/conversion',
    name: 'Conversion',
    component: () => import('../views/Conversion.vue')
  },
  {
    path: '/memo',
    name: 'Memo',
    component: () => import('../views/Memo.vue')
  },
  {
    path: '/alignment',
    name: 'Alignment',
    component: () => import('../views/Alignment')
  },
  {
    path: '/*',
    name: 'NotFound',
    component: () => import('../views/NotFound')
  }

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
