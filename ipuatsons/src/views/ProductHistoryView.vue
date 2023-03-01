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
//import VueSlideBar from 'vue-slide-bar';
const URL_IMG_FOLDER = 'http://127.0.0.1:8000/api/folder_img';
//const URL_IMG_UPLOAD = 'http://127.0.0.1:8000/api/upload_image';
const URL_GET_IMG = 'http://127.0.0.1:8000/api/image';



export default {




    name: "ProductHistoryView",
    setup() {
        const { cookies } = useCookies();
        return { cookies };



    },
    data() {
        return {
            filterNoneCpu: ['Black and White', 'ASCII'],
            filterOnCpu: ['Mosaic', 'PixelArt'],
            isLoading: true,
            imgBarWidth: '175',
            folders: [],
            images: [],
            imgShowSrc: null,
            filter: null,
            filter_value: 0

        }
    },
    methods: {
        goToAddProduct(){
            router.push('/addproduct')
        },


        goToFolder() {

            for (let i in this.folders) {
                if (this.folders[i].folder_name == document.getElementById("folder_sel").value) {
                    console.log('found')
                    axios.defaults.headers.get['jwt'] = this.cookies.get('jwt');
                    axios.get(URL_GET_IMG + "/all/" + this.folders[i].folder_id)
                        .then(res => {
                            this.images = []
                            this.isLoading = false
                            this.images = res.data

                        })

                    break;
                }
            }


        },
        goToProduct(product_id) {
            //console.log("enter folder :"+folder_id)
            let path = "/product/" + product_id
            window.location.href = path
        },
        changeFilter(filter_id) {
            this.filter = filter_id;
            document.getElementById("myRange").value = 80
            console.log(this.filter)
            console.log(this.filter_value)

        },





    }
    ,
    components: {
        SlideBar,
        //VueSlideBar
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
                    this.folders = res.data;
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
