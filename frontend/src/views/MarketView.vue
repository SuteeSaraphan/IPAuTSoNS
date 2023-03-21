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
                    <button type="button" @click="goSort('1')">sort by newest </button>
                    <button type="button" @click="goSort('2')">sort by oldest</button>
                    <input type="date" id="search" @change="goSearch">
                </div>


                <!-- show all products here -->
                <div class="cards">
                    <!-- show each product info here -->
                    <div class="card-single" v-for="product in this.productList" v-bind:key="product.product_id" @click="goToProduct(1)" >
                        <div class="card-flex">
                            <div class="card-info">
                                <div class="card-head">
                                    <span style="color: #000;">Seller - </span>
                                    <small style="color: #000;">{{product.seller}}</small>
                                </div>
                                <div class="card-img">
                                    <img :src="`data:image/jpeg;base64,${product.product_img}`" alt="{{ product.product_id }}">
                                </div>
                                <h2 style="color: #000;">Yha tub sean gun</h2>
                                <small style="color: #000;">object detection</small>
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
.card-single {
    border-radius: 15px;
    background-color: white;
}

.card-flex {
    width: 100%;
    padding-left: 15%;
    padding-right: 15%
}

.card-head {
    text-align: right;
    width: 100%;
}

.card-img {
    display: flex;
    justify-content: center;
    margin-left: 20%;
    margin-right: 20%;
}

.card-img img {
    max-width: 12rem;
    background-color: aqua;
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
            productList : []


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

        goSort(type) {
            if (type == "1") {
                let path = "/history/" + "newest"
                window.location.href = path;
            } else if (type == "2") {
                let path = "/history/" + "oldest"
                window.location.href = path;
            }

        },

        goSearch() {
            let path = "/history/" + document.getElementById("search_by_date").value
            window.location.href = path;
        },





    }
    ,
    components: {
        SlideBar,
        //VueSlideBar
    },
    async created() {
        console.log(this.$route.params.keyword)
        axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
        await axios.get('product/all/lastest')
            .then(res => {
                console.log(res.data)
                this.isLoading = false;
                this.productList = res.data
            })
            .catch(err =>{
                this.isLoading = false;
                console.log(err)
            })


    }
};
</script>
