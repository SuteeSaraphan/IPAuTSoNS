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
                    <button type="button" @click="go_sort('1')">sort by newest </button>
                    <button type="button" @click="go_sort('2')">sort by oldest</button>
                    <input type="date" id="search_by_date" @change="go_search">
                </div>




                <!-- folder image list show here -->
                <div style="background:#e7e5e6">
                    <table style="width: 100%; padding:1%">


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
                        <tr v-if="payments < 1" style="text-align: center;
                                align-items: center;
                                color: #000;
                                background:#ccc;">
                            <td colspan="4">!!! You do not have any record !!!</td>
                        </tr>

                        <tr v-for="payment in payments" v-bind:key="payment.id"
                            style="margin-top: 5px;margin-bottom: 5px;background:#ccc; ">

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
.sort-btn button {
    color: black;
    padding: 0.5%;
    margin-right: 0.5%;
}

.sort-btn input {
    color: black;
    padding: 0.5%;
    margin-right: 0.5%;
}
</style>

<script>
import SlideBar from '@/components/SlideBar'
//import router from '@/router';
import axios from 'axios';
//import VueSlideBar from 'vue-slide-bar';
const URL_PRODUCT_HISTORY = "product_history"




export default {
    name: "ProductHistoryView",
    setup() {
       



    },
    data() {
        return {
            isLoading: true,
            sort_his: null,

        }
    },
    methods: {

        search_by_date(payment_list, date_sel) {
            let temp = [];
            for (let i in payment_list) {
                console.log(payment_list[i].pay_time.substring(0, 10))
                if (payment_list[i].pay_time.substring(0, 10) == date_sel) {
                    temp.push(payment_list[i])
                }
            }
            console.log(temp)
            return temp
        },


        // let path = "/img_folder/" + folder_id + "/1"
        // window.location.href = path

        go_sort(type) {
            if (type == "1") {
                let path = "/history/" + "newest"
                window.location.href = path;
            } else if (type == "2") {
                let path = "/history/" + "oldest"
                window.location.href = path;
            }

        },

        go_search() {
            let path = "/history/" + document.getElementById("search_by_date").value
            window.location.href = path;
        },


        sort(payment_list, type) {
            try {
                if (type == 'oldest') {
                    let temp = payment_list
                    temp.sort((a, b) => (a.pay_time > b.pay_time) ? 1 : ((b.pay_time > a.pay_time) ? -1 : 0));
                    payment_list = temp
                    return payment_list;
                }
                else if (type == 'newest') {
                    let temp = payment_list
                    temp.reverse((a, b) => (a.pay_time > b.pay_time) ? 1 : ((b.pay_time > a.pay_time) ? -1 : 0));
                    payment_list = temp
                    return payment_list;
                }
                else {
                    payment_list = this.search_by_date(payment_list, type);
                    return payment_list;
                }
            } catch (error) {
                return payment_list = [];
            }

        },





    }
    ,
    components: {
        SlideBar,
        //VueSlideBar
    },
    created() {
        console.log(this.$route.params.type);
        axios.defaults.headers.get['jwt']= this.$store.state.jwt;
        axios.get(URL_PRODUCT_HISTORY+"/"+this.$route.params.product_id+"/"+this.$route.params.type)
            .then(res => {
                console.log(res.data[0].pay_time.substring(0, 10))
                this.payments = this.sort(res.data, this.$route.params.type);
                this.isLoading = false
            })
            .catch(err => {
                this.isLoading = false
                console.log("error : "+err)
            })
    }


};
</script>
