import Vue from 'vue'
import Router from 'vue-router'
import Label from '@/views/Label.vue'
import Record from '@/views/Record.vue'
import Tape from '@/views/Tape.vue'

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
      path: '/tape',
      name: 'Tape',
      component: Tape
    }
  ]
})
