<template>
    <div>
        <SlideBar></SlideBar>
        <div class="main-content">
            <header>
                <div class="menu-toggle">
                    <label for="sidebar-toggle">
                        <span style="color:#000 ;" class="las la-bars"></span>
                    </label>
                </div>
                <span class="bars"></span>

                <div style="color:#000 ;">
                    Drive
                </div>
            </header>
            <main>
                <div class="loading" v-if="this.isLoading">Loading&#8230;</div>

                <!-- show full image here  -->
                <div class="full-img" v-if="this.fullShow">

                    <button style="border: none; width: 3rem; align-self: flex-end;" @click="this.fullShow = false">
                        <span style="font-size: 1.5rem;" class=" las la-times-circle"></span>
                    </button>


                    <img style='
                                                    height:95%; 
                                                    object-fit: scale-down;
                                                    border: 1px;
                                                    margin-bottom: 2%;
                                                    image-rendering: auto;'
                        :src="`data:image/jpeg;base64,${this.fullImage.img_data}`" alt="{{ this.fullImage.img_id }}">

                </div>

                <!-- loading -->
                <div v-if="this.isUploading">
                        <div class="uploading">
                            <radial-progress-bar :diameter="500" :completed-steps="completedSteps" :total-steps="totalSteps"
                                :startColor="this.barColor" :stopColor="this.barColor" style="
                                    align-items: center;
                                    justify-content:center;
                                ">
                                <h2>On Process</h2>
                                <h1>Completed : {{ completedSteps }} %</h1>
                            </radial-progress-bar>
                        </div>
                    </div>
                    <!-- loading -->



                <h1>Image Folder page</h1>
                <h2 v-if="this.folder.length == 0">Folder name : Untitle</h2>
                <h2 v-if="this.folder.length != 0">Folder name : {{ this.folder.folder_name }}</h2>

                <!-- upload image here  -->
                <form style="padding:5px;">
                    <input type="file" accept="image/*" @change="uploadImage($event)" id="file-input" multiple="multiple">
                    <button type="button" @click="onUploadFile" style="padding-right:0.5%;padding-left:0.5%;background-color:#5294e2;"><span class="las la-cloud-upload-alt"></span> Upload</button>
                </form>

                <hr>

                <!-- show image array here  -->
                <div class="cards">
                    <div class="card-single" v-for="image in this.images" v-bind:key="image.img_id" style="background-color:#4b5162;
                                                border-radius: 15px;">
                        <div style="display: block; justify-content: center; padding: 2.5%; ">
                            <img :src="`data:image/jpeg;base64,${image.img_data}`" alt="{{ image.img_id }}"
                                @click="fullImageView(image.img_id)" style="
                                        display: block;
                                        margin-left: auto;
                                        margin-right: auto;
                                        width: auto;
                                        max-height: 12rem;
                                        max-width: 15rem;
                                        ">
                        </div>
                        <div class="container" style="width:90%;
                                                margin-left: 3%; 
                                                margin-right: 3%; 
                                                display:flex; 
                                                flex-direction:row; 
                                                justify-content:space-between; 
                                                align-items:center;
                                                ">
                            <div style="padding:2px; 
                                            overflow: hidden;
                                            text-overflow: ellipsis;
                                            white-space: nowrap;
                                            ">

                                {{ showImgName(image.path) }}
                            </div>

                            <!-- delete image button here  -->

                            <div>
                                <button style="background-color: red;
                                                                                padding:2px;
                                                                                border: none;"
                                    @click="deleteImage(image.img_id)">
                                    <span style="font-size: 1.5rem;" class="las la-trash"></span></button>
                            </div>
                        </div>


                    </div>
                </div>


                <!-- page select here  -->
                <div style="
                                                    display: flex;
                                                    margin: auto;
                                                    padding-top: 1%;
                                                    width: 35%;
                                                    height: 50px;
                                                    justify-content: space-between;
                                                    text-align: center;
                                                    ">
                    <a style="align-self: center;width: 350px;">Page :
                        <select id="pageSel" style="color:#000 ;" @change="goToPage">
                            <option v-for="i in this.pages" :key="i" style="color:#000 ;">
                                {{ i }}
                            </option>
                            <option selected style="color:#000 ;" hidden> {{ this.pageSel }}</option>
                        </select>
                    </a>
                </div>
            </main>
        </div>
    </div>
</template>

<style></style>

<script>
import SlideBar from '@/components/SlideBar'
import router from '@/router';
import axios from 'axios';
import RadialProgressBar from 'vue-radial-progress';
const URL_IMG_FOLDER = 'folder_img';
const URL_IMG = 'image';



export default {
    name: "ImgFolderView",
    setup() {

    },
    data() {
        return {
            selectedFile: [],
            token_url: "",
            files: [],
            images: [],
            fullImage: null,
            owner: false,
            isLoading: true,
            fullShow: false,
            pages: 1,
            pageSel: 0,
            folder: null,
            upload_progress: 0,
            isUploading: false,
            completedSteps :0,
            totalSteps:0,
            barColor: "#5294e2",


        }
    },
    methods: {

        // choose image to upload
        uploadImage(event) {
            this.selectedFile = []
            for (let i = 0; i < event.target.files.length; i++) {
                this.selectedFile.push(event.target.files[i])
            }



        },
        //upload image to server
        async onUploadFile() {
            this.upload_progress = 0
            if (this.selectedFile.length > 0) {
                this.isUploading = true
                //console.log(this.selectedFile[0])
                this.totalSteps = this.selectedFile.length;
                let data = new FormData();
                for (let i = 0; i < this.selectedFile.length; i++) {
                    data = new FormData();
                    data.append('jwt', this.$store.state.jwt);
                    data.append('folder', this.folder.folder_name);
                    data.append('img_file', this.selectedFile[i]);
                    await this.performUpload(data)
                }
                this.isUploading = false
                alert('Upload all done')
            } else {
                alert('please select file before upload')
            }

        },
        async performUpload(data) {
            let config = {
                header: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            await axios.post(
                URL_IMG,
                data,
                config
            ).then(
                async (response) => {
                    this.completedSteps += 1
                    this.upload_progress += 1
                    console.log(response.data['status'])
                    if (this.upload_progress == this.selectedFile.length) {
                        this.isUploading = false
                        window.location.reload()
                    }
                }
            ).catch(err => {
                alert(err)
            })
        },

        //view full resolution image
        fullImageView(img_id) {
            this.fullImage = null
            this.fullShow = true
            axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
            axios.get(URL_IMG + "/once/" + img_id)
                .then(res => {
                    this.fullImage = res.data[0]
                    console.log(this.fullImage)
                })
        },

        //delete image 
        deleteImage(img_id) {
            if (confirm("Are you sure to delete this image ?")) {
                axios.defaults.headers.delete['jwt'] = this.$store.state.jwt;
                axios.delete(URL_IMG + "/" + img_id)
                    .then(async res => {
                        alert(res.data['status']);
                        location.reload();
                    })
            }
        },

        // edit image name
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

        // for show image name by cut it out from path
        showImgName(path) {
            let temp = path.split("/");
            return temp.pop()
        },

        goToPage() {
            console.log(document.getElementById("pageSel").value)
            let path = "/img_folder/" + this.$route.params.folder_id + "/" + document.getElementById("pageSel").value
            window.location.href = path

        },

        getImageOnPage(page) {
            // get image data from data base
            this.pageSel = page;
            //console.log(this.pageSel)
            axios.get(URL_IMG + "/" + page + "/" + this.$route.params.folder_id)
                .then(res => {
                    this.isLoading = false
                    this.images = res.data
                })

        }




    }
    ,
    components: {
        SlideBar,
        RadialProgressBar
    },
    created() {
        axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
        //check rights in this folder
        axios.get(URL_IMG_FOLDER)
            .then(res => {
                for (let i in res.data) {
                    if (this.$route.params.folder_id == res.data[i].folder_id) {
                        this.owner = true
                        this.folder = res.data[i]
                        break;
                    }
                }

                if (this.owner == false) {
                    alert("You can not access this folder");
                    router.push('/drive')
                } else {
                    // count image in from data base
                    axios.get(URL_IMG + "/count/" + this.$route.params.folder_id)
                        .then(res => {
                            //console.log('image : ' + res.data)
                            this.pages = res.data / 24
                            this.pages = Math.ceil(this.pages)
                            //console.log('pages count : ' + this.pages)
                        })
                    this.getImageOnPage(this.$route.params.page);
                }


            })
            .catch(err => console.log(err))



    }
};
</script>
