import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import "./assets/style.css"
import Axios from 'axios';
Axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';

createApp(App).use(store).use(router).mount('#app')

