<template>
  <div>
    <h1>v-model</h1>
    <input v-model="email" type="email" placeholder="enter your fucking email">
    <div>{{email}}</div>
    <button @click="email=''">Reset</button>

  </div>
</template>

<script>
export default {
  name: "app",
  data() {
    return {
      email:""
    }
  },
  methods: {
    
  },

}
</script>

<style>

</style>