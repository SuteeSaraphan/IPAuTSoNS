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
                        <button @click="goToAddProduct">
                            <span class="las la-plus"></span>
                            Add product to sell
                        </button>
                    </div>

                </div>


                <!-- show all products here -->
                <div class="cards">


                    <!-- show each product info here -->
                    <div class="card-single" @click="goToProduct(1)">
                        <div class="card-flex">
                            <div class="card-info">
                                <div class="card-head">
                                    <span style="color: #000;">Seller - </span>
                                    <small style="color: #000;">Peachi_27</small>
                                </div>
                                <div class="card-img">
                                    <img src="https://live.staticflickr.com/65535/52639909358_84b98cc68f_o_d.jpg">
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
//import axios from 'axios';






export default {




    name: "MarketView",
    setup() {



    },
    data() {
        return {


        }
    },
    methods: {
        goToAddProduct() {
            router.push('/add_product')
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


    }
};
</script>
