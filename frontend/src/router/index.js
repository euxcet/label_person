import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/views/Login.vue'
import Record from '@/views/Record.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/record',
      name: 'Record',
      component: Record
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})
