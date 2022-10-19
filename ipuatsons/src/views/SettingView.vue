<template>
    <div>
        <SlideBar></SlideBar>
        <div class="main-home">
            <div class="login-regis">
                <div class="menu">

                    <form style="padding:15px">
                        <h1>Profile setting Page</h1>
                        <div style="text-align: left">
                            <label style="font-size: 15px">Email :</label>
                            <p>
                                <input id="email" type="email" style="color:black" disabled="True" />
                            </p>
                        </div>
                        <div style="text-align: left">
                            <label style="font-size: 15px">Firstname :</label>
                            <p>
                                <input id="first_name" type="text" style="color:black" />
                            </p>
                        </div>
                        <div style="text-align: left">
                            <label style="font-size: 15px">Lastname :</label>
                            <p>
                                <input id="last_name" type="text" style="color:black" />
                            </p>
                        </div>




                        <div style="padding: 10px">
                            <input type="button" value="Submit" style="color:black" @click="edit_profile()" />
                            <input type="button" value="Clear" style="color:black" @click="clear()" />
                            <input type="button" value="Change password" style="width:85%" @click="change_password()">
                        </div>
                    </form>
                </div>


            </div>
        </div>
    </div>

</template>

<script>
import SlideBar from '@/components/SlideBar';
import { useCookies } from "vue3-cookies";
import router from '@/router';
const axios = require('axios').default;
export default {
    name: "SettingView",
    components: {
        SlideBar
    },
    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },
    data() {

    },
    methods: {
        edit_profile() {
            axios.put('http://127.0.0.1:8000/api/user',
                {
                    'jwt': this.cookies.get('jwt'),
                    'first_name': document.getElementById("first_name").value,
                    'last_name': document.getElementById("last_name").value
                }
            ).then(async res => {
                alert(res.data.status)
            }).catch(error => {
                alert(error);
            })

        },
        change_password() {
            router.push('/changepass')
        },
        
        clear(){
            document.getElementById("first_name").value = ""
            document.getElementById("last_name").value = ""
        }
    },
    created() {
            axios.defaults.headers.get['jwt'] = this.cookies.get('jwt');
            const URL = 'http://127.0.0.1:8000/api/user';
            axios.get(URL).then(async res => {
                document.getElementById("email").value = res.data.email
                document.getElementById("first_name").value = res.data.first_name
                document.getElementById("last_name").value = res.data.last_name
            }).catch(error => {
                alert(error);
            })
   

    }

}
</script>

<style>

</style>