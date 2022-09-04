import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import DriveView from "../views/DriveView.vue";
import Img_appView from "../views/Img_appView.vue";

const routes = [
  {
    path: "/",
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
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
