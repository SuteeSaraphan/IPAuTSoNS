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
                    <button class="dropbtn" type="button" @click="addNewFolder"><span class="las la-folder-plus"></span>Add new folder</button>
                </div>




                <!-- folder image list show here  -->
                <div style="background:#e7e5e6">

                    <ul style="padding:5px;">
                        <div v-if="files < 1" style="text-align: center;
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
                                

                                <div style="color:black;padding:10px; " @click="enterFolder(file.folder_id)"><span class="las la-folder"></span>
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
//import router from '@/router';
import axios from 'axios';

export default {

    name: "DriveView",
    setup() {

    },
    data() {
        return {
            selectedFile: [],
            files: [],
            isLoading: true
        }
    },
    methods: {

        async addNewFolder() {
            let newFolderName = prompt('Enter folder name');
            if (newFolderName.length == 0) {
                alert("Folder name is empty")
            } else {
                axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                await axios.post('folder_img',
                    {
                        'jwt': this.$store.state.jwt,
                        "folder_name": newFolderName
                    }
                ).then(async response => {
                    alert(response.data['status']);
                    location.reload();

                }).catch(err =>{
                    alert(err.response.data['status']);
                    //location.reload();
                })
            }

        },


        enterFolder(folder_id) {
            //console.log("enter folder :"+folder_id)
            let path = "/img_folder/" + folder_id + "/1"
            window.location.href = path
        },


        async deleteFolder(folder_id) {
            if (confirm("Are you sure to delete this folder ?")) {
                axios.defaults.headers.delete['jwt'] = this.$store.state.jwt;
                await axios.delete("folder_img/" + folder_id)
                    .then(async res => {
                        alert(res.data['status']);
                        location.reload();
                    }).catch(error =>{
                        console.log(error)
                        alert("delete folder fail");
                    })
            }
        }



    }
    ,
    components: {
        SlideBar
    },
    async created() {
        axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
        const URL = 'folder_img';
        await axios.get(URL)
            .then(res => {
                this.files = res.data;
                this.isLoading = false
            })
            .catch(err => {
                this.isLoading = false
                alert(err.data)
            })


    }
};
</script>
