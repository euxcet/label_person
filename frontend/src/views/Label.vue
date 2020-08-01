<template>
  <div class="main">
    <img :src="'data:image/jpeg;base64,'+imageBytes" :height=400 />
    <div class="button-row">
        <el-button class="label-button" size="small" type="primary" @click="goBack">上一张</el-button>
        <el-button class="label-button" size="small" type="danger" @click="update(0)">框定错误</el-button>
    </div>
    <div class="button-row">
        <el-button class="label-button" size="small" type="success" @click="update(1)">向上</el-button>
    </div>
    <div class="button-row">
        <el-button class="label-button" size="small" type="success" @click="update(3)">向左</el-button>
        <el-button class="label-button" size="small" type="success" @click="update(2)">向下</el-button>
        <el-button class="label-button" size="small" type="success" @click="update(4)">向右</el-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Label',
  data () {
    return {
      next_url: 'http://127.0.0.1:5000/next',
      image_url: 'http://127.0.0.1:5000/image',
      score_url: 'http://127.0.0.1:5000/score',
      back_url: 'http://127.0.0.1:5000/back',
      imageBytes: '',
      id: 'null'
    }
  },
  mounted () {
    this.getImage()
  },
  methods: {
    goBack () {
      axios.post(this.back_url, {'id': this.id}, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).then(response => {
        this.id = response.data.id
        axios.post(this.image_url, {'id': this.id}, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }).then(response => {
          this.imageBytes = response.data
        })
      })
    },
    update (score) {
      axios.post(this.score_url, {'id': this.id, 'score': score}, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).then(response => {
        this.getImage()
      })
    },
    getImage () {
      axios.post(this.next_url, {'id': this.id}, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).then(response => {
        this.id = response.data.id
        axios.post(this.image_url, {'id': this.id}, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }).then(response => {
          this.imageBytes = response.data
        })
      })
    }
  }
}
</script>
