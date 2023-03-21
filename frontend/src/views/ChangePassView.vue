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
                    asd
                </div>
            </header>
            <main>
                <div class="setting">
                    <div class="menu">

                        <form style="padding:15px">
                            <h1>Change password Page</h1>
                            <div style="text-align: left">
                                <label style="font-size: 15px">Old password :</label>
                                <p>
                                    <input id="oldPassword" type="password" style="color:black" />
                                </p>
                            </div>
                            <div style="text-align: left">
                                <label style="font-size: 15px">New password :</label>
                                <p>
                                    <input id="newPassword" type="password" style="color:black" />
                                </p>
                            </div>
                            <div style="text-align: left">
                                <label style="font-size: 15px">New password confirm :</label>
                                <p>
                                    <input id="newPasswordConfirm" type="password" style="color:black" />
                                </p>
                            </div>




                            <div style="padding: 15px">
                                <input type="button" value="Submit" style="color:black" @click="editPassword()" />
                                <input type="button" value="Clear" style="color:black" @click="clear()" />
                                <input type="button" value="Back" style="width:85%" @click="back()">
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
import router from '@/router';
const axios = require('axios').default;
export default {
    name: "ChangePassView",
    components: {
        SlideBar
    },
    setup() {

    },
    data() {

    },
    methods: {
        editPassword() {
            axios.put('password',
                {
                    'jwt': this.$store.state.jwt,
                    'oldPassword': document.getElementById("oldPassword").value,
                    'newPassword': document.getElementById("newPassword").value
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
            document.getElementById("oldPassword").value = ""
            document.getElementById("newPassword").value = ""
            document.getElementById("newPasswordConfirm").value = ""
        }

    },
    created() {

        axios.defaults.headers.get['jwt'] = this.$store.state.jwt;
        axios.get('user')
            .then(res => res)
            .catch(err => {
                alert('Can not change password now try again later')
                console.log(err.data)
            })

    }

}
</script>

