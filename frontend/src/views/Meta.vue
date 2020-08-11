<template>
  <div>
    <p>图片总数：{{all_cnt}}</p>
    <p>最少标注次数：{{min_val}}</p>
    <p>最少标注图片图：{{min_cnt}}</p>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Tape',
  data () {
    return {
      url: 'http://127.0.0.1:5000/meta',
      all_cnt: 0,
      min_val: 0,
      min_cnt: 0
    }
  },
  mounted () {
    axios.post(this.url, {}, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    }).then(response => {
      this.all_cnt = response.data.all_cnt
      this.min_val = response.data.min_val
      this.min_cnt = response.data.min_cnt
    })
  },
  methods: {
  }
}
</script>
