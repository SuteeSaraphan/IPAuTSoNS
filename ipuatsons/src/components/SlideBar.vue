<template>
  <!-- Sidebar -->
  <input type="checkbox" name="" id="sidebar-toggle">
  <div class="sidebar">
    <div class="sidebar-brand">
      <div class="brand-flex">
        <img src="../img/logo.png" width="70px" alt="">

        <div class="brand-icons">
          <span class="las la-bell"></span>
          <span class="las la-user-circle"></span>
        </div>
      </div>
    </div>

    <div class="sidebar-main">
      <div class="sidebar-user">
        <img src="../img/profile.jpg" alt="">
        <div>
          <h3>Peach</h3>
          <span>Credit: 227</span>
          <span>Usage Total: 32GB</span>
          <span>60 %</span>
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
        </div>
      </div>
      <div class="sidebar-menu">
        <div class="menu-head">
          <span>User</span>
        </div>
        <ul>
          <li>
            <a>
              <span class="ri-function-line"></span>
              <router-link to="/home">Feed</router-link>
            </a>
          </li>
          <li>
            <a href="">
              <span class="ri-hard-drive-2-line"></span>
              <router-link to="/drive">My Drive</router-link>
            </a>
          </li>
          <li>
            <a href="">
              <span class="ri-settings-line"></span>
              <router-link to="/setting">User Setting</router-link>
            </a>
          </li>
        </ul>
        <div class="menu-head">
          <span>Applications</span>
        </div>
        <ul>

          <!-- Real -->
          <!-- <li>
            <a href="">
              <span class="ri-camera-lens-fill"></span>
              <router-link to="/img_app">ImageProcessing App</router-link>
            </a>
          </li> -->
          <!-- Real -->

          <!-- Demo -->
          <li>
            <a href="">
              <span class="ri-camera-lens-fill"></span>
              <router-link to="/img_app/0">ImageProcessing App</router-link>
            </a>
          </li>
          <!-- Demo -->


          <li>
            <a href="">
              <span class="ri-store-line"></span>
              <router-link to="/market">Marketplace</router-link>
            </a>
          </li>
        </ul>
        <li>
          <a @click="logout()">
            <span class="ri-logout-box-line"></span>
            Logout
          </a>
        </li>
      </div>
    </div>
  </div>
  <!----------------------------------------------------- end of side bar ----------------------------------------------------->
</template>

<script>
import { useCookies } from "vue3-cookies";
import router from '@/router';
export default {
  name: 'SlideBar',
  setup() {
    const { cookies } = useCookies();
    return { cookies };
  },
  created() {
    if (this.cookies.get('jwt') == null) {
      router.push('/login')
    }
  },
  methods: {
    logout() {
      this.cookies.remove('jwt')
      router.push('/login')
    }

  },
}

</script>


