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
                    asd
                </div>
            </header>


            <main>
                <div class="loading" v-if="this.isLoading">Loading&#8230;</div>
                <h1>Drive page</h1>

                <!-- upload image here  -->
                <form style="padding:5px;">
                    <input type="file" accept="image/*" @change="uploadImage($event)" id="file-input"
                        multiple="multiple">
                    <hr>
                    <label>Folder : </label>
                    <button type="button" @click="onUploadFile" style="color:black">Upload</button>
                    <form>
                        <select id="folder">
                            <option v-for="file in files" v-bind:key="file.id" style="color:black">{{
                                file.folder_name
                            }}
                            </option>
                        </select>
                    </form>
                </form>

                <!--Add new folder image here  -->
                <div>
                    <form style="padding:5px;">
                        <label>Add new folder : </label>
                        <input type="text" id="new_folder">
                        <button type="button" @click="addNewFolder" style="color:black">Add new folder</button>
                    </form>
                </div>


                <!-- folder image list show here  -->
                <div style="background:#e7e5e6">
                    <ul style="padding:5px;">
                        <li v-for="file in files" v-bind:key="file.id" style="margin-top: 5px;margin-bottom: 5px;">

                            <div style="display : flex; 
                             flex-direction : row;
                             justify-content: space-between;
                             align-items : center;">

                                <div style="color:black;padding:10px" @click="enterFolder(file.folder_id)">
                                    {{ file.folder_name }}</div>

                                <!-- dropUp list here  -->
                                <div class="dropup">
                                    <button class="dropbtn">Option</button>
                                    <div class="dropup-content">
                                        <a @click="deleteFolder(file.folder_id)">Delete</a>
                                        <a href="#">Edit name</a>
                                    </div>
                                </div>


                            </div>
                            <hr>
                        </li>

                    </ul>
                </div>


            </main>
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
            files: [],
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
            this.isLoading = true
            if (this.selectedFile.length > 0) {
                const URL = 'http://127.0.0.1:8000/api/upload_image';
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
                        this.isLoading = false
                        alert('image upload response >' + response.data['status'])
                        location.reload();
                    }
                ).catch(err => {
                    this.isLoading = false
                    alert(err)
                }

                )
            } else {
                this.isLoading = false
                alert('Please selected file before upload')
            }

        },


        addNewFolder() {
            if (document.getElementById("new_folder").value.length == 0) {
                alert("Folder name is empty")
            } else {
                axios.post('http://127.0.0.1:8000/api/folder_img',
                    {
                        'jwt': this.cookies.get('jwt'),
                        "folder_id": Math.random().toString(36).slice(2),
                        "folder_name": document.getElementById("new_folder").value,
                    }
                ).then(async response => {
                    alert(response.data['status']);
                    location.reload();

                })
            }

        },


        enterFolder(folder_id) {
            console.log(folder_id)
            let path = "/img_folder/" + folder_id + "/1"
            router.push({ path })
        },


        deleteFolder(folder_id) {
            if (confirm("Are you sure to delete this folder ?")) {
                axios.defaults.headers.delete['jwt'] = this.cookies.get('jwt');
                axios.delete("http://127.0.0.1:8000/api/folder_img/" + folder_id)
                    .then(async res => {
                        alert(res.data['status']);
                        location.reload();
                    })
            }
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
            const URL = 'http://127.0.0.1:8000/api/folder_img';
            axios.get(URL)
                .then(res => {
                    this.files = res.data;
                    this.isLoading = false
                })
                .catch(err => {
                    this.isLoading = false
                    alert(err.data)
                })

        }
    }
};
</script>
