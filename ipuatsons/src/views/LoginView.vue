<template>
    <div class="main-home">
        <h1>Login Page</h1>
        <form style="padding:15px">

            <div>
                <label>Email :</label>
                <p>
                    <input type="text" @change="(e) => setUser({ ...user, email: e.target.value })"
                        style="color:black" />
                </p>
            </div>

            <div>
                <label>Password :</label>
                <p>
                    <input type="password" @change="(e) => setUser({ ...user, password: e.target.value })"
                        style="color:black" />
                </p>
            </div>


            <input type="button" value="Login" style="color:black" @click="login()" />
        </form>

    </div>
</template>

<script>
import { useState } from '../composables/state';
export default {
    name: "LoginView",
    data() {
        const [user, setUser] = useState({
            email: "",
            password: ""
        });
        return {
            users: [],
            user,
            setUser,
            api_url: ''
        }
    },
    methods: {
        login() {
            this.api_url = 'http://127.0.0.1:8000/api/login/' + this.user.email + '/'
            fetch(this.api_url)
                .then(async response => await response.json())
                .then(async response => {
                    console.log(response)
                    this.users = response
                    if (this.users.password == this.user.password){
                        console.log('True')
                    }else{
                        console.log('False')
                    }
                })
               
            
            


        }
    }
}
</script>

<style>
</style>