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
                    <!----------------------------------------------------- product bar ----------------------------------------------------->
                    <div style="width : 20%;
                            padding-right: 10px;
                            height: 100%;
                            background-color: #383C4A;">

                        <div class="sidebar-main">
                            <div class="sidebar-menu">

                                <div class="menu-head">
                                    <span>Basic product</span>
                                </div>
                                <ul>
                                    <li v-for=" i in this.basicProduct" v-bind:key="i"
                                        style="background-color: #4B5162;padding: 10px;" @click="changeProduct(i)">
                                        <a>
                                            <span class="ri-function-line"></span>
                                            {{ i }}
                                        </a>
                                    </li>

                                </ul>
                                <div class="menu-head">
                                    <span>Marketplace product</span>
                                </div>
                                <ul>
                                    <li v-if="this.marketplaceProduct == null"
                                        style="background-color: #4B5162;padding: 10px;">
                                        <a> Don't have product from marketplace. </a>
                                    </li>
                                    <li v-for="i in this.marketplaceProduct" v-bind:key="i"
                                        style="background-color: #4B5162;padding: 10px;"
                                        @click="changeToMarketplaceProduct(i)">
                                        <a>
                                            <span class="ri-function-line"></span>
                                            {{ i['product_name'] }}
                                        </a>
                                    </li>

                                </ul>

                            </div>
                        </div>
                    </div>
                    <!----------------------------------------------------- end of product bar ----------------------------------------------------->


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
                        <div style="
                            display: flex;
                            flex-direction: row;
                            justify-items:flex-end;
                            align-items: center;
                            padding-bottom: 2%;">
                            <!-- bottom bar -->
                            <div v-if="this.product == 'PixelArt' || this.product == 'Mosaic'"
                                style=" width: 15%; text-align: center;">Adjust :</div>
                            <!-- choose how many pixel per bit -->
                            <div v-if="this.product == 'PixelArt'" style="width: 100%;
                                                                                        display: flex; 
                                                                                        flex-direction: column; 
                                                                                        justify-items:center; 
                                                                                        align-items: center;
                                                                                        padding-right: 1%;
                            
                                                    ">

                                <select id="parameter_value" style="color:#000 ;" @change="parameterAdjusting">
                                    <option v-for="i in 8" v-bind:key="i" style="color:#000 ;"> {{ (2 ** i) }} pixel/bit
                                    </option>
                                </select>
                            </div>
                            <!-- choose how many pixel per bit -->

                            <!-- choose what folder to process -->
                            <div v-if="this.product == 'Mosaic'" style="width: 100%;
                                                                                        display: flex; 
                                                                                        flex-direction: column; 
                                                                                        justify-items:center; 
                                                                                        align-items: center;
                                                                                        padding-right: 1%;
                            
                                                    ">

                                <select id="parameter_value" style="color:#000 ;" @change="parameterAdjusting">
                                    <option style="color:#000 ;" selected> --- Seleteced folder --- </option>
                                    <option v-for="folder in this.folders" :key="folder.folder_id" style="color:#000 ;">
                                        {{ folder.folder_name }}
                                    </option>
                                </select>
                            </div>
                            <!-- end of sliding bar -->

                            <!-- Export botton -->
                            <div v-if="this.imgShowSrc != null">
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
const URL_JOB_YOLO = 'yolo_export';
const URL_JOB_GAN = 'gan_export';
const URL_GET_PRODUCT = "product/img_app/";
const URL_GET_PRICE = "price_check/";


export default {




    name: "Img_appView",
    setup() {



    },
    data() {
        return {
            basicProduct: ['Black and White', 'ASCII', 'PixelArt', 'Mosaic'],
            marketplaceProduct: null,
            isLoading: true,
            folders: [],
            folder_id: null,
            images: [],
            imgShowSrc: null,
            product: null,
            adjValue: 30,
            addMarketProduct : false

        }
    },
    methods: {


        goToFolder() {
            this.isLoading = true
            for (let i in this.folders) {
                if (this.folders[i].folder_name == document.getElementById("folder_sel").value) {
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



        async changeImg(img_id) {
            this.isLoading = true
            this.imgShowSrc = null
            axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
            await axios.get(URL_GET_IMG + "/once/" + img_id)
                .then(res => {
                    this.isLoading = false
                    this.imgShowSrc = res.data[0]
                }).catch(error => {
                    this.isLoading = false
                    console.log(error)
                    alert("Something went wrong try again")

                }
                )
        },

        async exportImg() {
            if (this.imgShowSrc == null || this.product == null) {
                alert("Please choose image and product before export")
            } else {
                if(this.marketplaceProduct == []){
                    this.isLoading = true
                    let price = 0
                    let filter2PriceCheck = null
                    console.log('use normal product')
                    filter2PriceCheck = this.product
                    axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
                    await axios.get(URL_GET_PRICE + filter2PriceCheck + "/" + document.getElementById("folder_sel").value)
                        .then(res => {
                            console.log(res.data)
                            price = res.data['total_price']
                            if (confirm("Is job will cost " + price + " credit. Do you want to process export ?")) {
                                console.log(this.imgShowSrc)
                                axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                                console.log("product :" + this.product)
                                let exportData = null

                                console.log('use normal product')
                                exportData = {
                                    'img_path': this.imgShowSrc.path,
                                    'img_id': this.imgShowSrc.img_id,
                                    'img_selected': 'all',
                                    'product_id': this.product,
                                    'product_value': this.adjValue
                                }

                                axios.post(URL_JOB, exportData)
                                    .then(async res => {
                                        console.log(res)
                                        this.isLoading = false
                                        this.$store.commit('setCredit', res.data['credit_left']);
                                        alert("Job is on processing")
                                    })
                                    .catch(async err => {
                                        this.isLoading = false
                                        alert(err.response.data['status'] + ' because ' + err.response.data['cause'])
                                    })
                            } else {
                                this.isLoading = false
                            }
                        }).catch(err => {
                            console.log(err)
                            this.isLoading = false
                            alert("Can't get product price, try again")
                        })

                }
                else if (this.isInMarketProduct(this.product)) {
                    this.isLoading = true
                    let price = 0
                    let filter2PriceCheck = null
                    console.log('use normal product')
                    filter2PriceCheck = this.product['product_id']
                    console.log('filter2PriceCheck : '+filter2PriceCheck)
                    axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
                    await axios.get(URL_GET_PRICE + filter2PriceCheck + "/" + document.getElementById("folder_sel").value)
                        .then(res => {
                            console.log(res.data)
                            price = res.data['total_price']
                            if (confirm("Is job will cost " + price + " credit. Do you want to process export ?")) {
                                console.log(this.imgShowSrc)
                                axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                                console.log("product :" + this.product)
                                let exportData = null

                                console.log('use normal product')
                                exportData = {
                                    'img_path': this.imgShowSrc.path,
                                    'img_id': this.imgShowSrc.img_id,
                                    'img_selected': 'all',
                                    'product_id': this.product,
                                    'product_value': this.adjValue
                                }

                                axios.post(URL_JOB, exportData)
                                    .then(async res => {
                                        console.log(res)
                                        this.isLoading = false
                                        this.$store.commit('setCredit', res.data['credit_left']);
                                        alert("Job is on processing")
                                    })
                                    .catch(async err => {
                                        this.isLoading = false
                                        alert(err.response.data['status'] + ' because ' + err.response.data['cause'])
                                    })
                            } else {
                                this.isLoading = false
                            }
                        }).catch(err => {
                            console.log(err)
                            this.isLoading = false
                            alert("Can't get product price, try again")
                        })
                }

                else {
                    this.isLoading = true
                    let price = 0
                    let filter2PriceCheck = null
                    console.log('use Marketplace product')
                    filter2PriceCheck = this.product['product_id']

                    axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
                    await axios.get(URL_GET_PRICE + filter2PriceCheck + "/" + document.getElementById("folder_sel").value)
                        .then(res => {


//----------------------------------------YOLO--------------------------------------------------------                           
                            if (this.product['model'] == 'YOLOv5') {
                                price = res.data['total_price']
                                console.log('Yolo')
                                if (confirm("Is job will cost " + price + " credit. Do you want to process export ?")) {
                                    axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                                    let exportData = null
                                    exportData = {
                                        'img_path': this.imgShowSrc.path,
                                        'img_id': this.imgShowSrc.img_id,
                                        'img_selected': 'all',
                                        'product_id': this.product['product_id'],
                                        'product_value': this.adjValue
                                    }

                                    axios.post(URL_JOB_YOLO, exportData)
                                        .then(async res => {
                                            console.log(res)
                                            this.isLoading = false
                                            this.$store.commit('setCredit', res.data['credit_left']);
                                            alert("Job is on processing")
                                        })
                                        .catch(async err => {
                                            this.isLoading = false
                                            alert(err.response.data['status'] + ' because ' + err.response.data['cause'])
                                        })
                                } else {
                                    this.isLoading = false
                                }

                            }
//-----------------------------------------------GANS------------------------------------------------------------------                            
                            else if (this.product['model'] == 'GANs') {
                                price = res.data['total_price']
                                if (confirm("Is job will cost " + price + " credit. Do you want to process export ?")) {
                                    axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                                    let exportData = null
                                    exportData = {
                                        'img_path': this.imgShowSrc.path,
                                        'img_id': this.imgShowSrc.img_id,
                                        'img_selected': 'all',
                                        'product_id': this.product['product_id'],
                                        'product_value': this.adjValue
                                    }

                                    axios.post(URL_JOB_GAN, exportData)
                                        .then(async res => {
                                            console.log(res)
                                            this.isLoading = false
                                            this.$store.commit('setCredit', res.data['credit_left']);
                                            alert("Job is on processing")
                                        })
                                        .catch(async err => {
                                            this.isLoading = false
                                            alert(err.response.data['status'] + ' because ' + err.response.data['cause'])
                                        })
                                } else {
                                    this.isLoading = false
                                }
                            }


                        }).catch(err => {
                            console.log(err)
                            this.isLoading = false
                            alert("Can't get product price, try again")
                        })
                }
            }
        },



        async parameterAdjusting() {
            this.isLoading = true
            if (this.imgShowSrc != null) {
                this.isLoading = true

                console.log(document.getElementById("parameter_value").value)
                this.adjValue = document.getElementById("parameter_value").value;

                if (this.product == "Mosaic") {
                    for (let i in this.folders) {
                        if (this.folders[i].folder_name == document.getElementById("parameter_value").value) {
                            console.log(this.folders[i].path)
                            this.adjValue = this.folders[i].path
                        }
                    }
                }

                let img_preview = null
                let url_preview = null

                console.log('use normal product')
                url_preview = 'preview'
                img_preview = {
                    'img_id': this.imgShowSrc.img_id,
                    'product_id': this.product,
                    'product_value': this.adjValue

                }
                axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                await axios.post(url_preview, img_preview)
                    .then(res => {
                        this.imgShowSrc = null
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

        async changeProduct(product_id) {
            if (this.imgShowSrc != null) {
                this.isLoading = true
                this.product = product_id;
                //document.getElementById("paramter_value").value = 80
                let img_preview = null
                let url_preview = null
                if (this.product == "Mosaic") {
                    for (let i in this.folders) {
                        if (this.folders[i].folder_name == document.getElementById("folder_sel").value) {
                            this.adjValue = this.folders[i].path
                        }
                    }
                }


                url_preview = 'preview'
                img_preview = {
                    'img_id': this.imgShowSrc.img_id,
                    'product_id': this.product,
                    'product_value': this.adjValue

                }

                axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                await axios.post(url_preview, img_preview)
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

        async changeToMarketplaceProduct(product) {
            console.log(product)
            if (this.imgShowSrc != null) {
                this.isLoading = true
                let img_preview = null
                let url_preview = null
                this.product = product


                url_preview = 'preview_adv'
                img_preview = {
                    'img_id': this.imgShowSrc.img_id,
                    'product_id': product['product_id'],
                    'product_value': this.adjValue

                }

                axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                await axios.post(url_preview, img_preview)
                    .then(res => {
                        this.isLoading = false
                        this.imgShowSrc = res.data
                    })
                    .catch(err => {
                        this.isLoading = false
                        console.log(err)
                        alert(err.data)
                    })
            }
            else {
                alert('Please select image')
            }
        },

        isInMarketProduct(product_name){
            this.marketplaceProduct.forEach((item) =>{
                if(item['product_id']==product_name){
                    return true
                }
            })
            return false
        },





    }
    ,
    components: {
        SlideBar,
        //VueSlideBar
    },
    async created() {
        this.marketplaceProduct = this.$store.state.productUse
        axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
        await axios.get(URL_IMG_FOLDER)
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
            this.marketplaceProduct.forEach((item) =>{
                if(item['product_id']==this.$route.params.product_id){
                    this.addMarketProduct = true
                }
            })

            console.log(this.addMarketProduct)
            if(this.addMarketProduct == false){
                await axios.get(URL_GET_PRODUCT + this.$route.params.product_id)
                    .then(res => {
                        this.$store.commit('addProduct',res.data);
                        this.marketplaceProduct = this.$store.state.productUse
                    }).catch(err => {
                        console.log(err)
                        alert("Product loading fail, try again")
                    })
            }

        }




    }
};
</script>
