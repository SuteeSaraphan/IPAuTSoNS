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
                        <h1>Add new product</h1>
                        <small>เพิ่มสินค้าใหม่</small>
                    </div>



                </div>

                <div class="product-form">
                    <form>
                        <label for="pname">Product name :</label>
                        <input id="pname" name="pname" type="text" required>

                        <label for="ptype">Product type :</label>
                        <input id="ptype" name="ptype" type="text" required>

                        <label for="pmodel">Product model :</label>
                        <input id="pmodel" name="pmodel" type="text" required>

                        <label for="pdetail">Product detail :</label>
                        <textarea id="pdetail" name="pdetail" type="text" required></textarea>

                        <label for="price">Product price :</label>
                        <input id="price" name="price" type="text" required>

                        <label for="pimg">Product image : </label>
                        <input id="pimg" name="pimg" type="file" accept="image/*" @change="uploadImage($event)" required>

                        <label for="pweight">Weight file : </label>
                        <input id="pweight" name="pweight" type="file" accept="" @change="uploadWeight($event)" required>


                    </form>
                    <button style="background-color: #5294e2; padding: 0.3%; margin-top: 1%;" @click="addProduct"
                        type="button"> Add product </button>

                    <p id="output"></p>
                </div>

            </main>
        </div>
        <label for="sidebar-toggle" class="body-label"></label>
    </div>
</template>
<style>
.product-form {
    margin: auto;
    width: 70%;
    padding: 2%;
}

textarea {
    width: 100%;
    height: 150px;
    padding: 12px 20px;
    box-sizing: border-box;
    border: 2px solid #ccc;
    border-radius: 4px;
    background-color: #f8f8f8;
    font-size: 13px;
    resize: none;
    color: black;
}

@media (max-width: 800px) {}
</style>
<script>
import SlideBar from '@/components/SlideBar'
//import router from '@/router';
import axios from 'axios';
const URL_ADD_PRODUCT = 'product';

export default {




    name: "AddProductView",
    setup() {

    },
    data() {
        return {

            selectedImg: null,
            selectedWeight: null,


        }
    },
    methods: {

        



        // choose image to upload
        uploadImage(event) {
            //console.log('event :'+event.target.files[0].name)
            this.selectedImg = event.target.files[0]
            if (this.selectedImg.size >= 15000000) {
                console.log('selectedImg :' + this.selectedImg.size)
                alert("This file is too big")
            } else {
                console.log('selectedImg :' + this.selectedImg.size)
            }

        },

        // choose weight to upload
        uploadWeight(event) {
            //console.log('event :'+event.target.files[0].name)
            this.selectedWeight = event.target.files[0]
            console.log('selectedWeight :' + this.selectedWeight.size)
            
        },

        //add product to database
        addProduct() {
            //console.log(this.folder.folder_name)
            if (this.selectedImg != null & this.selectedWeight != null) {
                this.isLoading = true
                let data = new FormData();
                data.append('product_img', this.selectedImg);
                data.append('weight_file', this.selectedWeight);
                data.append('name', document.getElementById("pname").value);
                data.append('type', document.getElementById("ptype").value);
                data.append('model', document.getElementById("pmodel").value);
                data.append('detail', document.getElementById("pdetail").value);
                data.append('price', document.getElementById("price").value);


                //console.log(data)

                let config = {
                    header: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
                axios.defaults.headers.post['jwt'] = this.$store.state.jwt;
                axios.post(
                    URL_ADD_PRODUCT,
                    data,
                    config
                ).then(
                    async (response) => {
                        alert('product upload response >' + response.data['status'])
                    }
                ).catch(err => {
                    alert(err)
                })
            } else {
                alert('Please upload image and weight before add product')
            }

        },


    }
    ,
    components: {
        SlideBar,
        //VueSlideBar
    },
    created() {
        console.log(this.$route.params.product_id)

    }
};
</script>
