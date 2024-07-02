import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../components/home/LoginPage.vue";
import AdminPage from "../components/home/AdminPage.vue";
import PlaygroundPage from "../components/home/PlaygroundCard.vue";
import ChatPage from "../components/chat/HomePage.vue";
import HomeEmpty from "../components/template/HomeEmptyPage.vue";
import HomeLogin from "../components/template/HomeLoginPage.vue";
import HomeAdmin from "../components/template/HomeAdminPage.vue";
import ChatSidebar from "../components/template/ChatSidebar.vue";
import ChatChat from "../components/template/ChatChatCard.vue";
import ChatSettings from "../components/template/ChatSettings.vue";
import ChatItemEditor from "../components/template/ChatItemEditor.vue";
import ChatRoles from "../components/template/ChatRoles.vue";
import CustomElComponents from "../components/template/CustomElComponents.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      // 默认打开跳转路由
      // https://juejin.cn/post/7195183916481773624
      path: "/",
      redirect: "/login",
    },
    {
      path: "/login",
      component: LoginPage,
    },
    {
      path: "/admin",
      component: AdminPage,
    },
    {
      path: "/playground",
      component: PlaygroundPage,
    },
    {
      path: "/chat",
      component: ChatPage,
    },
    {
      path: "/template/home/empty",
      component: HomeEmpty,
    },
    {
      path: "/template/home/login",
      component: HomeLogin,
    },
    {
      path: "/template/home/admin",
      component: HomeAdmin,
    },
    {
      path: "/template/chat/sidebar",
      component: ChatSidebar,
    },
    {
      path: "/template/chat/chat",
      component: ChatChat,
    },
    {
      path: "/template/chat/settings",
      component: ChatSettings,
    },
    {
      path: "/template/chat/item",
      component: ChatItemEditor,
    },
    {
      path: "/template/chat/roles",
      component: ChatRoles,
    },
    {
      path: "/template/custom/els",
      component: CustomElComponents,
    },
  ],
});
export default router;
