<template>
  <div>
    

    <ul>
      <li><router-link to="/">Home</router-link> </li>
      <li><router-link to="/drive">Drive</router-link> </li>
    </ul>

    <router-view></router-view>
    
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