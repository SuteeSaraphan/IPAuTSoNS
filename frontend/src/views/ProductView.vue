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
                        <h1>{{product.product_name}}</h1>
                        <small>By {{product.ownner}} || {{product.last_update}}</small>
                    </div>

                    <div class="header-actions" v-if="this.product['is_ownner']">
                        <button @click="this.goEditProduct">
                            <span class="las la-edit"></span>
                            Edit this product
                        </button>

                        <button @click="this.goProductHistory">
                            <span class="las la-history"></span>
                            View product use history
                        </button>
                    </div>

                </div>

                <div class="product-main">
                    <div class="product-img">
                        <img :src="`data:image/jpeg;base64,${product.product_img}`">
                    </div>
                    <div class="product-detail">
                        <h1>{{product.product_name}}</h1>
                        <small>By {{product.ownner}} || {{product.last_update}}</small>
                        <p>{{product.detail}}</p>

                        <button @click="tryThisWeight(product.product_id)"> Try this weight </button>

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

.product-img {
    width: 60%;
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

.product-detail {
    background-color: brown;
    width: 100%;
    padding: 2%;
}

.product-detail button {
    margin-top: 2%;
    color: rgb(0, 0, 0);
    font-weight: bold;
    width: 50%;
    padding: 1%;
    border-radius: 5px;
}

@media (max-width: 800px) {
    .product-main {
        flex-direction: column;
    }

    .product-img {
        margin-left: auto;
        margin-right: auto;
    }

    .product-detail button {
        margin-top: 2%;
        color: rgb(0, 0, 0);
        font-weight: bold;
        width: 100%;
        padding: 1%;
        border-radius: 5px;
    }
}
</style>
<script>
import SlideBar from '@/components/SlideBar'
import axios from 'axios';

const URL_GET_PRODUCT = 'product';

export default {
    name: "ProductView",
    setup() {
     



    },
    data() {
        return {
            isLoading: true,
            product: null

        }
    },
    methods: {
        tryThisWeight(product_id){
            //console.log("enter folder :"+folder_id)
            let path = "/img_app/" + product_id
            window.location.href = path
        },
        goEditProduct(){
            let path = "/edit_product/" + this.$route.params.product_id
            window.location.href = path
        }
    }
    ,
    components: {
        SlideBar,
        //VueSlideBar
    },
    created() {
        console.log(this.$route.params.product_id)
        // count image in from data base
        axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
        axios.get(URL_GET_PRODUCT + '/once/' + this.$route.params.product_id)
            .then(res => {
                //console.log('image : ' + res.data)
                console.log(res.data);
                this.product = res.data;
            }).catch(err => {
                alert(err);
            })
    }

};
</script>
