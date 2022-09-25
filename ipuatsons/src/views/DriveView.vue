<template>
    <div>
    <SlideBar></SlideBar>
    <div class="main-home">
        <h1>Drive page</h1>
        <h1>v-model</h1>
        <input type="file" @change="onFileSelected">
        <button @click="onUploadFile">Upload</button>


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
            selectedFile: null,
            token_url: "",
        }
    },
    methods: {
        onFileSelected(event){
            this.selectedFile = event.target.files[0]
        },
        onUploadFile(){
            
        }
        
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