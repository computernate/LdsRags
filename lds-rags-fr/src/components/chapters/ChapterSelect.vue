<template>
    <div class="wrapper">
        <div class="section">
            <p @click="showgcbyauthorfunc">General Conference (By Author)</p>
            <div v-show="showgcbyauthor">Loading</div>
        </div>
        <div class="section">
            <p>General Conference (By Year)</p>
        </div>
        <div class="section">
            <p>Book of Mormon</p>
        </div>
        <div class="section">
            <p>50 random unanalyzed talks</p>
        </div>
    </div>
</template>

<script>

export default {
  name: 'ChapterSelect',
  data() {
    return {
      showgcbyauthor: null,
      gcbyauthor: null,
      showgcbyyear: null,
      gcbyyear: null,
      showbom:null,
      bom:null,
      showunanalized:null,
      unanalized:null,
    }
  },
  methods: {
    showgcbyauthorfunc(){
        if(this.showgcbyauthor){
            this.showgcbyauthor=false
            return
        }
        this.showgcbyauthor=true
    }
  }
}
</script>

<style scoped>
    .wrapper{
        background-color:grey;
        padding:20px;
        width:300px;
        height:100%;
    }
</style>