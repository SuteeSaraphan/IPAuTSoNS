<template>
    <div>
        <h1>Drive page</h1>
        <h1>v-model</h1>
        <input v-model="email" type="email" placeholder="enter your fucking email">
        <div><h1>{{email}}</h1></div>
        <button @click="email=''">Reset</button>
    
    </div>
   
</template>

<script>
export default {
    name:"DriveView",
    data() {
        return {
        email:""
        }
    },
    methods: {
    
    },
};
</script>