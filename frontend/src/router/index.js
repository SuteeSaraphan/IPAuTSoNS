import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import DriveView from "@/views/DriveView.vue";
import ImgAppView from "@/views/ImgAppView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisView from "@/views/RegisView.vue";
import SettingView from "@/views/SettingView";
import ChangePassView from "@/views/ChangePassView";
import ImgFolderView from "@/views/ImgFolderView";
import DemoExportView from "@/views/DemoExportView";
import MaketView from "@/views/MarketView";
import ProductView from "@/views/ProductView";
import AddProductView from "@/views/AddProductView";
import ProductHistoryView from "@/views/ProductHistoryView";
import HistoryView from "@/views/HistoryView";
import AdminView from "@/views/AdminView";
import EditProductView from "@/views/EditProductView";

const routes = [
  {
    path: "/admin",
    name: "admin",
    component: AdminView,
  },
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
    path: "/img_app/:product_id",
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
    path: "/demoexport",
    name: "demoexport",
    component: DemoExportView,
  },


  {
    path: "/market/:keyword",
    name: "market",
    component: MaketView,
  },

  {
    path: "/product/:product_id",
    name: "product",
    component: ProductView,  
  },

  {
    path: "/add_product",
    name: "add_product",
    component: AddProductView,  
  },

  {
    path: "/edit_product/:product_id",
    name: "edit_product",
    component: EditProductView,  
  },

  {
    path: "/product_history/:product_id/:type",
    name: "product_history",
    component: ProductHistoryView,  
  },

  {
    path: "/history/:type",
    name: "history",
    component: HistoryView,  
  },





];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
