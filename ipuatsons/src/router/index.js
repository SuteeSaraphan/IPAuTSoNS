import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import DriveView from "@/views/DriveView.vue";
import Img_appView from "@/views/Img_appView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisView from "@/views/RegisView.vue";
import SettingView from "@/views/SettingView";
import ChangePassView from "@/views/ChangePassView";

const routes = [
  {
    path: "/home",
    name: "home",
    component: HomeView,
  },
  
  {
    path: "/drive",
    name: "drive",
    component: DriveView,
  },

  {
    path: "/img_app",
    name: "img_app",
    component: Img_appView,
  },

  {
    path: "/login",
    name: "login",
    component: LoginView,
  },

  {
    path: "/",
    name: "defult",
    component: LoginView,
  },

  {
    path: "/register",
    name: "register",
    component: RegisView,
  },
  
  {
    path: "/setting",
    name: "setting",
    component: SettingView,
  },

  {
    path: "/changepass",
    name: "changepass",
    component: ChangePassView,
  },


];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
