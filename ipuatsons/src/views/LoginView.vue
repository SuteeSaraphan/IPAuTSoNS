<template>
    <div class="login-regis">
        <div class="menu">
            <form style="width:25%">
                <img src="@/assets/logo.png" style="width:250px" alt="">
                <div style="text-align: left">
                    <label style="font-size: 15px">Email :</label>
                    <p>
                        <input id="email" type="text" @change="(e) => setUser({ ...user, email: e.target.value })"
                            style="color:black" />
                    </p>
                </div>

                <div style="text-align: left">
                    <label style="font-size: 15px">Password :</label>
                    <p>
                        <input id="password" type="password"
                            @change="(e) => setUser({ ...user, password: e.target.value })" style="color:black" />
                    </p>
                </div>

                <div style="padding: 7px">
                    <input type="button" value="Login" @click="login()" />
                    <input type="button" value="Register" style="color: white;background-color: #5294e2;"
                        @click="go_register()" />
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
            if (document.getElementById('email').value.length == 0) {
                alert('Email is empty')
            } else if (document.getElementById('password').value.length == 0) {
                alert('Password is empty')
            } else {
                axios.post('http://127.0.0.1:8000/api/login',
                    {
                        'email': this.user.email,
                        'password': this.user.password
                    }
                )
                    .then(async response => {
                        this.cookies.set('jwt', response.data.jwt, '3h')
                        router.push('/home');
                    }).catch(async error => {
                        alert(error.response.data['detail']);
                    })
            }


        },
        go_register() {
            router.push('/register');
        }
    },
    created() {
        if(this.cookies.get('jwt')!=null){
            router.push('/home');
        }
        


    }
}
</script>

