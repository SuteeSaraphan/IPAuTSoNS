import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import DriveView from "@/views/DriveView.vue";
import ImgAppView from "@/views/ImgAppView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisView from "@/views/RegisView.vue";
import SettingView from "@/views/SettingView";
import ChangePassView from "@/views/ChangePassView";
import ImgFolderView from "@/views/ImgFolderView";
import DemoView from "@/views/DemoView";
import DemoExportView from "@/views/DemoExportView";

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
    path: "/img_folder/:folder_id/:page",
    name: "img_folder",
    component: ImgFolderView,
  },

  {
    path: "/img_app",
    name: "img_app",
    component: ImgAppView,
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

  {
    path: "/demo",
    name: "demo",
    component: DemoView,
  },
  {
    path: "/demoexport",
    name: "demoexport",
    component: DemoExportView,
  },


];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
