<template>
    <div>
        <SlideBar></SlideBar>
        <div class="main-home">
            <div class="loading" v-if="this.isLoading">Loading&#8230;</div>
            <h1>Image Folder page</h1>
            <h2 v-if="this.files.length == 0">Folder name : Untitle</h2>
            <h2 v-if="this.files.length != 0">Folder name : {{ this.files[0].folder_name }}</h2>

            <!-- upload image here  -->
            <form style="padding:5px;">
                <input type="file" accept="image/*" @change="uploadImage($event)" id="file-input" multiple="multiple">
                <button type="button" @click="onUploadFile" style="color:black">Upload</button>
            </form>

            <hr>

            <!-- show image here  -->
            <div class="row">
                <div class="column" v-for="image in this.images" v-bind:key="image.img_id">
                    <div class="content">
                        <div class="card">


                            <img style='display:block; 
                                        width:200px;
                                        height:200px;
                                        object-fit: scale-down; 
                                        border: 1px; 
                                        image-rendering: auto;' :src="`data:image/jpeg;base64,${image.img_data}`"
                                alt="{{ image.img_id }}">


                            <div class="container"
                                style="display:flex; flex-direction: row;justify-content:space-between;align-items:center;">

                                <div style="padding:2px; 
                                            text-overflow: ellipsis; 
                                            overflow: hidden; 
                                            width: 130px; 
                                            white-space: nowrap;">
                                    {{ showImgName(image.path) }}
                                </div>

                                <!-- delete image button here  -->
                                <button style="background-color: red;
                                                padding:2px;
                                                border: none;" @click="deleteImage(image.img_id)">Delete</button>
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
            owner: 0,
            isLoading: true,
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
            this.isLoading=true
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
                    this.isLoading=false
                    alert('image upload response >' + response.data['status'])
                    location.reload();
                }
            ).catch(err =>{
                this.isLoading=false
                alert(err)
            })
        },

        deleteImage(img_id) {
            if (confirm("Are you sure to delete this image ?")) {
                axios.defaults.headers.delete['jwt'] = this.cookies.get('jwt');
                axios.delete(URL_GET_IMG + "/" + img_id)
                    .then(async res => {
                        alert(res.data['status']);
                        location.reload();
                    })
            }
        },


        editImgName() {
            let text;
            let person = prompt("Please enter your name:", "Harry Potter");
            if (person == null || person == "") {
                text = "User cancelled the prompt.";
            } else {
                text = "Hello " + person + "! How are you today?";
            }
            document.getElementById("demo").innerHTML = text;
        },

        showImgName(path) {
            let temp = path.split("/");
            return temp[5]
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
                                this.isLoading=false
                                this.images = res.data
                            })
                    }


                })
                .catch(err => console.log(err))


        }
    }
};
</script>
