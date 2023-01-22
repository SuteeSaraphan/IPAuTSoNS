import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import "./assets/style.css"
import { globalCookiesConfig } from "vue3-cookies";


globalCookiesConfig({
    expireTimes: "5h",
    path: "/",
    domain: "",
    secure: true,
    sameSite: "None",
  });

createApp(App).use(store).use(router).mount('#app')

