<template>
    <div>
        <SlideBar></SlideBar>
        <div class="main-home">
            <h1>Image Folder page</h1>
            Folder name : {{ this.files[0].folder_name }}
            <form style="padding:5px;">
                <input type="file" accept="image/*" @change="uploadImage($event)" id="file-input" multiple="multiple">
                <button type="button" @click="onUploadFile" style="color:black">Upload</button>
            </form>
            <hr>
            <div class="row">
                <div class="column" v-for="image in this.images" v-bind:key="image.img_id">
                    <div class="content">
                        <div class="card">
                            <img style='display:block; width:250px;height:200px; object-fit: scale-down; border: 1px; image-rendering: auto;'
                                :src="`data:image/jpeg;base64,${image.img_data}`" alt="{{ image.img_id }}">
                            <div class="container" >
                                {{ image.img_id }}
                                {{image.img_type}}

                                <button style="background-color: red;padding:2px;" @click="deleteImage(image.img_id)" >Delete</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import SlideBar from '@/components/SlideBar'
import { useCookies } from "vue3-cookies";
import router from '@/router';
import axios from 'axios';
const URL_IMG_FOLDER = 'http://127.0.0.1:8000/api/folder_img';
const URL_IMG_UPLOAD = 'http://127.0.0.1:8000/api/upload_image';
const URL_GET_IMG = 'http://127.0.0.1:8000/api/image';



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
            files: [],
            images: [],
            owner: 0
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

            let data = new FormData();
            data.append('jwt', this.cookies.get('jwt'));
            data.append('folder', this.files[0].folder_name);

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
                URL_IMG_UPLOAD,
                data,
                config
            ).then(
                async (response) => {
                    alert('image upload response >' + response.data['status'])
                    location.reload();
                }
            )
        },

        deleteImage(img_id){
            axios.defaults.headers.delete['jwt'] = this.cookies.get('jwt');
            axios.delete(URL_GET_IMG + "/" + img_id)
            .then(async res =>{
                alert(res.data['status']);
                location.reload();
            })
        }



    }
    ,
    components: {
        SlideBar
    },
    created() {

        if (this.cookies.get('jwt') == null) {
            alert("You are not login yet , please login fisrt")
            router.push('/login')
        }
        else {
            axios.defaults.headers.get['jwt'] = this.cookies.get('jwt');
            axios.get(URL_IMG_FOLDER)
                .then(res => {
                    this.files = res.data
                    for (let i in this.files) {
                        if (this.$route.params.folder_id == this.files[i].folder_id) {
                            this.owner += 1
                        }
                    }

                    if (this.owner != 1) {
                        alert("You can not access this folder");
                        router.push('/drive')
                    } else {
                        axios.get(URL_GET_IMG + "/" + this.$route.params.folder_id)
                            .then(res => {
                                //console.log(res.data)
                                this.images = res.data
                            })
                    }


                })
                .catch(err => console.log(err.data))


        }
    }
};
</script>
