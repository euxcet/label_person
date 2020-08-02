<template>
  <div class="main">
    <img :src="'data:image/jpeg;base64,'+imageBytes" :height=400 />
    <div class="button-row">
        <el-button class="label-button" size="small" type="primary" @click="goBack">上一张</el-button>
        <el-button class="label-button" size="small" type="danger" @click="update(0)">框定错误</el-button>
    </div>
    <div class="button-row">
        <el-button class="label-button" size="small" type="success" @click="update(1)">背对</el-button>
    </div>
    <div class="button-row">
        <el-button class="label-button" size="small" type="success" @click="update(3)">向左</el-button>
        <el-button class="label-button" size="small" type="success" @click="update(2)">正对</el-button>
        <el-button class="label-button" size="small" type="success" @click="update(4)">向右</el-button>
    </div>
    <div class="tip-rows">
      <div class="tip-row"><p style="font-weight: bold">说明：</p></div>
      <div class="tip-row"><p> 1. 若图中人头部的大部分区域没有被包含在绿色框中或人远离屏幕则点击框定错误</p></div>
      <div class="tip-row"><p> 2. 若框定正确，按照绿色框中人脸的朝向选择背对屏幕、正对屏幕、朝向图片左边、朝向图片右边中的一项</p></div>
      <div class="tip-row"><p> 3. 选择错误时可以点击上一张按钮重新标注</p></div>
      <div class="tip-row"><p> 4. 快捷键：上一张[b] 框定错误[f] 背对[w] 正对[s] 向左[a] 向右[d]</p></div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Label',
  created () {
    document.addEventListener('keyup', this.handleKeyUp)
  },
  destroyed () {
    document.removeEventListener('keyup', this.handleKeyUp)
  },
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
    handleKeyUp (event) {
      const e = event || window.event || arguments.callee.caller.arguments[0]
      if (!e) return
      const {key, keyCode} = e
      if (keyCode == 87) { // w
        this.update(1)
      }
      else if (keyCode == 83) { // s
        this.update(2)
      }
      else if (keyCode == 65) { // a
        this.update(3)
      }
      else if (keyCode == 68) { // d
        this.update(4)
      }
      else if (keyCode == 66) { // b
        this.goBack()
      }
      else if (keyCode == 70) { // f
        this.update(0)
      }
    },
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
