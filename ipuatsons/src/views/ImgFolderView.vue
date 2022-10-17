<template>
    <div>
        <SlideBar></SlideBar>
        <div class="main-home">
            <h1>Image Folder page</h1>
            <form style="padding:5px;">
                <input type="file" accept="image/*" @change="uploadImage($event)" id="file-input" multiple="multiple">
                <button type="button" @click="onUploadFile" style="color:black">Upload</button>
            </form>

        </div>
    </div>
</template>

<script>
import SlideBar from '@/components/SlideBar'
import { useCookies } from "vue3-cookies";
import router from '@/router';
import axios from 'axios';

export default {

    name: "ImgFolderView",
    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },
    data() {
        return {
            selectedFile: [],
            token_url: "",
            files: []
        }
    },
    methods: {

        uploadImage(event) {
            this.selectedFile = []
            for (let i = 0; i < event.target.files.length; i++) {
                this.selectedFile.push(event.target.files[i])
            }



        },
        onUploadFile() {
            const URL = 'http://127.0.0.1:8000/api/image';
            let data = new FormData();
            data.append('jwt', this.cookies.get('jwt'));
            data.append('folder', document.getElementById("folder").value);

            //console.log(this.selectedFile[0])

            for (let i = 0; i < this.selectedFile.length; i++) {
                data.append('img_file', this.selectedFile[i]);
            }

            //console.log(data)

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
                async (response) => {
                    alert('image upload response >' + response.data['status'])
                    location.reload();
                }
            )
        },



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
        else {
            axios.defaults.headers.get['jwt'] = this.cookies.get('jwt');
            const URL = 'http://127.0.0.1:8000/api/folder_img';
            axios.get(URL)
                .then(res => this.files = res.data)
                .catch(err => console.log(err.data))

        }
    }
};
</script>