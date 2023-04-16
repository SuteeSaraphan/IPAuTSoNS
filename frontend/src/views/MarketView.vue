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
                <div class="loading" v-if="this.isLoading">Loading&#8230;</div>
                <div class="page-header">
                    <div>
                        <h1>Marketplace</h1>
                        <small>ตลาดซื้อ-ขาย</small>
                    </div>

                    <div class="header-actions">
                        <button @click="goAddProduct">
                            <span class="las la-plus"></span>
                            Add product to sell
                        </button>
                    </div>

                </div>

                <!-- filter history here  -->
                <div class="sort-btn" style="padding:5px;">
                    <div>
                        <button type="button" @click="goSort('1')">sort by newest </button>
                        <button type="button" @click="goSort('2')">sort by oldest</button>
                        <input type="date" id="search" @change="goSearch">
                    </div>
                    <div>
                        Type :
                        <select id="typeSel" style="color:#000 ; width: 15rem;" @change="selType">
                            <option style="color:#000 ;" v-if="this.$route.params.type != 'All'"> All </option>
                            <option style="color:#000 ;" v-if="this.$route.params.type == 'All'" selected> All </option>
                            <option style="color:#000 ;" v-if="this.$route.params.type != 'Object detection'"> Object detection </option>
                            <option style="color:#000 ;" v-if="this.$route.params.type == 'Object detection'" selected> Object detection </option>
                            <option style="color:#000 ;" v-if="this.$route.params.type != 'Image enhancer'"> Image enhancer </option>
                            <option style="color:#000 ;" v-if="this.$route.params.type == 'Image enhancer'" selected> Image enhancer </option>
                        </select>
                
                        Model :
                        <select id="modelSel" style="color:#000 ; width: 15rem;" @change="selModel">
                            <option style="color:#000 ;" v-if="this.$route.params.model != 'All'"> All </option>
                            <option style="color:#000 ;" v-if="this.$route.params.model == 'All'" selected> All </option>
                            <option style="color:#000 ;" v-if="this.$route.params.model != 'YOLOv5'"> YOLOv5 </option>
                            <option style="color:#000 ;" v-if="this.$route.params.model == 'YOLOv5'" selected> YOLOv5 </option>
                            <option style="color:#000 ;" v-if="this.$route.params.model != 'GANs'"> GANs </option>
                            <option style="color:#000 ;" v-if="this.$route.params.model == 'GANs'" selected> GANs </option>
                        </select>
                    </div>
                </div>




                <!-- show all products here -->
                <div class="cards">
                    <!-- show each product info here -->
                    <div class="card-single" v-for="product in this.productList" v-bind:key="product.product_id"
                        @click="goProduct(product.product_id)">
                        <div class="card-flex">
                            <div class="card-info">
                                <div class="card-head">
                                    <span style="color: #000;">Seller - </span>
                                    <small style="color: #000;">{{ product.seller }}</small>
                                </div>
                                <div class="card-img">
                                    <img :src="`data:image/jpeg;base64,${product.product_img}`"
                                        alt="{{ product.product_id }}">
                                </div>
                                <h2 style="color: #000;">{{ product.product_name }}</h2>
                                <small style="color: #000;">{{ product.product_type }}</small>
                            </div>
                        </div>
                    </div>
                    <!-- end of show each product info here -->





                </div>
            </main>
        </div>
        <label for="sidebar-toggle" class="body-label"></label>
    </div>
</template>
<style>
.sort-btn{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: left;

}
@media (max-width: 800px) {
    .sort-btn{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: left;

}
    
}
.card-single {
    border-radius: 15px;
    background-color: white;
}

.card-flex {
    width: 100%;
    padding-left: 5%;
    padding-right: 5%
}

.card-head {
    text-align: right;
    width: 100%;
}

.card-img {
    display: block;
    justify-content: center;
    padding: 2.5%;
}

.card-img img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: auto;
    max-height: 12rem;
    max-width: 15rem;
}
</style>

<script>
import SlideBar from '@/components/SlideBar'
import router from '@/router';
import axios from 'axios';





export default {




    name: "MarketView",
    setup() {



    },
    data() {
        return {
            isLoading: true,
            productList: []


        }
    },
    methods: {
        goAddProduct() {
            router.push('/add_product')
        },

        goProduct(product_id) {
            //console.log("enter folder :"+folder_id)
            let path = "/product/" + product_id
            window.location.href = path
        },
        //---/market/:type/:model/:sort---
        goSort(sort) {
            if (sort == "1") {
                let path = "/market/"+this.$route.params.type+"/"+this.$route.params.model+"/newest"
                window.location.href = path;
            } else if (sort == "2") {
                let path = "/market/"+this.$route.params.type+"/"+this.$route.params.model+"/oldest"
                window.location.href = path;
            }

        },

        goSearch() {
            let path = "/market/" + document.getElementById("search_by_date").value
            window.location.href = path;
        },

        selType(){
            let path = "/market/"+document.getElementById("typeSel").value+"/"+this.$route.params.model+"/"+this.$route.params.sort
            window.location.href = path;
        },

        selModel(){
            let path = "/market/"+this.$route.params.type+"/"+document.getElementById("modelSel").value+"/"+this.$route.params.sort
            window.location.href = path;
        },






    },
    components: {
        SlideBar,
        //VueSlideBar
    },
    async created() {
        console.log(this.$route.params.sort)
        console.log(this.$route.params.type)
        console.log(this.$route.params.model)
        
        //---/market/:type/:model/:sort---
        axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
        await axios.get('market/'+ this.$route.params.type+'_'+this.$route.params.model+'_'+this.$route.params.sort)
            .then(res => {
                console.log(res.data)
                this.isLoading = false;
                this.productList = res.data
            })
            .catch(err => {
                this.isLoading = false;
                console.log(err)
            })


    }
};
</script>
