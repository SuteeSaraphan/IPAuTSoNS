<template>
    <div style="display: flex; justify-content: center;">
        <div class="login-regis">
            <div class="menu">
                <form style="width:80%;
                justify-content: center;">
                    <img src="@/assets/logo.png" style="max-width:500px;width: 80%;" alt="">
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
    </div>
</template>

<script>
import { useState } from '../composables/state';
import router from '@/router';
const axios = require('axios').default;
export default {
    name: "LoginView",
    setup() {
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
        async login() {
            if (document.getElementById('email').value.length == 0) {
                alert('Email is empty')
            } else if (document.getElementById('password').value.length == 0) {
                alert('Password is empty')
            } else {
                await axios
                .post('login',
                    {
                        'email': this.user.email,
                        'password': this.user.password
                    }
                )
                    .then(response => {
                        this.$store.commit('setToken',response.data.jwt)
                        this.$store.commit('setName',[response.data.fname,response.data.lname])
                        axios.defaults.headers.get['jwt'] = this.cookies.get('jwt');
                        router.push('/home');
                    }).catch(error => {
                        alert(error.response.data['status']);
                    })
            }


        },
        go_register() {
            router.push('/register');
        }
    },
    created() {
        if (this.$store.state.isAuthenticated) {
            router.push('/home');
        }



    }
}
</script>

