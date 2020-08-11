import Vue from 'vue'
import Router from 'vue-router'
import Label from '@/views/Label.vue'
import Record from '@/views/Record.vue'
import Meta from '@/views/Meta.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Label',
      component: Label
    },
    {
      path: '/record',
      name: 'Record',
      component: Record
    },
    {
      path: '/meta',
      name: 'Meta',
      component: Meta
    }
  ]
})
