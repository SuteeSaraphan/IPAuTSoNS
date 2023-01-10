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
                        <h2>Drive > Congratulations_CEDT_27</h2>
                        <div
                            style="display: flex;flex-direction: row;  width: 1300px; padding:10px; overflow-x: scroll;">

                            <div @click="changePhoto(1)">
                                <img src="../img/for_demo/DSC01507.jpg" width="175" style="padding:10px;">
                            </div>
                            <div @click="changePhoto(2)">
                                <img src="../img/for_demo/DSC01535.jpg" width="175" style="padding:10px;">
                            </div>
                            <div @click="changePhoto(3)">
                                <img src="../img/for_demo/DSC01540.jpg" width="175" style="padding:10px;">
                            </div>
                            <div @click="changePhoto(4)">
                                <img src="../img/for_demo/DSC01550.jpg" width="175" style="padding:10px;">
                            </div>
                            <div @click="changePhoto(5)">
                                <img src="../img/for_demo/DSC01574.jpg" width="175" style="padding:10px;">
                            </div>
                            <div @click="changePhoto(6)">
                                <img src="../img/for_demo/DSC01577.jpg" width="175" style="padding:10px;">
                            </div>
                            <div @click="changePhoto(7)">
                                <img src="../img/for_demo/DSC01583.jpg" width="175" style="padding:10px;">
                            </div>
                            <div @click="changePhoto(8)">
                                <img src="../img/for_demo/DSC01608.jpg" width="175" style="padding:10px;">
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



export default {


    name: "DemoView",
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
            imgShowSrc: require('@/img/for_demo/DSC01507.jpg')

        }
    },
    methods: {
        waitFewSec() {
            this.isLoading = true
            console.log('wait few sec')
            setTimeout(() => this.isLoading = false, 2000);
        },

        changeFilter() {
            this.waitFewSec()
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
        }





    }
    ,
    components: {
        SlideBar
    },
    created() {
        this.waitFewSec()
        if (this.cookies.get('jwt') == null) {
            alert("You are not login yet , please login fisrt")
            router.push('/login')
        }

    }
};
</script>
