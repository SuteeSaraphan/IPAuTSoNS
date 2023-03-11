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
                    Payment history
                </div>
            </header>


            <main>
                <div class="loading" v-if="this.isLoading">Loading&#8230;</div>
                <h1>Payment history</h1>

                
                <!-- filter history here  -->
                <div class="sort-btn" style="padding:5px;">
                    <button type="button" @click="sort('new')" >sort by newest </button>
                    <button type="button" @click="sort('old')" >sort by oldest</button>
                    <input type="date" id="search_by_date" @change="search_date()">
                </div>
                
                


                <!-- folder image list show here -->
                <div style="background:#e7e5e6">
                    <table style="width: 100%; padding:1%" >
                    
                        <tr v-if="payments < 1" 
                        style="text-align: center;
                            align-items: center;
                            color: #000;
                            background:#ccc;">
                            <td>!!! You do not have image folder !!!</td>
                        </tr>
                        <tr style="margin-top: 5px;margin-bottom: 5px; background-color: #ccc; text-align: center;">
                            <!-- <div style="display : flex; 
                             flex-direction : row;
                             justify-content: space-between;
                             align-items : center;

                             background:#ccc;"> -->
                                <td style="color:black;padding:10px; ">
                                    payment_id
                                </td>
                                <td style="color:black;padding:10px; justify-self: center;">
                                    product_id
                                </td>
                                <td style="color:black;padding:10px;">
                                    type
                                </td>
                                <td style="color:black;padding:10px;">
                                    pay_time
                                </td>

                        </tr>

                        <tr v-for="payment in payments" v-bind:key="payment.id" style="margin-top: 5px;margin-bottom: 5px;background:#ccc; ">

                            <!-- <div style="display : flex; 
                             flex-direction : row;
                             justify-content: space-between;
                             align-items : center;
                             padding-right: 15px;
                             background:#ccc;"> -->


                                <td style="color:black;padding:10px;">
                                    {{ payment.payment_id }}
                                </td>
                                <td style="color:black;padding:10px;">
                                    {{ payment.product_id }} 
                                </td>
                                <td style="color:black;padding:10px;">
                                    {{ payment.type }} 
                                </td>
                                <td style="color:black;padding:10px;">
                                    {{ payment.pay_time }}
                                </td>


                            
                        </tr>

                    
                </table>
                </div>


            </main>
        </div>
    </div>
</template>
<style>
    .sort-btn button{
        color: black;
        padding: 0.5%;
        margin-right: 0.5%;
    }
    .sort-btn input{
        color: black;
        padding: 0.5%;
        margin-right: 0.5%;
    }
</style>

<script>
import SlideBar from '@/components/SlideBar'
import { useCookies } from "vue3-cookies";
import router from '@/router';
import axios from 'axios';
//import VueSlideBar from 'vue-slide-bar';
const URL_PAYMENT = "http://127.0.0.1:8000/api/payment"




export default {
    name: "HistoryView",
    setup() {
        const { cookies } = useCookies();
        return { cookies };



    },
    data() {
        return {
            isLoading: true,

        }
    },
    methods: {
        search_date(){
            console.log(document.getElementById("search_by_date").value)
        },
        

        sort(type){
            if (type == 'old'){
                let temp = this.payments
                temp.sort((a,b) => (a.pay_time > b.pay_time) ? 1 : ((b.pay_time > a.pay_time) ? -1 : 0));
                this.payments = temp
                console.log(this.payments);
            }
            else if(type == 'new'){
                let temp = this.payments
                this.payments.reverse((a,b) => (a.pay_time > b.pay_time) ? 1 : ((b.pay_time > a.pay_time) ? -1 : 0));
                this.payments = temp
                console.log(this.payments);
            } 
        }





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
            axios.get(URL_PAYMENT)
                .then(res => {
                    this.payments = res.data;
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
