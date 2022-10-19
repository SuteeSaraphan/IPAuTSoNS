<template>
    <div class="login-regis">
        <div class="menu">
            <form style="width:25%">
                <img src="@/img/logo.png" style="width:250px" alt="">
                <div style="text-align: left">
                    <label style="font-size: 15px">Email :</label>
                    <p>
                        <input type="text" @change="(e) => setUser({ ...user, email: e.target.value })"
                            style="color:black" />
                    </p>
                </div>

                <div style="text-align: left">
                    <label style="font-size: 15px">Password :</label>
                    <p>
                        <input type="password" @change="(e) => setUser({ ...user, password: e.target.value })"
                            style="color:black" />
                    </p>
                </div>

                <div style="padding: 7px">
                    <input type="button" value="Login" style="color:black" @click="login()" />
                    <input type="button" value="Register" style="color:black" @click="go_register()" />
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { useState } from '../composables/state';
import { useCookies } from "vue3-cookies";
import router from '@/router';
const axios = require('axios').default;
export default {
    name: "LoginView",
    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },
    data() {
        const [user, setUser] = useState({
            email: "",
            password: ""
        });
        return {
            user,
            setUser
        }
    },
    methods: {
        login() {
            axios.post('http://127.0.0.1:8000/api/login',
                {
                    'email': this.user.email,
                    'password': this.user.password
                }
            )
                .then(async response => {
                    this.cookies.set('jwt', response.data.jwt, '1h')
                    axios.defaults.headers.get['jwt'] = this.cookies.get('jwt');
                    axios.get('http://127.0.0.1:8000/api/user')
                        .then(async res => {
                            res
                            router.push('/home')
                        }).catch(error => {
                            alert(error);
                        })
                })
        },
        go_register() {
            router.push('/register')
        }
    }
}
</script>

