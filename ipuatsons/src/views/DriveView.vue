<template>
    <div>
        <SlideBar></SlideBar>
        <div class="main-home">
            <h1>Drive page</h1>
            <h1>v-model</h1>
            <input type="file" accept="image/*" @change="uploadImage($event)" id="file-input" multiple="multiple">
            <hr>
            <label for="folder">Folder : </label>
            <input type="text" id="folder" name="folder">
            <button @click="onUploadFile" style="color:black">Upload</button>


        </div>
    </div>
</template>

<script>
import SlideBar from '@/components/SlideBar'
import { useCookies } from "vue3-cookies";
import router from '@/router';
import axios from 'axios';
export default {
    name: "DriveView",
    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },
    data() {
        return {
            selectedFile: [],
            token_url: "",

        }
    },
    methods: {

        uploadImage(event) {
            this.selectedFile=[]
            for(let i = 0;i< event.target.files.length;i++){
                this.selectedFile.push(event.target.files[i])
            }

            
            
        },
        onUploadFile(){
            const URL = 'http://127.0.0.1:8000/api/image';
            let data = new FormData();
            data.append('jwt', this.cookies.get('jwt'));
            data.append('folder',document.getElementById("folder").value);
            console.log(this.selectedFile[0])
            
            for(let i = 0;i< this.selectedFile.length;i++){
                data.append('img_file', this.selectedFile[i]);
            }
            
            let config = {
                header: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            axios.post(
                URL,
                data,
                config
            ).then(
                response => {
                    console.log('image upload response > ', response)
                }
            )
        }
    }
    ,
    components: {
        SlideBar
    },
    created() {
        if (this.cookies.get('jwt') == null) {
            alert("You are not login yet , please login fisrt")
            router.push('login')
        }
    }
};
</script>