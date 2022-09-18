<template>
    <div>
    <SlideBar></SlideBar>
    <div class="main-home">
        <h1>Drive page</h1>
        <h1>v-model</h1>
        <input v-model="email" type="email" placeholder="enter your email">
        <div>
            <h1>{{ email }}</h1>
        </div>
        <button @click="email = ''" style="color:black">Reset</button>
        <button @click="get_token" style="color:black">get_token</button>

    </div>
</div>
</template>

<script>
import SlideBar from '@/components/SlideBar'
import { useCookies } from "vue3-cookies";
import router from '@/router';
export default {
    name: "DriveView",
    setup() {
        const { cookies } = useCookies();
        return { cookies };
  },
    data() {
        return {
            email: "",
            token_url: "",
        }
    },
    methods: {
        
    },
    components:{
        SlideBar
    },
    created(){
    if (this.cookies.get('jwt')==null){
      alert("You are not login yet , please login fisrt")
      router.push('login')
    }
  }
};
</script>