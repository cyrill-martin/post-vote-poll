import { createRouter, createWebHistory } from "vue-router";

import Home from "./pages/Home.vue";
import About from "./pages/About.vue";
import Poll from "./pages/Poll.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: Home },
    { path: "/about", component: About },
    {
      path: "/poll/:id",
      component: Poll,
      props: true,
    },
    { path: "/:notFound(.*)", redirect: "/" },
  ],
  scrollBehavior() {
    return { left: 0, top: 0 };
  },
});

export default router;
