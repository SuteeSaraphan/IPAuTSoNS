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
                    Image processing application
                </div>
            </header>


            <main>
                <div style="display: flex;flex-direction: row;">
                    <div class="loading" v-if="this.isLoading">Loading&#8230;</div>
                    <input type="checkbox" name="" id="sidebar-toggle">
                    <!----------------------------------------------------- filter bar ----------------------------------------------------->
                    <div style="width : 18%;
                          padding-right: 10px;
                          height: 800px;
                          background-color: #383C4A;
                          overflow-y: scroll;">

                        <input type="text" v-model="search" placeholder="Search" />
                        <div class="sidebar-main">
                            <div class="sidebar-menu">

                                <div class="menu-head">
                                    <span>Basic filter</span>
                                </div>
                                <ul>
                                    <li v-for=" i in this.filterNoneCpu" v-bind:key="i"
                                        style="background-color: #4B5162;padding: 10px;" @click="changeFilter()">
                                        <a>
                                            <span class="ri-function-line"></span>
                                            {{ i }}
                                        </a>
                                    </li>

                                </ul>
                                <div class="menu-head">
                                    <span>Advance Filter</span>
                                </div>
                                <ul>
                                    <li v-for=" i in this.filterOnCpu" v-bind:key="i"
                                        style="background-color: #4B5162;padding: 10px;" @click="changeFilter()">
                                        <a>
                                            <span class="ri-function-line"></span>
                                            {{ i }}
                                        </a>
                                    </li>

                                </ul>

                            </div>
                        </div>
                    </div>
                    <!----------------------------------------------------- end of filter bar ----------------------------------------------------->


                    <!-- image show -->
                    <div style="
                  padding-left: 15px;
                  padding-right: 20px;
                  padding-top: 15px;
                  display: flex;
                  flex-direction: column;
                  background-color: #4B5162;">
                        <h2>Drive >
                            <a style="align-self: center;width: 350px;">
                                <select id="folder_sel" style="color:#000 ;" @change="goToFolder">
                                    <option style="color:#000 ;" selected> --- Seleteced folder --- </option>
                                    <option v-for="folder in this.folders" :key="folder.folder_id" style="color:#000 ;">
                                        {{ folder.folder_name }}
                                    </option>
                
                                </select>
                            </a>
                        </h2>
                        <div
                            style="display: flex;flex-direction: row;  width: 1300px; padding:10px; overflow-x: scroll;">

                            <div @click="changePhoto(1)">
                                <img src="../img/for_demo/DSC01507.jpg" width="175" style="padding:10px;">
                            </div>
                            

                        </div>

                        <div style="
                  display: flex;
                  flex-direction: column;
                  justify-content: space-between;
                  align-items: center;
                  padding:20px;">
                            <img :src="this.imgShowSrc" width="700">

                        </div>

                        <div style="
                      display: flex;
                      flex-direction: row;
                      justify-content: flex-end;
                      padding:20px;">
                            <button type="button" @click="exportImg" style="
                              font-weight: bold;

                              color: #000;
                              padding: 10px;">
                                Export
                            </button>
                        </div>







                    </div>
                    <!-- image show -->
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
const URL_IMG_FOLDER = 'http://127.0.0.1:8000/api/folder_img';
//const URL_IMG_UPLOAD = 'http://127.0.0.1:8000/api/upload_image';
const URL_GET_IMG = 'http://127.0.0.1:8000/api/image';




export default {


    name: "Img_appView",
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
            folders : [],
            images :[],

        }
    },
    methods: {


        goToFolder() {
            for(let i in this.folders){
                if(this.folders[i].folder_name == document.getElementById("folder_sel").value){
                    console.log('founded')
                    
                    break;
                }else{
                    console.log('not found')
                }
            }


        },
        
        changeFilter() {
            this.imgShowSrc = require('@/img/for_demo/DSC01577-pixie-watermark.png')


        },

        changePhoto(img_id) {
            if (img_id == 1) {
                this.imgShowSrc = require('@/img/for_demo/DSC01507.jpg')
            } if (img_id == 2) {
                this.imgShowSrc = require('@/img/for_demo/DSC01535.jpg')
            } if (img_id == 3) {
                this.imgShowSrc = require('@/img/for_demo/DSC01540.jpg')
            } if (img_id == 4) {
                this.imgShowSrc = require('@/img/for_demo/DSC01550.jpg')
            } if (img_id == 5) {
                this.imgShowSrc = require('@/img/for_demo/DSC01574.jpg')
            } if (img_id == 6) {
                this.imgShowSrc = require('@/img/for_demo/DSC01577.jpg')
            } if (img_id == 7) {
                this.imgShowSrc = require('@/img/for_demo/DSC01583.jpg')
            } if (img_id == 8) {
                this.imgShowSrc = require('@/img/for_demo/DSC01608.jpg')
            }

        },

        exportImg() {
            router.push('/demoexport')
        },

        getImageOnPage(page) {
            // get image data from database
            this.page_sel = page;
            console.log(this.page_sel)
            axios.get(URL_GET_IMG + "/" + page + "/" + this.$route.params.folder_id)
                .then(res => {
                    console.log(res.data)
                    this.isLoading = false
                    this.images = res.data
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
        else{
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
