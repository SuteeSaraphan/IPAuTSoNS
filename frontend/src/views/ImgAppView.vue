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
                    <div style="width : 20%;
                                                              padding-right: 10px;
                                                              height: 100%;
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
                                        style="background-color: #4B5162;padding: 10px;" @click="changeFilter(i)">
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
                                        style="background-color: #4B5162;padding: 10px;" @click="changeFilter(i)">
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


                    <!-- image list show -->
                    <div style="
                                                      padding-left: 15px;
                                                      padding-right: 20px;
                                                      padding-top: 15px;
                                                      width: 80%;
                                                      height: 50%;
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
                        <div style="display: flex;
                                                                flex-direction: row; 
                                                                width: 100%;
                            
                                                                padding:10px;
                                                                overflow-x: scroll;
                                                                align-items: center;
                                                                ">

                            <div v-for="image in this.images" :key="image.img_id">
                                <img :src="`data:image/jpeg;base64,${image.img_data}`" style="
                                                                    padding: 10px;
                                                                    max-width: 175px;
                                                                    max-height: 100px;
                                                                    " @click="changeImg(image.img_id)">
                            </div>


                        </div>
                        <!-- image full show -->

                        <div v-if="this.imgShowSrc != null" style="
                                                                display: flex;
                                                                flex-direction: column;
                                                                justify-content: space-between;
                                                                align-items: center;
                                                                padding:20px;">
                            <img :src="`data:image/jpeg;base64,${this.imgShowSrc.img_data}`" height="350">

                        </div>
                        <div v-if="this.imgShowSrc != null"
                            style="display: flex; flex-direction: row; justify-items:flex-start; align-items: center;">

                            <div style=" width: 15%; text-align: center;">Filter :</div>
                            <!-- sliding bar -->
                            <div class="slidecontainer" style="width: 100%;
                                                                                        display: flex; 
                                                                                        flex-direction: column; 
                                                                                        justify-items:center; 
                                                                                        align-items: center;
                            
                                                    ">
                                <input type="range" min="1" max="100" value="80" class="slider" id="myRange"
                                    @change="filterAdjusting" style="width: 100%;">
                            </div>
                            <!-- end of sliding bar -->

                            <!-- Export botton -->
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
                            <!-- Export botton -->
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
//import router from '@/router';
import axios from 'axios';
//import VueSlideBar from 'vue-slide-bar';
const URL_IMG_FOLDER = 'folder_img';
const URL_GET_IMG = 'image';
const URL_JOB = 'make_docker_file';
const URL_GET_PRODUCT = "product/filter/"


export default {




    name: "Img_appView",
    setup() {



    },
    data() {
        return {
            filterNoneCpu: ['Black and White', 'ASCII', 'PixelArt'],
            filterOnCpu: ['Mosaic', 'Object-detection'],
            isLoading: true,
            imgBarWidth: '175',
            folders: [],
            images: [],
            imgShowSrc: null,
            filter: "none",
            filterValue: 80,
            importFilter: null

        }
    },
    methods: {


        goToFolder() {

            for (let i in this.folders) {
                if (this.folders[i].folder_name == document.getElementById("folder_sel").value) {
                    console.log('found')
                    axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
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



        changeImg(img_id) {
            this.imgShowSrc = null
            axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
            axios.get(URL_GET_IMG + "/once/" + img_id)
                .then(res => {
                    this.imgShowSrc = res.data[0]
                }).catch(error => {
                    console.log(error)
                    alert("Something went wrong try again")

                }
                )
        },

        async exportImg() {
            console.log(this.imgShowSrc)
            axios.defaults.headers.post['jwt'] = this.$store.state.jwt;

            let exportData = null
            if(this.importFilter != null){
                if (this.importFilter['product_name'] == this.filter) {
                    console.log('use import filter')
                    exportData = {
                        'img_path': this.imgShowSrc.path,
                        'img_id': this.imgShowSrc.img_id,
                        'filter_id': this.importFilter['product_id'],
                        'filter_value': this.filterValue
                    }
                } else {
                    console.log('use normal filter')
                    exportData = {
                        'img_path': this.imgShowSrc.path,
                        'img_id': this.imgShowSrc.img_id,
                        'img_selected': 'all',
                        'filter_id': this.filterValue
                    }
                }
            }else{
                    console.log('use normal filter')
                    exportData = {
                        'img_path': this.imgShowSrc.path,
                        'img_id': this.imgShowSrc.img_id,
                        'img_selected': 'all',
                        'filter_id': this.filterValue
                    }
                }
                
            await axios.post(URL_JOB, exportData)
                .then(async res => {
                    console.log(res)
                    alert("Job is on processing")
                })
                .catch(async err => {
                    alert(err.response.data['status'] +' because '+ err.response.data['cause'])
                })
        },

        getImageOnPage(page) {
            // get image data from database
            this.page_sel = page;
            console.log(this.page_sel)
            axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
            axios.get(URL_GET_IMG + "/" + page + "/" + this.$route.params.folder_id)
                .then(res => {
                    console.log(res.data)
                    this.isLoading = false
                    this.images = res.data[0]
                })

        },

        filterAdjusting() {
            if (this.imgShowSrc != null) {
                this.isLoading = true
                this.filterValue = document.getElementById("myRange").value;
                let img_preview = null
                let url_preview = null

                if(this.importFilter != null){
                    if (this.importFilter['product_name'] == this.filter) {
                        console.log('use import filter')
                        url_preview = 'preview_adv'
                        img_preview = {
                            'img_id': this.imgShowSrc.img_id,
                            'filter_id': this.importFilter['product_id'],
                            'filter_value': this.filterValue
                        }
                    } else {
                        console.log('use normal filter')
                        url_preview = 'preview'
                        img_preview = {
                            'img_id': this.imgShowSrc.img_id,
                            'filter_id': this.filter,
                            'filter_value': this.filterValue
                        }
                    }
                }else{
                    console.log('use normal filter')
                        url_preview = 'preview'
                        img_preview = {
                            'img_id': this.imgShowSrc.img_id,
                            'filter_id': this.filter,
                            'filter_value': this.filterValue
                        }
                }
                axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                axios.post(url_preview, img_preview)
                    .then(res => {
                        this.isLoading = false
                        this.imgShowSrc = res.data
                    })
                    .catch(err => {
                        this.isLoading = false
                        console.log(err)
                        alert('!!! Preview fail ,try again !!!')
                    })
            } else {
                alert('Please select image')
            }

        },

        changeFilter(filter_id) {
            if (this.imgShowSrc != null) {
                this.isLoading = true
                this.filter = filter_id;
                document.getElementById("myRange").value = 80
                let img_preview = null
                let url_preview = null

                if(this.importFilter != null){
                    if (this.importFilter['product_name'] == filter_id) {
                        console.log('use import filter')
                        url_preview = 'preview_adv'
                        img_preview = {
                            'img_id': this.imgShowSrc.img_id,
                            'filter_id': this.importFilter['product_id'],
                            'filter_value': this.filterValue
                        }
                    } else {
                        console.log('use normal filter')
                        url_preview = 'preview'
                        img_preview = {
                            'img_id': this.imgShowSrc.img_id,
                            'filter_id': this.filter,
                            'filter_value': this.filterValue
                        }
                    }
                }else{
                    console.log('use normal filter')
                        url_preview = 'preview'
                        img_preview = {
                            'img_id': this.imgShowSrc.img_id,
                            'filter_id': this.filter,
                            'filter_value': this.filterValue
                        }
                }
                console.log("call api preview at : " + url_preview)
                axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                axios.post(url_preview, img_preview)
                    .then(res => {
                        this.isLoading = false
                        this.imgShowSrc = res.data
                    })
                    .catch(err => {
                        this.isLoading = false
                        alert(err.data)
                    })
            }
            else {
                alert('Please select image')
            }

        },





    }
    ,
    components: {
        SlideBar,
        //VueSlideBar
    },
    created() {
        axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
        axios.get(URL_IMG_FOLDER)
            .then(res => {
                this.folders = res.data;
                this.isLoading = false
            })
            .catch(err => {
                this.isLoading = false
                console.log(err)
                alert(err.data)
            })


        if (this.$route.params.product_id != "0") {
            axios.get(URL_GET_PRODUCT + this.$route.params.product_id)
                .then(res => {
                    this.importFilter = res.data
                    console.log(this.importFilter)
                    this.filterOnCpu.push(res.data['product_name'])
                }).catch(err => {
                    console.log(err)
                    alert("Filter loading fail, try again")
                })
        }




    }
};
</script>
