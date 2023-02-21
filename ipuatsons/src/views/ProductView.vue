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
                    Product
                </div>
            </header>

            <main>
                <div class="page-header">
                    <div>
                        <h1>Product name</h1>
                        <small>ชื่อสินค้า - คนขาย &เ จ้าของ</small>
                    </div>

                </div>

                <div class="product-main">
                    <div class="product-img">
                        <img src="https://live.staticflickr.com/65535/52639909358_84b98cc68f_o_d.jpg">
                    </div>
                    <div class="product-detail">
                        <h1>Product name</h1>
                        <small>ชื่อสินค้า - คนขาย & เจ้าของ</small>
                        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla felis neque, auctor at interdum
                        sit amet, blandit nec diam. Donec ut elit mauris. Vestibulum ante ipsum primis in faucibus orci
                        luctus et ultrices posuere cubilia curae; Integer ac neque in eros vehicula lacinia ut sed
                        augue. Donec porttitor eget sem a hendrerit. Sed convallis gravida tellus, a tempor risus
                        commodo quis. Fusce mattis a sem id condimentum. Integer id neque a nulla venenatis ultrices non
                        rhoncus nisi. Nulla vel erat ornare, consectetur velit a, pellentesque nulla. Etiam vitae neque
                        placerat quam euismod finibus in vel eros. Morbi imperdiet laoreet erat ut maximus.</p>

                        <p>Nulla porta vehicula ante, ac imperdiet lorem mattis eu. Integer lacinia lorem a lectus
                        eleifend, in fringilla eros egestas. Donec accumsan quam eu dui dignissim, sit amet lacinia
                        neque feugiat. Phasellus pellentesque, sem in consequat euismod, odio ex pharetra augue, eget
                        pharetra dolor nunc egestas turpis. Nullam nec luctus massa, vel posuere purus. Curabitur
                        lobortis ullamcorper congue. Nulla convallis, nisi vel consectetur accumsan, orci lorem
                        efficitur erat, eget malesuada magna velit consectetur dui.</p>

                        <p>Nam ac placerat nibh, quis tincidunt ex. Orci varius natoque penatibus et magnis dis parturient
                        montes, nascetur ridiculus mus. Curabitur id lorem orci. Donec facilisis erat at pulvinar
                        mollis. Maecenas ut dolor quis sem pulvinar luctus. Mauris ultrices posuere lacus id hendrerit.
                        Mauris tincidunt pulvinar ante a tincidunt. Suspendisse nec consequat eros. Cras semper, ligula
                        eget hendrerit euismod, nisi dui tempor diam, vitae dapibus leo ligula in mi. Phasellus non
                        mauris vitae nisi lacinia fringilla. Vestibulum lectus urna, dignissim sed luctus a, feugiat a
                        tortor. Cras fermentum sem sollicitudin, aliquam massa vel, placerat dui. Nunc lacus lectus,
                        auctor quis mi ac, efficitur venenatis augue. Maecenas ornare leo a felis vulputate finibus.
                        Pellentesque elementum quis sem ut fringilla. Sed nec sodales nibh.</p>

                    </div>

                </div>

            </main>
        </div>
        <label for="sidebar-toggle" class="body-label"></label>
    </div>
</template>
<style>
.product-main {
    margin-top: 2%;
    display: flex;
    flex-direction: row;
    width: 100%;
    height: auto;
    background-color: rgb(42, 208, 0);

}

@media (max-width: 800px) {
    .product-main {
    flex-direction: column;
  }
}

.product-img {
    width: 100%;
    background-color: rgb(33, 84, 129);
}

.product-img img {
    height: auto;
    width: 100%;
    min-width: 12rem;
    overflow: scale-down;
    display: block;
    margin-left: auto;
    margin-right: auto;
    padding: 2%;
}

.product-detail{
    background-color: brown;
    width: 100%;
    padding: 2%;
}
</style>
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




    name: "ProductView",
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
