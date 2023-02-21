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
                    Market
                </div>
            </header>

            <main>
                <div class="page-header">
                    <div>
                        <h1>Marketplace</h1>
                        <small>ตลาดซื้อ-ขาย</small>
                    </div>

                    <div class="header-actions">
						<button>
							<span class="las la-plus"></span>
							Add product to sell
						</button>
					</div>

                </div>


                <!-- show all products here -->
                <div class="cards">


                    <!-- show each product info here -->
                    <div class="card-single">
                        <div class="card-flex">
                            <div class="card-info">
                                <div class="card-head">
                                    <span style="color: #000;">Seller - </span>
                                    <small style="color: #000;">Peachi_27</small>
                                </div>
                                <img src="https://live.staticflickr.com/65535/52639909358_84b98cc68f_o_d.jpg">
                                <h2 style="color: #000;">Yha tub sean gun</h2>
                                <small style="color: #000;">object detection</small>
                            </div>
                        </div>
                    </div>
                    <!-- end of show each product info here -->


                    <!-- show each product info here -->
                    <div class="card-single">
                        <div class="card-flex">
                            <div class="card-info">
                                <div class="card-head">
                                    <span style="color: #000;">Seller - </span>
                                    <small style="color: #000;">Peachi_27</small>
                                </div>
                                <img src="https://live.staticflickr.com/65535/52282498076_acc417f003_o_d.jpg">
                                <h2 style="color: #000;">Yha tub sean gun</h2>
                                <small style="color: #000;">object detection</small>
                            </div>
                        </div>
                    </div>
                    <!-- end of show each product info here -->

                    <!-- show each product info here -->
                    <div class="card-single">
                        <div class="card-flex">
                            <div class="card-info">
                                <div class="card-head">
                                    <span style="color: #000;">Seller - </span>
                                    <small style="color: #000;">Peachi_27</small>
                                </div>
                                <img src="https://live.staticflickr.com/65535/52282495158_e31d45500c_o_d.jpg" style="">
                                <h2 style="color: #000;">Yha tub sean gun</h2>
                                <small style="color: #000;">object detection</small>
                            </div>
                        </div>
                    </div>
                    <!-- end of show each product info here -->



                    <div class="card-single">
                        <div class="card-flex">
                            <div class="card-info">
                                <div class="card-head">
                                    <span style="color: #000;">Coming Soon</span>
                                    <small style="color: #000;">Coming Soon</small>
                                </div>
                                <h2 style="color: #000;">Coming Soon</h2>
                                <small style="color: #000;">Coming Soon</small>
                            </div>
                        </div>
                    </div>
                    <div class="card-single">
                        <div class="card-flex">
                            <div class="card-info">
                                <div class="card-head">
                                    <span style="color: #000;">Coming Soon</span>
                                    <small style="color: #000;">Coming Soon</small>
                                </div>
                                <h2 style="color: #000;">Coming Soon</h2>
                                <small style="color: #000;">Coming Soon</small>
                            </div>
                        </div>
                    </div>
                    <div class="card-single">
                        <div class="card-flex">
                            <div class="card-info">
                                <div class="card-head">
                                    <span style="color: #000;">Coming Soon</span>
                                    <small style="color: #000;">Coming Soon</small>
                                </div>
                                <h2 style="color: #000;">Coming Soon</h2>
                                <small style="color: #000;">Coming Soon</small>
                            </div>
                        </div>
                    </div>
                    <div class="card-single">
                        <div class="card-flex">
                            <div class="card-info">
                                <div class="card-head">
                                    <span style="color: #000;">Coming Soon</span>
                                    <small style="color: #000;">Coming Soon</small>
                                </div>
                                <h2 style="color: #000;">Coming Soon</h2>
                                <small style="color: #000;">Coming Soon</small>
                            </div>
                        </div>
                    </div>



                </div>
            </main>
        </div>
        <label for="sidebar-toggle" class="body-label"></label>
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




    name: "MarketView",
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



        changeImg(img_id) {
            this.imgShowSrc = null
            axios.defaults.headers.get['jwt'] = this.cookies.get('jwt');
            axios.get(URL_GET_IMG + "/once/" + img_id)
                .then(res => {
                    this.imgShowSrc = res.data[0]
                }).catch(error => {
                    console.log(error)
                    alert("Something went wrong try again")

                }
                )
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

        },

        filterAdjusting() {
            this.filter_value = document.getElementById("myRange").value;
            console.log(this.filter)
            console.log(this.filter_value)
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
