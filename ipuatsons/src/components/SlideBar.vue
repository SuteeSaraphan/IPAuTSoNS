<template>
  <!-- Sidebar -->
  <div class="sidebar" v-if="this.email!=''">
      <a href="#" class="logo" style="text-align-last: center;">
        <h1>
          <router-link to="/">IPAUTSONS</router-link>
        </h1>
      </a>

      <!-- Profile -->
      <div class="profile">
        <div class="profile-img">
          <img src="@/img/profile.jpg" alt="">
        </div>
        <div class="name">
          <h1>PEACH</h1>
          <img src="@/img/name.png" alt="">
        </div>
        <span>Credit : 227</span>

        <span class="text-muted" style="font-size: 1rem;">Usage Total : <span id="total-value">32</span>GB</span>
        <!-- Info Bar -->
        <div class="bg-white rounded-xl shadow-sm overflow-hidden p-1">
          <div class="relative h-6 flex items-center justify-center">
            <div class="absolute top-0 bottom-0 left-0 rounded-lg w-[60%] bg-blue-200"></div>
            <div class="relative text-blue-900 font-medium text-sm">60%</div>
          </div>
        </div>
      </div>
      <!-- END Info Bar -->




      <!-- About -->
      <div class="about">
        <div class="box">
          <h3>54</h3>
          <span>Models</span>
        </div>

        <div class="box">
          <h3>22/7</h3>
          <span>Followers</span>
        </div>

        <div class="box">
          <h3>27</h3>
          <span>Following</span>
        </div>
      </div>

      <!-- Menu -->
      <div class="menu">

        <a href="#">
          <span class="icon">
            <i class="ri-function-line"></i>
          </span>
          <router-link to="/home">Feed</router-link>
        </a>

        <a href="#">
          <span class="icon">
            <i class="ri-hard-drive-2-line"></i>
          </span>
          <router-link to="/drive">Drive</router-link>
        </a>


        <a href="#">
          <span class="icon">
            <i class="ri-camera-lens-fill"></i>
          </span>
          <router-link to="/img_app">Image Application</router-link>
        </a>

        <a href="#">
          <span class="icon">
            <i class="ri-store-line"></i>
          </span>
          Marketplace
        </a>

        <a href="#">
          <span class="icon">
            <i class="ri-settings-line"></i>
          </span>
          Setting
        </a>

        <a @click="logout()" href="#">
          <span class="icon">
            <i class="ri-logout-box-line"></i>
          </span>
          Logout
        </a>

      </div>
    </div>
    <!----------------------------------------------------- end of side bar ----------------------------------------------------->
</template>

<script>
import { useCookies } from "vue3-cookies";
import router from '@/router';
export default {
    name:'SlideBar',
    setup() {
        const { cookies } = useCookies();
        return { cookies };
    }, 
    created(){
    if (this.cookies.get('jwt')==null){
      router.push('login')
    }
  },
    methods: {
      logout(){
        this.cookies.remove('jwt')
        router.push('login')
      }
  
  },
}

</script>

<style>

</style>