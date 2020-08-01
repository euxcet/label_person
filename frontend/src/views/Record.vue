<template>
    <div class="main">
      <div v-html="title" class="record-title"></div>
      <div v-html="message" class="record-message"></div>
      <span class="record-remain">{{count}}</span>
      <div class="record-row">
        <el-button class="record-button" size="small" type="primary" @click="getTask">{{button}}</el-button>
      </div>
      <img class="cross" :src="cross" :height=cross_height :style="{'top':position.x,'left':position.y}">
    </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'Record',
  data () {
    return {
      begin_url: 'http://127.0.0.1:5000/begin',
      end_url: 'http://127.0.0.1:5000/end',
      button: '录制',
      title: '',
      message: '',
      query: {
        'stage': 0,
        'task': 0,
        'count': 1
      },
      count: '',
      cross_height: 150,
      position: {
        'x': '-200px',
        'y': '-200px'
      },
      cross: require('../assets/image/cross.jpg')
    }
  },
  mounted () {
    // this.getTask()
  },
  methods: {
    getTask () {
      if (this.button === '开始') {
        axios.post(this.begin_url, this.query, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }).then(response => {
          this.button = '结束'
        })
      } else if (this.button === '结束' || this.button === '录制') {
        axios.post(this.end_url, this.query, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }).then(response => {
          if (response.data.hascross) {
            this.cross_height = 150
          } else {
            this.cross_height = 0
          }
          this.query.stage = response.data.stage
          this.query.task = response.data.task
          this.query.count = response.data.count
          this.count = '剩余次数：' + response.data.remain.toString()
          this.title = response.data.title
          this.message = response.data.message
          this.position.x = response.data.x.toString() + 'px'
          this.position.y = response.data.y.toString() + 'px'
          this.button = '开始'
        })
      }
    }
  }
}
</script>
