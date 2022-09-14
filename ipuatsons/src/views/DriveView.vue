<template>
    <div class="main-home">
        <h1>Drive page</h1>
        <h1>v-model</h1>
        <input v-model="email" type="email" placeholder="enter your email">
        <div>
            <h1>{{ email }}</h1>
        </div>
        <button @click="email = ''" style="color:black">Reset</button>
        <button @click="get_token" style="color:black">get_token</button>

    </div>

</template>

<script>
export default {
    name: "DriveView",
    data() {
        return {
            email: "",
            token_url: "",
        }
    },
    methods: {
        
    },
};
</script>