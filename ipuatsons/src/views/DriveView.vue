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

                
                <!--Add new folder image here  -->
                <div style="padding:5px;">
                    <button class="dropbtn" type="button" @click="addNewFolder" >Add new folder</button>
                </div>
                
                


                <!-- folder image list show here  -->
                <div style="background:#e7e5e6">
                    
                    <ul style="padding:5px;">
                        <div v-if="files < 1" 
                        style="text-align: center;
                            align-items: center;
                            color: #000;
                            background:#ccc;">!!! You do not have image folder !!!</div>

                        <li v-for="file in files" v-bind:key="file.id" style="margin-top: 5px;margin-bottom: 5px; ">

                            <div style="display : flex; 
                             flex-direction : row;
                             justify-content: space-between;
                             align-items : center;
                             padding-right: 15px;
                             background:#ccc;">

                                <div style="color:black;padding:10px; " @click="enterFolder(file.folder_id)">
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
            isLoading: true
        }
    },
    methods: {

        addNewFolder() {
            let newFolderName = prompt('Enter folder name');
            if (newFolderName.length == 0) {
                alert("Folder name is empty")
            } else {
                axios.post('folder_img',
                    {
                        'jwt': this.cookies.get('jwt'),
                        "folder_id": Math.random().toString(36).slice(2),
                        "folder_name": newFolderName
                    }
                ).then(async response => {
                    alert(response.data['status']);
                    location.reload();

                })
            }

        },


        enterFolder(folder_id) {
            //console.log("enter folder :"+folder_id)
            let path = "/img_folder/" + folder_id + "/1"
            window.location.href = path
        },


        deleteFolder(folder_id) {
            if (confirm("Are you sure to delete this folder ?")) {
                axios.defaults.headers.delete['jwt'] = this.cookies.get('jwt');
                axios.delete("folder_img/" + folder_id)
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
            const URL = 'folder_img';
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
