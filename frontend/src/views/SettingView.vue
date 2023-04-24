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
                    User profile setting
                </div>
            </header>
            <main>
                <div class="setting">
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
                                <input type="button" value="Submit" style="color:black" @click="editProfile()" />
                                <input type="button" value="Clear" style="color:black" @click="clear()" />
                                <input type="button" value="Change password" style="width:85%"
                                    @click="changePassword()">
                            </div>
                        </form>
                    </div>


                </div>
            </main>
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
        async editProfile() {
            await axios.put('/user',
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
        changePassword() {
            router.push('/changepass')
        },

        clear() {
            document.getElementById("first_name").value = ""
            document.getElementById("last_name").value = ""
        }
    },
    async created() {
        axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
        await axios.get('user').then(async res => {
            document.getElementById("email").value = res.data.email
            document.getElementById("first_name").value = res.data.first_name
            document.getElementById("last_name").value = res.data.last_name
        }).catch(error => {
            alert(error);
        })


    }

}
</script>

