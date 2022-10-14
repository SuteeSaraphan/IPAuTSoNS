<template>
    <div>
        <SlideBar></SlideBar>
        <div class="main-home">
            <h1>Drive page</h1>
            <h1>v-model</h1>
            <form style="padding:5px;">
                <input type="file" accept="image/*" @change="uploadImage($event)" id="file-input" multiple="multiple">
                <hr>
                <label>Folder : </label>
                <input type="text" id="folder">
                <button type="button" @click="onUploadFile" style="color:black">Upload</button>


            </form>
            <!-- <form>
                <select id="img_folder">
                    <option value="volvo">Volvo</option>
                    <option value="saab">Saab</option>
                    <option value="vw">VW</option>
                    <option value="audi" selected>Audi</option>
                </select>
            </form> -->


            <div>
                <form style="padding:5px;">
                    <label>Add new folder : </label>
                    <input type="text" id="new_folder">
                    <button type="button" @click="addNewFolder" style="color:black">Add new folder</button>


                </form>
            </div>



            <div>
                <ul>
                    <li v-for="file in files" v-bind:key="file.id">
                        {{file}}
                    </li>
                </ul>
            </div>



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
                    alert('image upload response >', response.data.status)
                    location.reload();
                }
            )
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
                        "is_hidden": "false"
                    }
                ).then(async response => {
                    response.data
                    alert('Regis complete')
                    router.push('login')
                }).catch(async error => {
                    alert(error.response.data.email)
                    router.push('register')
                })
            }

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
                .then(res => console.log(res))
                .catch(err => console.log(err))

        }
    }
};
</script>