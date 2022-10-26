<template>
    <div>
        <SlideBar></SlideBar>
        <div class="main-home">
            <div class="login-regis">
                <div class="menu">

                    <form style="padding:15px">
                        <h1>Change password Page</h1>
                        <div style="text-align: left">
                            <label style="font-size: 15px">Old password :</label>
                            <p>
                                <input id="old_password" type="password" style="color:black" />
                            </p>
                        </div>
                        <div style="text-align: left">
                            <label style="font-size: 15px">New password :</label>
                            <p>
                                <input id="new_password" type="password" style="color:black" />
                            </p>
                        </div>
                        <div style="text-align: left">
                            <label style="font-size: 15px">New password confirm :</label>
                            <p>
                                <input id="new_password_confirm" type="password" style="color:black" />
                            </p>
                        </div>




                        <div style="padding: 15px">
                            <input type="button" value="Submit" style="color:black" @click="edit_password()" />
                            <input type="button" value="Clear" style="color:black" @click="clear()" />
                            <input type="button" value="Back" style="width:85%" @click="back()">
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
    name: "ChangePassView",
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
        edit_password() {
            axios.put('http://127.0.0.1:8000/api/password',
                {
                    'jwt': this.cookies.get('jwt'),
                    'old_password': document.getElementById("old_password").value,
                    'new_password': document.getElementById("new_password").value
                }
            ).then(async res => {
                alert(res.data.status)
            }).catch(error => {
                alert(error);
            })

        },
        back() {
            router.push('/setting')
        },

        clear() {
            document.getElementById("old_password").value = ""
            document.getElementById("new_password").value = ""
            document.getElementById("new_password_confirm").value = ""
        }

    },
    created() {
        if (this.cookies.get('jwt') == null) {
            alert("You are not login yet , please login fisrt")
            router.push('/login')
        }
        else {
            axios.defaults.headers.get['jwt'] = this.cookies.get('jwt');
            const URL = 'http://127.0.0.1:8000/api/user';
            axios.get(URL)
                .then(res => res)
                .catch(err => {
                    alert('Can not change password now try again later')
                    console.log(err.data)
                })

        }
    }

}
</script>

