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
                        <input id="pname" name="pname" type="text">

                        <label for="ptype">Product type :</label>
                        <input id="ptype" name="ptype" type="text">

                        <label for="pmodel">Product model :</label>
                        <input id="pmodel" name="pmodel" type="text">

                        <label for="price">Product price :</label>
                        <input id="price" name="price" type="text">

                        <label for="pimg">Product image : </label>
                        <input id="pimg" name="pimg" type="file" accept="image/*" @change="uploadImage($event)">

                    </form>
                </div>

            </main>
        </div>
        <label for="sidebar-toggle" class="body-label"></label>
    </div>
</template>
<style>
.product-form{
    margin: auto;
    width: 80%;
    padding: 2%;
    background-color: brown;
}
@media (max-width: 800px) {}
</style>
<script>
import SlideBar from '@/components/SlideBar'
import { useCookies } from "vue3-cookies";
import router from '@/router';
import axios from 'axios';

//const URL_GET_PRODUCT = 'http://127.0.0.1:8000/api/product';
//const URL_GET_IMG = 'http://127.0.0.1:8000/api/image';



export default {




    name: "AddProductView",
    setup() {
        const { cookies } = useCookies();
        return { cookies };



    },
    data() {
        return {
            isLoading: true,
            selectedImg : null,


        }
    },
    methods: {

        // choose image to upload
        uploadImage(event) {
            //console.log('event :'+event.target.files[0].name)
            this.selectedImg = event.target.files[0]
            //console.log('selectedImg :'+this.selectedImg)
        },

        //upload image to server
        onUploadFile() {
            //console.log(this.folder.folder_name)
            if (this.selectedFile.length > 0) {
                this.isLoading = true
                let data = new FormData();
                data.append('jwt', this.cookies.get('jwt'));
                data.append('folder', this.folder.folder_name);

                //console.log(this.selectedFile[0])

                for (let i = 0; i < this.selectedFile.length; i++) {
                    data.append('img_file', this.selectedFile[i]);
                }

                //console.log(data)

                let config = {
                    header: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
                axios.post(
                    //URL_IMG_UPLOAD,
                    data,
                    config
                ).then(
                    async (response) => {
                        this.isLoading = false
                        alert('image upload response >' + response.data['status'])
                        location.reload();
                    }
                ).catch(err => {
                    this.isLoading = false
                    alert(err)
                })
            } else {
                alert('please upload Image before add product')
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

        //cookie checker
        if (this.cookies.get('jwt') == null) {
            alert("You are not login yet , please login fisrt")
            router.push('/login')
        }
        else {

            // count image in from data base
            axios.defaults.headers.get['jwt'] = this.cookies.get('jwt');

        }
    }
};
</script>
